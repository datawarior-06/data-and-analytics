# Data and Analytics Platforms

> End-to-end data engineering platform demonstrating production-grade batch, streaming, and big data solutions using modern cloud-native tools across Azure and AWS.

---

## Objectives

This project demonstrates practical proficiency in **Data Engineering**, **Data Analytics**, and **Big Data** problem-solving — covering the full spectrum from raw ingestion to analytics-ready warehouse layers, using industry-standard architecture patterns and tools.

All data used in this project is publicly available. This is a non-commercial, evolving project — completed modules are built to production-grade standards; work-in-progress sections are clearly marked within the codebase.

---

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Batch data solutions — maximum modularity, industry-grade efficiency and best practices | 🔄 In Progress |
| **Phase 2** | Low-latency stream data processing with big data scale | 📋 Planned |
| **Phase 3** | Next-generation analytics — data science integration, ML pipelines, scaling strategies | 📋 Planned |

Throughout all phases: cloud-independent tooling, multi-framework implementation, and cutting-edge open standards.

---

## High Level Design Architecture — Phase 1

![Data and Analytics HLD Architecture](https://github.com/user-attachments/assets/a19e0961-6f05-44d9-bd9f-c54e074b1b16)

### Architecture Overview

Phase 1 implements a **purchase orders analytics pipeline** — ingesting transactional data from REST APIs, AWS S3, and CSV flat files into a medallion lakehouse architecture, terminating in an Azure SQL data warehouse for reporting.

**Source Systems**
- REST API (JSON/XML)
- AWS S3 (Parquet, JSON)
- CSV files via SFTP / Blob drop

**Orchestration & CI/CD**
- Azure Data Factory — Copy Activity, Data Flows, Linked Services, Triggers
- GitHub + GitHub Actions — version control, CI/CD pipeline, Dev → QA → Prod environment promotion
- Databricks Asset Bundles (`databricks.yml`) — notebook and job deployment

**Medallion Lakehouse (Databricks Community + ADLS Gen2)**
- 🟤 **Bronze** — raw landing zone, append-only Delta, schema-on-read
- ⬜ **Silver** — cleansed, deduplicated, SCD 1/SCD 2, data quality enforced
- 🟡 **Gold** — aggregated, Kimball star schema (Facts + Dimensions), query-optimised Delta (Z-ORDER, VACUUM)

**In-Transit Processing**
- Azure Functions — general-purpose compute, multi-cloud API integration
- Azure Logic Apps — lightweight alerting and workflow triggers
- Azure Data Lake Storage Gen2 — intermediate and staging storage
- AWS S3 — primary data storage 

**Security & Governance**
- Azure Key Vault — secrets, connection strings, certificates
- AWS IAM — roles and policies for S3 and cross-cloud access
- GitHub Actions Environment Credentials — CI/CD secret management

**Warehouse**
- Azure SQL Database — relational data warehouse, Facts and Dimensions, views, stored procedures

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Orchestration | Azure Data Factory, GitHub Actions |
| Processing | Databricks (PySpark), Azure Functions, Azure Logic Apps |
| Storage | Azure Data Lake Storage Gen2, AWS S3, Delta Lake |
| Warehouse | Azure SQL Database |
| Security | Azure Key Vault, AWS IAM |
| DevOps | GitHub, GitHub Actions, Databricks Asset Bundles |
| Languages | Python, PySpark, SQL |

---

## Concepts Demonstrated

`ETL/ELT` `Medallion Architecture` `Data Warehousing` `Lakehouse` `SCD 1 / SCD 2` `Delta Lake` `Kimball Modeling` `Spark Optimization` `Data Quality` `Data Governance` `Multi-Cloud` `DevOps / DataOps` `CI/CD` `Performance Tuning` `Big Data`

---

## Repository Structure

```
├── .github/workflows/          # GitHub Actions CI/CD pipelines
├── azure-function/             # Azure Function app — purchase orders transfer
├── data-and-analytics-factory/ # ADF factory export (ARM templates)
├── dataset/                    # Sample / reference datasets
├── docs/                       # Low-level documentation per business use case
│   └── purchase-orders/        # Mapping specs, data dictionaries, flow docs
├── factory/                    # ADF pipeline JSON definitions
├── linkedService/              # ADF linked service configurations
├── notebooks/                  # Databricks notebooks (bronze / silver / gold)
├── pipeline/                   # ADF pipeline definitions
├── databricks.yml              # Databricks Asset Bundle config
├── publish_config.json         # ADF publish configuration
└── requirements.txt            # Python dependencies
```

> For detailed mappings, data dictionaries, and flow documentation for each business use case, see `/docs`.

---

## Getting Started

> **Prerequisites:** Azure subscription, Databricks Community Edition account, AWS account (free tier sufficient), GitHub account.

1. **Clone the repo**
   ```bash
   git clone https://github.com/datawarior-06/data-and-analytics.git
   ```

2. **Set up secrets** — add the following to GitHub Actions Environment Credentials (Dev / QA / Prod):
   - `AZURE_SUBSCRIPTION_ID`
   - `ADF_RESOURCE_GROUP`
   - `DATABRICKS_HOST` and `DATABRICKS_TOKEN`
   - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

3. **Deploy ADF** — publish via GitHub Actions workflow or manually import `factory/` ARM templates into your Azure Data Factory instance.

4. **Deploy Databricks notebooks** — use Databricks Asset Bundles:
   ```bash
   databricks bundle deploy
   ```

5. **Navigate to `/docs/purchase-orders`** for end-to-end setup guide for the Phase 1 use case.

---

## Contact

Questions, ideas, or collaboration interest? Reach out at **balasourvendra@gmail.com** with subject line `Data-And-Analytics`.

Contributions and feedback are always welcome — this project is designed to grow.
