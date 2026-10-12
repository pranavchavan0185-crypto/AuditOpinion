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

**A3. Target sample size: 12 companies (6 flagged + 6 matched clean controls). Stretch only if time allows.**
*Why:* the project had about 11 working days, and every company needs a hand-checked audit report and a price file. A small, fully verified sample is more defensible than a larger rushed one. The reduction is a time constraint, not a design preference, and is declared in the report.
*Risk:* very low statistical power. With about 12 observations, a test can only detect very large differences. Results will be described, and tests reported with this caveat; "no detectable difference in this sample" will not be read as "no effect".

**A4. Sampling method: purposive matched sample, not random.**
*Why:* Modified opinions are rare among NSE-listed companies. A random 100 would contain too few to test. We declare this openly on the methodology page.
*Risk:* Selection effects; results describe this sample, not all NSE companies.

**A5. Flagged group (6): highest-severity signal in the index report decides the stratum.**
Hierarchy: Disclaimer > Adverse > Qualified > Going-concern material uncertainty (unmodified opinion) > EOM only. Target: mainly Qualified, with at least one going-concern or EOM case if available. If a stratum cannot be filled, the shortfall is reported.
*Risk:* disclaimers and adverse opinions are very rare.

**A6. Control group (6): unmodified opinion, no EOM, no going-concern paragraph, report for the same index financial year as the flagged firm it is matched to.**
Matching: 1:1 on industry group and approximate size (market capitalisation), as far as the data allows.
*Risk:* matching is approximate; unobserved differences remain.

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

**C1. Abnormal return (primary): 125 market trading days (about 6 months).** Stock buy-and-hold return minus Nifty 50 buy-and-hold return over the same two dates. A 250-day (12-month) window is reported as a secondary result where price data allows.
Entry = closing price on the date the audited results (with the audit report) were published on the exchange, or the last market day before it. Exit = closing price 125 market days later. The window is counted on the Nifty trading calendar, so every company is measured over the same dates.
*Why 125 days as primary:* one price download per company fits the available time, and 6 months is long enough for the market to absorb an audit signal.
*Why entry is the announcement-day close:* results are often released after market hours, so the market reaction falls on the next trading day, which then sits inside the window.
*Why market-adjusted:* simple, hand-checkable, and answers "did the market under- or over-react".
*Risk:* ignores beta; announcement time is not checked case by case; microcap prices are noisy.

**C2. Prices adjusted for splits, bonuses and dividends where the source allows.** If a stock is delisted or suspended during the window, the return is measured to the last available price and flagged.

**C3. Auditor change (secondary).** The audit firm (by firm registration number) signing the next year's report differs from the index year. We record the reason: resignation / non-reappointment / completion of tenure. The primary test counts only changes before completion of tenure. [VERIFY Companies Act rotation limits on MCA]

**C4. Restatement (exploratory only).** Identified from later annual reports and exchange filings that explicitly say figures were restated. If fewer than 5 restatement cases are found, it is reported descriptively and not tested.
*Why:* Restatement data is not published in one place; undercounting is likely.

**C5. Repeat qualification (control variable).** Many filings state, in the Statement on Impact of Audit Qualifications, how often a qualification has repeated. A qualification repeated for years carries little new information. We record `repeat_qualification` (yes/no/not stated) from that statement.

**C6. Optional fundamental check:** next-year net loss (yes/no), from published financial statements.

**C7. Missing price data is reported, not filled.** If a stock has no usable price at entry or exit (for example trading suspended or moved to another series), the abnormal return is recorded as missing with the reason. The engine rejects a price more than 5 calendar days old.
*Why it matters:* the firms most likely to drop out are the most distressed ones. Dropping them biases results toward finding no effect (survivorship bias). The count of missing cases is reported in the results.

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
