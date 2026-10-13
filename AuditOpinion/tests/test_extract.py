"""
Tests for extract.py coding rules.

The fixtures below are SYNTHETIC: short strings written in the standard wording of
SA 700 / 705 / 706 / 570. They are not copied from any company's report.
Real-report validation (hand-checked sample + Cohen's kappa) is done separately in Chapter 11.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from extract import (code_report, company_category, frequency_statements, process_pages,  # noqa: E402
                     repeat_qualification, split_reports)

BOILERPLATE = (
    "Auditor's Responsibilities. Conclude on the appropriateness of the use of the going concern "
    "basis of accounting and whether a material uncertainty exists related to events or conditions "
    "that may cast significant doubt. Other Matters. The figures for the last quarter are balancing figures."
)

CLEAN = "Independent Auditor's Report To the Members. Opinion. In our opinion the statements give a true and fair view. Basis for Opinion. " + BOILERPLATE
QUAL_FOR = "Independent Auditor's Report To the Board. Qualified Opinion. except for the effects of the matter described in the Basis for Qualified Opinion section, give a true and fair view. Basis for Qualified Opinion. The company has not provided for X."
QUAL_OF = "Independent Auditor's Report To the Board. Qualified Opinion. Basis of Qualified Opinion. The company has not provided for X. " + BOILERPLATE
ADVERSE = "Independent Auditor's Report To the Members. Adverse Opinion. Basis for Adverse Opinion. The statements do not give a true and fair view."
DISCLAIM = "Independent Auditor's Report To the Members. Disclaimer of Opinion. We do not express an opinion. Basis for Disclaimer of Opinion. We could not obtain evidence."
EOM = "Independent Auditor's Report To the Members. Opinion. true and fair view. Emphasis of Matter. We draw attention to Note 12. Our opinion is not modified in respect of this matter."
GC = "Independent Auditor's Report To the Members. Opinion. true and fair view. Material Uncertainty Related to Going Concern. We draw attention to Note 5."
KAM = "Independent Auditor's Report To the Members. Opinion. true and fair view. Key Audit Matters. Revenue recognition. " + BOILERPLATE


def test_clean_report_is_unmodified_and_boilerplate_does_not_trigger_going_concern():
    r = code_report(CLEAN)
    assert r["opinion_type"] == "U"
    assert not r["eom_flag"] and not r["going_concern_flag"]


def test_qualified_both_heading_variants():
    assert code_report(QUAL_FOR)["opinion_type"] == "Q"
    assert code_report(QUAL_OF)["opinion_type"] == "Q"     # "Basis of Qualified Opinion" wording


def test_adverse_and_disclaimer():
    assert code_report(ADVERSE)["opinion_type"] == "A"
    assert code_report(DISCLAIM)["opinion_type"] == "D"


def test_eom_is_flag_not_modified_opinion():
    r = code_report(EOM)
    assert r["eom_flag"] is True
    assert r["opinion_type"] == "U"          # EOM does NOT modify the opinion


def test_going_concern_heading_sets_flag():
    r = code_report(GC)
    assert r["going_concern_flag"] is True
    assert r["opinion_type"] == "U"


def test_other_matters_and_kam_are_not_eom():
    assert not code_report(KAM)["eom_flag"]
    assert not code_report(CLEAN)["eom_flag"]


def test_qualified_plus_eom_codes_both_layers():
    r = code_report(QUAL_FOR + " Emphasis of Matter. See Note 9.")
    assert r["opinion_type"] == "Q" and r["eom_flag"]


def test_severity_order_disclaimer_beats_qualified():
    r = code_report(QUAL_FOR + " " + DISCLAIM)
    assert r["opinion_type"] == "D"


def test_split_standalone_and_consolidated_and_ignore_annexure_reference():
    standalone = "Independent Auditor's Report To the Board. Opinion. true and fair view of the Company."
    consol = ("Independent Auditor's Report To the Board. Report on the Consolidated Financial Results. "
              "Qualified Opinion. Basis for Qualified Opinion. Subsidiary matter. "
              "See Annexure A to the Independent Auditor's Report for details.")
    pages = [standalone, consol]
    reports = split_reports(pages)
    assert [r[0] for r in reports] == ["standalone", "consolidated"]   # annexure sentence did not split
    coded, category, _ = process_pages(pages)
    assert coded[0]["opinion_type"] == "U" and coded[1]["opinion_type"] == "Q"
    assert category == "Q"                                             # highest severity wins


def test_company_category_order():
    base = {"opinion_type": "U", "eom_flag": False, "going_concern_flag": False}
    assert company_category([dict(base, eom_flag=True)]) == "EOM-only"
    assert company_category([dict(base, going_concern_flag=True, eom_flag=True)]) == "GC-only"
    assert company_category([dict(base), dict(base, opinion_type="A")]) == "A"
    assert company_category([dict(base)]) == "U"


def test_repeat_qualification_detected():
    text = ("Frequency of qualification: This has been subject matter of qualification in the "
            "auditor's report since the year 2007 and has continued. d. Management's views")
    assert repeat_qualification(text) is not None
    assert repeat_qualification("Frequency of qualification: First time. d.") is None


def test_split_when_heading_says_report_on_standalone_and_consolidated():
    pages = ["Independent Auditor's Report on Standalone Audited Annual Financial Results of the Company "
             "Pursuant to Regulation 33 To the Board of Directors of X Limited Qualified Opinion. Basis for Qualified Opinion. Y.",
             "Independent Auditor's Report on Consolidated Audited Annual Financial Results of the Group "
             "Pursuant to Regulation 33 To the Board of Directors of X Limited Qualified Opinion. Basis for Qualified Opinion. Z."]
    reports = split_reports(pages)
    assert [r[0] for r in reports] == ["standalone", "consolidated"]


def test_frequency_repeat_new_and_mixed():
    text = ("Frequency of qualification: Qualification was also present in previous year (d) For Audit ... "
            "(b) Frequency of qualification: Qualification added in current year. (c) For Audit ... "
            "Frequency of qualification: Qualified for the first time in the Limited Review for the quarter.")
    labels = [l for l, _ in frequency_statements(text)]
    assert labels == ["repeat", "new", "new"]


def test_split_tolerates_ocr_noise_in_heading():
    pages = ["Independent Auditor's Report on Standalone Results To the Board of X. Qualified Opinion. Basis for Qualified Opinion.",
             "Independent Auditor1 s Report on Consolidated Results To the Board of X. Opinion. true and fair view."]
    reports = split_reports(pages)
    assert [r[0] for r in reports] == ["standalone", "consolidated"]


def test_ifc_material_weakness_sets_ifc_flag():
    txt = ("Independent Auditor's Report To the Board of X. Qualified Opinion. Basis for Qualified Opinion. Receivables. "
           "Auditor's Qualification on the Internal Financial Controls relating to above matters: the following material "
           "weakness have been identified in the operating effectiveness of the internal financial controls.")
    r = code_report(txt)
    assert r["ifc_modified_flag"] is True
    assert code_report(CLEAN)["ifc_modified_flag"] is False     # boilerplate about IFC must not trigger
