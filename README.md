# IFCO Data Engineering Challenge

Solution to the [IFCO Data Engineering Test](https://github.com/Digital-IFCO/data-engineering-test), developed in **Databricks Community Edition** with PySpark.

---

## Repository structure

```
ifco_challenge/
├── data/
│   ├── orders.csv
│   └── invoicing_data.json
├── notebooks/
│   ├── 000_Setup.py              ← data ingestion and path configuration
│   ├── 00_DataDiscovery.py       ← exploratory data analysis
│   ├── 01_CrateType.py           ← test 1: crate type distribution per company
│   ├── 02_OrdersName.py          ← test 2: contact full name
│   ├── 03_OrdersAddress.py       ← test 3: contact address
│   ├── 04_SalesCommissions.py    ← test 4: sales team commissions
│   └── 05_SalesOwners.py         ← test 5: companies and their sales owners
├── src/
│   └── transformations.py        ← pure functions used across notebooks
├── tests/
│   ├── test_01.py
│   ├── test_02.py
│   ├── test_03.py
│   ├── test_04.py
│   └── test_05.py
├── dashboard/
│   └── ifco_dashboard.pbix       ← optional: Power BI visualization (test 6)
├── Dockerfile
└── requirements.txt
```

---

## How to run — unit tests (Docker)

No Databricks account needed. Requires [Docker](https://www.docker.com/get-started) installed.

```bash
git clone https://github.com/smoyacopa/ifco_challenge.git
cd ifco_challenge
docker build -t ifco-challenge .
docker run ifco-challenge
```

All 5 test files will run automatically and results will be printed to the console.

---

## How to run — notebooks (Databricks)

1. Open [Databricks Community Edition](https://community.cloud.databricks.com)
2. Go to **Repos** → **Add repo** → paste the repository URL:
   ```
   https://github.com/smoyacopa/ifco_challenge
   ```
3. Run notebooks in order, starting with `000_Setup`

> Data is downloaded automatically from this repository — no manual file upload or additional configuration required.

---

## Technical decisions

- **Databricks + PySpark** — notebooks developed and tested in Databricks Community Edition
- **Separation of concerns** — business logic lives in `src/transformations.py` as pure Python functions, keeping notebooks focused on orchestration and making unit testing possible without a Spark cluster
- **Dynamic path resolution** — `000_Setup` detects the repository root at runtime using `dbutils`, so notebooks work regardless of where the repo is cloned
- **Data ingestion from GitHub** — source files are downloaded from the public repository URL to `/tmp/` on the cluster driver, avoiding any dependency on DBFS or Unity Catalog
- **Company name deduplication** — company names are normalised before grouping (lowercase, remove non-alphanumeric characters) to consolidate dirty duplicates such as `"Fresh Fruits Co"` / `"Fresh Fruits c.o"`
- **Invoice deduplication** — one `order_id` has two invoices with identical amounts (exact duplicate). Deduplication is applied using `ROW_NUMBER()` before commission calculation to avoid inflating results
- **VAT handling** — invoice amounts are stored in cents and VAT as a percentage string. Net value is calculated as `gross / (1 + vat/100) / 100`
- **Commission tiers** — position 1 (main owner): 6%, position 2: 2.5%, position 3: 0.95%, remaining positions: 0%
