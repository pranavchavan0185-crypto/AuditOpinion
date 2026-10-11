# AuditOpinion — Modified Opinion Study

**Research question:** What do modified audit opinions (and Emphasis of Matter / going-concern signals) predict about a listed Indian company's subsequent performance?

PGDM Capstone, Imperial School of Banking & Management Studies, Pune.
Authors: Pranav Sandip Chavan (PGDM/25/24) · Anamika Singh (PGDM/25/30)

## Status
Framework stage. See `codebook.md`, `assumptions.md`, `sources.csv`.

## Five layers
| Layer | Files |
|---|---|
| L1 Ingest | `ingest.py`, `data/`, `sources.csv` |
| L2 Extract | `extract.py`, `rag/` |
| L3 Engine | `engine/`, `tests/` |
| L4 Commentary | `commentary.py`, `governance.md` |
| L5 Output | `app.py`, `report.py` |

## Data
Secondary, published data only (annual reports, exchange filings, NSE prices). Every pull is logged in `sources.csv`.
No synthetic data is used unless declared in `assumptions.md`.

## How to run
(To be completed as each layer is built.)

## Disclaimer
Educational research project. Nothing here is investment advice.
