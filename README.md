# 🚀 Job Listings Data Pipeline

> A production-ready ETL pipeline that fetches job listings from a public API, validates data quality with dbt, and orchestrates daily runs using Apache Airflow.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791.svg)
![Airflow](https://img.shields.io/badge/Airflow-2.x-017CEE.svg)
![dbt](https://img.shields.io/badge/dbt-1.5+-FF694B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📖 Overview

This pipeline solves a common data engineering challenge: **how to reliably ingest, clean, and validate external API data for analytics**.

**What it does:**
- Fetches job listings daily from a public API
- Stores raw JSON for complete data lineage
- Transforms messy data into clean, structured tables
- Enforces data quality with automated dbt tests
- Fails fast when data doesn't meet standards

**Why it matters:** Downstream analysts can trust the data is complete, deduplicated, and always up-to-date.

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Jobs API      │  External data source
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Python Ingestion│  Fetch & store raw JSON
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  raw_jobs       │  PostgreSQL (JSONB storage)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SQL Transform   │  Clean, normalize, dedupe
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ cleaned_jobs    │  PostgreSQL (structured tables)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   dbt Tests     │  Validate data quality
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Airflow DAG    │  Orchestrate & monitor
└─────────────────┘
```

**Tech Stack:**
- **Python** → API ingestion
- **PostgreSQL** → Data storage & SQL transformations  
- **Airflow** → Orchestration, scheduling, retries
- **dbt** → Data quality enforcement

---

## 🔄 Pipeline Flow

| Step | Action | Output |
|------|--------|--------|
| 1️⃣ | Airflow triggers daily at 2 AM UTC | Pipeline starts |
| 2️⃣ | Python script fetches jobs from API | Raw JSON stored |
| 3️⃣ | SQL extracts & normalizes fields | Structured records |
| 4️⃣ | UPSERT logic deduplicates data | Clean table updated |
| 5️⃣ | dbt runs validation tests | Pass/Fail status |
| 6️⃣ | Pipeline succeeds or fails | Alert sent |

**Key Feature:** Fully idempotent—safe to re-run without duplicates.

---

## ✅ Data Quality (dbt)

### What Gets Validated

Every run checks the `cleaned_jobs` table for:

| Test | Column | Rule |
|------|--------|------|
| 🔑 **Primary Key** | `job_id` | NOT NULL + UNIQUE |
| 🏢 **Company** | `company_name` | NOT NULL |
| 💼 **Job Title** | `title` | NOT NULL |

### dbt Schema Definition

```yaml
models:
  - name: cleaned_jobs
    columns:
      - name: job_id
        tests:
          - not_null
          - unique
      - name: company_name
        tests:
          - not_null
      - name: title
        tests:
          - not_null
```

### What Happens on Failure

❌ If ANY test fails → **Airflow DAG fails**  
✅ Only clean, validated data reaches production

This guarantees analysts never query incomplete or duplicate records.

---

## 🎯 Design Decisions

### What I Prioritized

| Decision | Rationale |
|----------|-----------|
| **SQL over Pandas** | Better performance, easier to review |
| **Raw data preservation** | Enables reprocessing & auditing |
| **Simple Airflow operators** | More maintainable than complex TaskFlow |
| **dbt for validation only** | Keeps transformations in plain SQL |
| **Idempotent UPSERT** | Safe for backfills & re-runs |

### What I Skipped (Intentionally)

- ❌ Kubernetes / Docker orchestration → Not needed at this scale
- ❌ Real-time streaming → Batch daily is sufficient
- ❌ Advanced partitioning → Current volume doesn't require it
- ❌ Complex monitoring → Airflow alerts cover basics

**Philosophy:** Start simple, scale when needed.

---

## 📊 Example Query

```sql
-- Find top companies hiring right now
SELECT 
    company_name, 
    COUNT(*) as total_jobs
FROM cleaned_jobs
GROUP BY company_name
ORDER BY total_jobs DESC
LIMIT 10;
```

---

## 📁 Project Structure

```
job-listings-pipeline/
├── dags/
│   └── job_listings_dag.py      # Airflow DAG definition
├── scripts/
│   ├── fetch_jobs.py            # API ingestion
│   └── clean_jobs.py            # Data transformation
├── models/
│   └── schema.yml               # dbt tests
├── sql/
│   ├── schema/                  # Table DDL
│   └── transforms/              # Cleaning logic
└── README.md
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙋 Questions?

Open an issue or reach out at **your.email@example.com**

---

<div align="center">

**Built with ❤️ by [Your Name]**

⭐ Star this repo if you find it useful!

</div>
