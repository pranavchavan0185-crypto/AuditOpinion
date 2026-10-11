# Codebook — Audit Opinion Coding

Purpose: so that two people reading the same report assign the same codes.
Rule: code only what the report says. Never infer. If unsure, mark `UNCLEAR` and discuss with your co-coder.

## 0. Which document and which section

- Use the **annual** "Independent Auditor's Report" on the **standalone** and **consolidated** financial statements.
- Ignore quarterly limited-review reports.
- Opinion section: "Opinion" / "Qualified Opinion" / "Adverse Opinion" / "Disclaimer of Opinion".
- Basis section: "Basis for Opinion" / "Basis for Qualified Opinion" etc.
- Record the page number of every piece of evidence.

## 1. Layer 1 — Opinion type (choose exactly one per report)

| Code | Meaning | Standard | Trigger phrases (illustrative standard wording) |
|---|---|---|---|
| U | **Unmodified** (clean). Financial statements give a true and fair view. | SA 700 | "give a true and fair view"; heading "Opinion" with no "Basis for Qualified/Adverse" |
| Q | **Qualified.** Fair view *except for* a specific material matter. | SA 705 | heading "Basis for Qualified Opinion"; "except for the effects of the matter described in the Basis for Qualified Opinion section" |
| A | **Adverse.** Statements are materially and pervasively misstated. | SA 705 | heading "Basis for Adverse Opinion"; "do not give a true and fair view" because of the matter described |
| D | **Disclaimer.** Auditor could not obtain enough evidence and effects could be pervasive. | SA 705 | heading "Basis for Disclaimer of Opinion"; "we do not express an opinion" |

Heading wording varies: "Basis for Qualified Opinion" and "Basis of Qualified Opinion" are both common. Treat them the same.

Decision rule: if the opinion paragraph is headed "Qualified Opinion", "Adverse Opinion" or "Disclaimer of Opinion", code that, regardless of what the notes say.

## 2. Layer 2 — Flags (each Yes/No; independent of opinion type)

| Flag | Code YES when... | Standard | Trigger phrases |
|---|---|---|---|
| EOM | A separate paragraph headed **"Emphasis of Matter"** appears and the opinion is not modified because of it. | SA 706 | heading "Emphasis of Matter"; "Our opinion is not modified in respect of this matter" |
| GC | A section headed **"Material Uncertainty Related to Going Concern"** appears. | SA 570 | "material uncertainty exists that may cast significant doubt on ... ability to continue as a going concern" |
| IFC | The report on **Internal Financial Controls** (annexure) has a qualified or adverse opinion. | ICAI guidance note on IFC reporting [VERIFY] | "adverse opinion on internal financial controls"; "material weakness" |

Do NOT code as EOM or modified:
- **Key Audit Matters** (heading "Key Audit Matters"): not warnings.
- **"Other Matter"** paragraphs (SA 706): they refer to something not presented in the financial statements. Optionally record as `OM`, but they are not EOM.
- CARO remarks in the annexure: note them in `evidence_text` but do not change the opinion code.
- A going-concern *discussion in the notes* with no auditor paragraph.

Relationships to remember:
- EOM = **clean opinion + a spotlight paragraph**. Not a modified opinion.
- Going-concern material uncertainty = **separate section**, also not itself a modified opinion. If the uncertainty is not adequately disclosed, the auditor modifies the opinion (Q or A) instead.
- A report can have Q **and** an EOM, or Q **and** GC. Code every layer that applies.

## 3. Layer 3 — Reason category (only if Q, A, D, EOM or GC applies)

Choose the **primary** reason and optionally one secondary.

| Code | Reason |
|---|---|
| R1 | Revenue recognition |
| R2 | Receivables / loans / advances (recoverability, provisioning) |
| R3 | Investments, subsidiaries or goodwill (impairment, valuation) |
| R4 | Related-party transactions or balances |
| R5 | Inventory, fixed assets or other balance-sheet existence/valuation |
| R6 | Litigation, contingent liabilities or regulatory matters |
| R7 | Going concern, liquidity or debt servicing |
| R8 | Internal financial controls |
| R9 | Limitation of scope (records unavailable, evidence not obtainable) |
| R10 | Other (describe) |

Also note the **financial statement area** affected (Revenue, Receivables, Investments, Inventory, Borrowings, Other) in `evidence_text`.

## 4. Mapping to the four categories in the capstone brief

| Brief category | Our coding |
|---|---|
| Clean | opinion = U, EOM = No, GC = No |
| Emphasis of matter | opinion = U, EOM = Yes (GC may also be Yes) |
| Qualified | opinion = Q |
| Adverse | opinion = A (Disclaimer reported as its own row) |

Company-level category (for sampling): highest severity of the standalone and consolidated report, ordered
**D > A > Q > GC-only > EOM-only > U**.

## 5. Coding sheet columns (`data/coding_sheet.csv`)

`company_name, index_fy, report_type (standalone/consolidated), coder, opinion_type, eom_flag, going_concern_flag, ifc_modified_flag, repeat_qualification, reason_category, evidence_text, page_ref, source_id`

- `evidence_text`: copy the exact sentence(s) that justify the code, in quotation marks.
- `page_ref`: PDF page number.
- `repeat_qualification`: yes / no / not stated, from the frequency line of the company's Statement on Impact of Audit Qualifications.
- Each coder fills their own rows; do not look at your partner's coding until both are complete.

## 6. Worked examples (fill with real reports; do not invent)

| Code | Company | FY | Evidence sentence (exact) | Page | Source ID |
|---|---|---|---|---|---|
| Q | | | | | |
| EOM | | | | | |
| GC | | | | | |
| U | | | | | |

## 7. Disagreement log

| Company | FY | Coder 1 | Coder 2 | Why we differed | Final code | Codebook change? |
|---|---|---|---|---|---|---|

## 8. Agreement statistics (for Chapter 11)

- Percent agreement = matching codes ÷ total coded reports.
- Cohen's kappa = (observed agreement − chance agreement) ÷ (1 − chance agreement).
  Common interpretation (Landis & Koch): 0.61–0.80 substantial; above 0.80 almost perfect.
  Report percent agreement alongside kappa, because rare categories can make kappa unstable.
