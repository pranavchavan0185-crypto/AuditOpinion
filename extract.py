"""
extract.py  --  Layer 2 (Extract)

Reads an audit-report PDF (or plain text) and codes it using the rules in codebook.md.

DESIGN RULE: the rules below decide the category, not a language model.
Every coded flag stores the sentence that triggered it and the page number,
so each result can be traced to the source document.

Usage:
    python extract.py path/to/report.pdf
    python extract.py path/to/report.pdf --csv data/processed/auto_coded.csv
"""
import argparse
import csv
import os
import re

# ---------------------------------------------------------------------------
# 1. READING THE PDF
# ---------------------------------------------------------------------------

def read_pdf_pages(path):
    """Return a list of page texts. Needs: pip install pdfplumber"""
    import pdfplumber
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages


def clean(text):
    """Normalise curly quotes and whitespace so phrase matching is reliable."""
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", text)


# ---------------------------------------------------------------------------
# 2. SPLITTING INTO INDIVIDUAL AUDITOR'S REPORTS
# ---------------------------------------------------------------------------
# A results PDF or annual report can hold a standalone AND a consolidated report.
# A real report starts with the heading followed by "To ..." (the addressee).
# This avoids false splits on sentences like "Annexure A to the Independent Auditor's Report".

REPORT_START = re.compile(r"independent auditor'?s'? report\s+to\b", re.IGNORECASE)


def split_reports(pages):
    """Return a list of (scope, start_page, text) for each auditor's report found."""
    # Build one string, remembering where each page begins.
    full, offsets = "", []
    for i, p in enumerate(pages, start=1):
        offsets.append((len(full), i))
        full += clean(p) + " "

    starts = [m.start() for m in REPORT_START.finditer(full)]
    if not starts:                      # fallback: treat the whole document as one report
        return [("unknown", 1, full)]

    def page_at(pos):
        pg = 1
        for off, num in offsets:
            if off <= pos:
                pg = num
        return pg

    reports = []
    for idx, s in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(full)
        text = full[s:end]
        scope = "consolidated" if "consolidated" in text[:400].lower() else "standalone"
        reports.append((scope, page_at(s), text))
    return reports


# ---------------------------------------------------------------------------
# 3. THE CODING RULES (mirror codebook.md)
# ---------------------------------------------------------------------------
# NOTE: boilerplate such as "whether a material uncertainty exists related to events..."
# appears in EVERY clean report, so the going-concern flag looks for the SECTION HEADING only.

RULES = {
    "D": [r"basis for disclaimer of opinion", r"disclaimer of opinion"],
    "A": [r"basis (?:for|of) adverse opinion", r"\badverse opinion\b"],
    "Q": [r"basis (?:for|of) qualified opinion", r"except for the effects? of the matters? described in the basis"],
}
EOM_PATTERNS = [r"emphasis of matters?", r"our opinion is not modified in respect of th(?:is|ese) matters?"]
GC_PATTERNS = [r"material uncertainty related to going concern"]
IFC_MOD_PATTERNS = [r"adverse opinion on (?:the )?internal financial controls",
                    r"qualified opinion on (?:the )?internal financial controls"]

SEVERITY = ["D", "A", "Q"]   # checked in this order; first hit wins (Disclaimer > Adverse > Qualified)


def find_evidence(text, patterns, width=110):
    """Return (matched_phrase, snippet around it) for the first pattern that hits, else None."""
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            a, b = max(0, m.start() - width), min(len(text), m.end() + width)
            return m.group(0), text[a:b].strip()
    return None


def code_report(text):
    """Apply the codebook to ONE auditor's report. Returns a dict of codes and evidence."""
    result = {"opinion_type": "U", "eom_flag": False, "going_concern_flag": False,
              "ifc_modified_flag": False, "evidence": {}}

    for code in SEVERITY:
        hit = find_evidence(text, RULES[code])
        if hit:
            result["opinion_type"] = code
            result["evidence"]["opinion"] = hit
            break

    hit = find_evidence(text, EOM_PATTERNS)
    if hit:
        result["eom_flag"] = True
        result["evidence"]["eom"] = hit

    hit = find_evidence(text, GC_PATTERNS)
    if hit:
        result["going_concern_flag"] = True
        result["evidence"]["going_concern"] = hit

    hit = find_evidence(text, IFC_MOD_PATTERNS)
    if hit:
        result["ifc_modified_flag"] = True
        result["evidence"]["ifc"] = hit
    return result


def repeat_qualification(full_text):
    """Detect the 'Statement on Impact of Audit Qualifications' frequency line, if present.
    Returns the sentence if the filing says the qualification has repeated, else None."""
    m = re.search(r"frequency of qualification[^.]*\.[^.]*\.", full_text, re.IGNORECASE)
    if m and re.search(r"since the year|repetitive|repeated|continued", m.group(0), re.IGNORECASE):
        return m.group(0)
    return None


# ---------------------------------------------------------------------------
# 4. COMPANY-LEVEL CATEGORY (for sampling) - codebook section 4
# ---------------------------------------------------------------------------

def company_category(coded_reports):
    """Highest severity across reports:  D > A > Q > GC-only > EOM-only > U"""
    types = [r["opinion_type"] for r in coded_reports]
    for code in SEVERITY:
        if code in types:
            return code
    if any(r["going_concern_flag"] for r in coded_reports):
        return "GC-only"
    if any(r["eom_flag"] for r in coded_reports):
        return "EOM-only"
    return "U"


# ---------------------------------------------------------------------------
# 5. RUN ON A FILE
# ---------------------------------------------------------------------------

def process_pages(pages, source_name="document"):
    reports = split_reports(pages)
    coded = []
    for scope, page, text in reports:
        c = code_report(text)
        c.update({"report_type": scope, "page_ref": page, "source": source_name})
        coded.append(c)
    full = clean(" ".join(pages))
    return coded, company_category(coded), repeat_qualification(full)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--csv", help="append coded rows to this CSV")
    args = ap.parse_args()

    pages = read_pdf_pages(args.pdf)
    coded, category, repeat = process_pages(pages, os.path.basename(args.pdf))

    print(f"File: {args.pdf}  |  pages read: {len(pages)}  |  reports found: {len(coded)}")
    for c in coded:
        print(f"\n[{c['report_type']}] starts page {c['page_ref']}")
        print(f"  opinion_type={c['opinion_type']}  EOM={c['eom_flag']}  "
              f"GC={c['going_concern_flag']}  IFC_modified={c['ifc_modified_flag']}")
        for key, (phrase, snip) in c["evidence"].items():
            print(f"  evidence[{key}]: ...{snip}...")
    print(f"\nCompany-level category: {category}")
    print(f"Repeat qualification stated in filing: {repeat or 'not stated'}")
    print("\nAUTOMATIC CODING ONLY. A human must check each result against the PDF.")

    if args.csv:
        new = not os.path.exists(args.csv)
        with open(args.csv, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["source", "report_type", "page_ref", "opinion_type", "eom_flag",
                            "going_concern_flag", "ifc_modified_flag", "evidence_opinion",
                            "repeat_qualification_text", "company_category"])
            for c in coded:
                ev = c["evidence"].get("opinion", ("", ""))[1]
                w.writerow([c["source"], c["report_type"], c["page_ref"], c["opinion_type"],
                            c["eom_flag"], c["going_concern_flag"], c["ifc_modified_flag"],
                            ev, repeat or "", category])


if __name__ == "__main__":
    main()
