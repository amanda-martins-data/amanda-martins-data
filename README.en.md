[Português](README.md) | **English**

<p align="center"><img src="assets/hero-en.svg" width="860" alt="Amanda Martins, Data Engineering and Analytics Engineering" /></p>

<p align="center">
<a href="https://www.linkedin.com/in/amandamartinsdts/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="mailto:amanda_mdantas@outlook.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
</p>

Data engineer. At work, I build production pipelines on Azure; in my portfolio, a complete data platform around a single domain, from ingestion to governance. Looking for **Data Engineering** or **Analytics Engineering** roles, remote or hybrid.

## 01 / The platform

Fourteen projects, one domain: air quality and climate in Brazil. Each project solves one layer of the platform, and the decisions made in one show up in the next.

<p align="center"><img src="assets/platform-en.svg" width="860" alt="Platform map: public sources feed ingestion (01, 02, 12, 13) and storage (03, 14, 04), which serve Power BI and AI; reliability (06, 05, 10) and governance (07, 08, 09, 11) cut across the whole platform" /></p>

## 02 / Case studies

<table>
<tr>
<td width="33%" valign="top">

**[Keys that don't match](https://github.com/amanda-martins-data/pipeline-multi-fonte-dados-publicos)**<br>
<sub>Project 13 · Python · DuckDB</sub>

**Problem:** three public sources with no common key.

**Finding:** 9.4% of Brazilian municipalities can't be reached by name alone, and stripping accents creates 8 new collisions.

**Decision:** resolve by name + state, with coordinates only as supporting evidence ([ADR 0012](https://github.com/amanda-martins-data/pipeline-multi-fonte-dados-publicos/blob/main/decisions/0012-estrategia-para-municipios-sem-correspondencia.md)).

**Result:** 5M+ rows joined by municipality, 100% resolved with name and state.

</td>
<td width="33%" valign="top">

**[Same architecture, two engines](https://github.com/amanda-martins-data/snowflake-medallion-qualidade-ar)**<br>
<sub>Projects 03 and 14 · dbt · Snowflake</sub>

**Problem:** reprocess without duplicates, then take the design to the cloud.

**Decision:** the same Medallion on Parquet + DuckDB and natively on Snowflake, with `COPY INTO`, Bronze in `VARIANT` and an incremental Silver with `MERGE`.

**Result:** idempotent reruns in both versions; 16/16 models and tests on Snowflake, with least-privilege roles.

</td>
<td width="33%" valign="top">

**[When the architecture breaks](https://github.com/amanda-martins-data/capacity-planning-qualidade-ar)**<br>
<sub>Project 10 · Python · AWS</sub>

**Problem:** know how far the AWS infrastructure (Lambda, S3, RDS) can go.

**Decision:** a capacity and cost model parameterized by volume, with tests.

**Result:** Lambda breaks at 45.2x the current volume; the expected 10x growth runs in 203 s, a quarter of the limit.

</td>
</tr>
</table>

## 03 / In production

**CPEA** · Mid-level Data Analyst, Data Engineering (Oct 2025 – present)

- Python pipelines serving **5 business areas**, from REST APIs (including ArcGIS) to ADLS Gen2 and DuckDB; **30% less execution time** in one of the processes.
- End-to-end data applications (PostgreSQL, FastAPI, Docker) on Azure Container Apps, deployed through OIDC with **zero secrets** in the repositories.
- Rolled out Azure DevOps for the team's agile delivery and ran internal trainings, including data architecture for IT.

<sub>Before: 5 years in data analysis and BI, across education, aviation and mobility. Lean Six Sigma Green Belt.</sub>

## 04 / Stack

<p align="center"><img src="assets/stack-en.svg" width="860" alt="Stack: Python, SQL, PostgreSQL, dbt, DuckDB, Snowflake, Airflow, Great Expectations, pytest, GitHub Actions, Azure (ADLS Gen2, Container Apps, Key Vault, Entra ID), Terraform, Docker, AWS, FastAPI, Power BI, Claude" /></p>

<details>
<summary><b>All 14 projects, one by one</b></summary>

| # | Project | Delivers |
|---|---|---|
| 01 | [ELT pipeline with dbt](https://github.com/amanda-martins-data/pipeline-qualidade-ar) | Public API ingestion, dimensional model and declarative tests |
| 02 | [Airflow orchestration](https://github.com/amanda-martins-data/orquestracao-airflow-qualidade-ar) | DAG with retries, alerts and branching |
| 03 | [Medallion architecture](https://github.com/amanda-martins-data/arquitetura-medallion-qualidade-ar) | Bronze/Silver/Gold layers on Parquet |
| 04 | [IaC on AWS](https://github.com/amanda-martins-data/iac-pipeline-cloud-qualidade-ar) | Lambda, S3 and RDS in Terraform |
| 05 | [Pipeline with AI](https://github.com/amanda-martins-data/ai-pipeline-qualidade-ar) | AI agents for data quality and documentation |
| 06 | [Observability](https://github.com/amanda-martins-data/observabilidade-qualidade-ar) | Great Expectations plus freshness and completeness checks |
| 07 | [ADRs](https://github.com/amanda-martins-data/adr-arquitetura-dados) | Architecture decisions with alternatives and a review trigger |
| 08 | [Governance and catalog](https://github.com/amanda-martins-data/governanca-catalogo-dados) | RACI, retention, LGPD classification and a catalog with lineage |
| 09 | [Corporate blueprint](https://github.com/amanda-martins-data/blueprint-arquitetura-corporativa) | Conceptual, logical and physical models and non-functional requirements |
| 10 | [Capacity planning](https://github.com/amanda-martins-data/capacity-planning-qualidade-ar) | Breaking points at 10x and 100x, with a tested cost model |
| 11 | [Security and access](https://github.com/amanda-martins-data/seguranca-acesso-dados) | RBAC, PII masking and auditing |
| 12 | [Streaming](https://github.com/amanda-martins-data/streaming-qualidade-ar) | Schema registry and event bus with tested guarantees |
| 13 | [Multi-source pipeline](https://github.com/amanda-martins-data/pipeline-multi-fonte-dados-publicos) | Three public sources joined with entity resolution |
| 14 | [Medallion on Snowflake](https://github.com/amanda-martins-data/snowflake-medallion-qualidade-ar) | Native Bronze/Silver/Gold on Snowflake with dbt and RBAC |

**In progress:** an Azure lakehouse as code (Databricks, Unity Catalog, Terraform) and data for AI (RAG and an MCP server over the Gold layer).

</details>

<p align="center"><img src="assets/city-en.svg" width="860" alt="Animated city of GitHub contributions: each block is a week and each lot a day" /></p>

---

<p align="center">
<a href="https://www.linkedin.com/in/amandamartinsdts/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="mailto:amanda_mdantas@outlook.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
</p>

<p align="center"><sub>Amanda Martins · layout inspired by the <a href="https://www.gitskins.com/readme-generator?template=community-builder-s-workbench-city-edition-9udn">Builder’s Workbench — City Edition</a> template by <a href="https://www.gitskins.com/creators/pengusto">@pengusto</a> on GitSkins</sub></p>
