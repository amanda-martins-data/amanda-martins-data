[Português](README.md) | **English**

<p align="center"><img src="assets/hero-en.svg" width="860" alt="Amanda Martins, Data Engineering and Architecture" /></p>

<p align="center">
<a href="https://www.linkedin.com/in/amandamartinsdts/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="mailto:amanda_mdantas@outlook.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
</p>

<p align="center"><img src="https://www.gitskins.com/api/section/city?username=amanda-martins-data&theme=retro" width="860" alt="GitHub contribution skyline" /></p>

Data professional with 6+ years of experience and a post-graduate degree in Data Architecture (PUC Minas). I build pipelines in Python and SQL, layered architectures on Azure and documented architecture decisions. Looking for **Data Engineering (Mid-level)** or **Analytics Engineering** roles, remote or hybrid.

## 01 / Results

**At CPEA** · Mid-level Data Analyst, Data Engineering (Oct 2025 – present)

- **5 business areas served** by Python pipelines that integrate REST APIs (including ArcGIS) with ADLS Gen2 and an analytics layer in DuckDB and SQL.
- **30% shorter run time** after turning a manual spreadsheet process into an API-based pipeline that writes to the bronze layer.
- **No secrets in repositories:** deployment with GitHub Actions and identity federation (OIDC); Docker apps on Azure Container Apps with Key Vault and Entra ID.
- **End-to-end data applications:** PostgreSQL databases with versioned, audited migrations, FastAPI services and web interface integration.

**Organization and governance**

- I support the technical organization of the data team: roadmap structuring and delivery tracking in Azure DevOps.
- I contribute to the company's AI governance and data protection: usage policies, risk mapping and AI automations (OCR and report generation).

**In the public portfolio**

- **5,025,594 real rows** from INMET joined to 5,570 IBGE municipalities and CETESB readings.
- **100% municipality resolution** with name and state, after finding that 9.4% cannot be reached by name alone.
- **13 published projects, 11 with CI** on GitHub Actions; decisions recorded as ADRs, with alternatives and a review trigger.

## 02 / Featured projects

<p align="center"><img src="assets/projects-en.svg" width="860" alt="Featured projects" /></p>

The documentation inside each repository is in Portuguese.

| Project | Problem | Result |
|---|---|---|
| [13 · Multi-source pipeline](https://github.com/amanda-martins-data/pipeline-multi-fonte-dados-publicos) | Three public sources whose keys do not match | 5M+ rows joined by municipality; 100% resolution with name and state |
| [03 · Medallion architecture](https://github.com/amanda-martins-data/arquitetura-medallion-qualidade-ar) | Reprocessing without duplicating data | Bronze/Silver/Gold on Parquet with dbt; a rerun gives the same result |
| [02 · Airflow orchestration](https://github.com/amanda-martins-data/orquestracao-airflow-qualidade-ar) | A manual pipeline with no fault tolerance | Scheduling, retries with backoff and alerts; switching sources without redeploys |
| [04 · IaC on AWS](https://github.com/amanda-martins-data/iac-pipeline-cloud-qualidade-ar) | Infrastructure created by hand | Lambda, S3 and RDS versioned in Terraform |
| [10 · Capacity planning](https://github.com/amanda-martins-data/capacity-planning-qualidade-ar) | Knowing when the architecture breaks | Breaking point calculated at 45.2x current volume; 14/14 tests |
| [11 · Security and access](https://github.com/amanda-martins-data/seguranca-acesso-dados) | Access control for sensitive data | Tested RBAC, PII masking and an audit trail |

<details>
<summary><b>All 13 projects</b></summary>

| # | Project | Delivers |
|---|---|---|
| 01 | [ELT pipeline with dbt](https://github.com/amanda-martins-data/pipeline-qualidade-ar) | OpenAQ ingestion, dimensional model and declarative tests |
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
| 13 | [Multi-source pipeline](https://github.com/amanda-martins-data/pipeline-multi-fonte-dados-publicos) | INMET + IBGE + CETESB with entity resolution |

</details>

## 03 / Stack

<p align="center"><img src="assets/stack-en.svg" width="860" alt="Portfolio stack" /></p>

## 04 / In progress

- **Azure lakehouse as code:** ADLS Gen2, Databricks and Unity Catalog in Terraform, with PySpark and Delta Lake jobs.
- **Data for AI:** a RAG pipeline and an MCP server on the Gold layer, using the access control from Project 11.

---

<p align="center">
<a href="https://www.linkedin.com/in/amandamartinsdts/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="mailto:amanda_mdantas@outlook.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
</p>

<p align="center"><sub>Amanda Martins · layout inspired by the <a href="https://www.gitskins.com/readme-generator?template=community-builder-s-workbench-city-edition-9udn">Builder’s Workbench — City Edition</a> template by <a href="https://www.gitskins.com/creators/pengusto">@pengusto</a> on GitSkins</sub></p>
