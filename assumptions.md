# Assumptions (defend every one in the viva)

Each assumption: what we assume, why, and what could go wrong.
Mark `[VERIFY]` items on the source before citing them in the report.

## A. Scope and sample

**A1. Unit of observation.** One *index report* per company: the annual audit report in which the audit signal is observed. Not a company-year panel.
*Why:* Keeps the analysis simple enough to explain line by line and avoids overlapping return windows.
*Risk:* Less data than a panel; results rest on a small sample.

**A2. Index period: audit reports for FY2021-22, FY2022-23 and FY2023-24.**
*Why:* (i) Every report has a full 12-month forward return window already observable. (ii) It avoids FY2019-20 and FY2020-21, when many EOM paragraphs referred to COVID-19 uncertainty and would blur what EOM means [VERIFY on sample]. (iii) It keeps workload feasible.
*Risk:* Narrow window; may not generalise to other years.

**A3. Target sample size: 60 companies (25 flagged + 35 controls). Stretch target 100 only if coding is complete by 14 October.**
*Why:* Two people can hand-verify 60 reports properly in the time available. A smaller, fully verified sample is more defensible than a larger rushed one.
*Risk:* Low statistical power. Non-significant results will not prove "no effect"; they will show "no detectable effect in this sample".

**A4. Sampling method: purposive matched sample, not random.**
*Why:* Modified opinions are rare among NSE-listed companies. A random 100 would contain too few to test. We declare this openly on the methodology page.
*Risk:* Selection effects; results describe this sample, not all NSE companies.

**A5. Flagged group (25): highest-severity signal in the index report decides the stratum.**
Hierarchy: Disclaimer > Adverse > Qualified > Going-concern material uncertainty (unmodified opinion) > EOM only.
Target strata: Modified opinion (qualified/adverse/disclaimer) 12 · Going-concern only 5 · EOM only 8.
*Why:* Makes strata mutually exclusive. If a stratum cannot be filled, we report the shortfall rather than lower the standard.
*Risk:* Disclaimers and adverse opinions are very rare; the modified stratum may be mostly "qualified".

**A6. Control group (35): unmodified opinion, no EOM, no going-concern paragraph, same index FY as the flagged firm it is matched to.**
Matching: 1:1 on industry group and market-cap band (terciles of the sample) for the 25 flagged firms; the remaining 10 are extra controls from the most heavily flagged industries.
*Why:* Controls separate "audit signal" from "industry or size effect".
*Risk:* Matching is approximate; unobserved differences remain.

**A7. Standalone vs consolidated.** Both reports are coded. The company-level category is the more severe of the two; the report type that drove it is recorded.
*Why:* Consolidated qualifications often arise from subsidiary or associate matters and differ from standalone.

**A8. Exclusions:** quarterly limited-review reports; banks, NBFCs and insurers (different financial structure and regulator) [confirm with faculty]; companies with fewer than 12 months of listed price history before the index date.
*Why:* Not comparable with the main sample.

## B. Coding

**B1. Three-layer coding, as in `codebook.md`.** Opinion type (Unmodified / Qualified / Adverse / Disclaimer) is coded separately from the EOM flag and the going-concern flag. EOM is NOT a modified opinion.

**B2. Qualification in the Internal Financial Controls report is coded as a separate flag**, not as a modified opinion on the financial statements.

**B3. Key Audit Matters (KAMs) are not audit signals.** They are not coded as EOM or qualification.

**B4. Coding is rule-based (phrase triggers in the codebook). The language model only helps locate text; it never decides the category.** Every coded case stores the evidence text and page reference.

**B5. Validation:** both authors independently code the sample (all 60 if possible; at least 25, stratified to include every category). We report percent agreement and Cohen's kappa, and resolve disagreements by re-reading the report and updating the codebook.

## C. Outcomes

**C1. Abnormal return (primary).** Stock buy-and-hold return minus Nifty 50 buy-and-hold return over 250 trading days (about 12 months), starting from the first trading day after the date the audited results (with the audit report) were published on the exchange. Secondary window: 125 trading days.
*Why:* Market-adjusted return is simple, hand-checkable, and answers "did the market under- or over-react".
*Risk:* Market-adjusted return ignores beta. Stated as a limitation.

**C2. Prices adjusted for splits, bonuses and dividends where the source allows.** If a stock is delisted or suspended during the window, the return is measured to the last available price and flagged.

**C3. Auditor change (secondary).** The audit firm (by firm registration number) signing the next year's report differs from the index year. We record the reason: resignation / non-reappointment / completion of tenure. The primary test counts only changes before completion of tenure. [VERIFY Companies Act rotation limits on MCA]

**C4. Restatement (exploratory only).** Identified from later annual reports and exchange filings that explicitly say figures were restated. If fewer than 5 restatement cases are found, it is reported descriptively and not tested.
*Why:* Restatement data is not published in one place; undercounting is likely.

**C5. Optional fundamental check:** next-year net loss (yes/no), from published financial statements.

## D. Statistics

**D1. Mann-Whitney U** for abnormal returns (returns are skewed and the sample is small).
**D2. Fisher's exact test** for auditor change vs audit signal (small cell counts make chi-square unreliable).
**D3. One OLS regression:** abnormal return on audit-signal flags plus controls (log market cap, previous-year loss, Debt/Equity). Controls kept to four or fewer because of sample size.
**D4. Significance level 5%.** We also report effect size (difference in median abnormal return) so practical significance is separate from statistical significance.

## E. Interpretation

**E1. Association, not causation.** Distress can cause both the qualification and the poor return (reverse causality). We say "associated with", never "causes" or "proves".
**E2. No fraud claims.** An audit signal indicates elevated risk, not wrongdoing.

## F. Data and ethics

**F1. Secondary, published data only. No synthetic data is planned. If any is used, it is declared here and on the methodology page.**
**F2. Every number in the report traces to a row in `sources.csv`.**
**F3. Generated commentary cites a source or a computed number; uncited sentences are removed.**
