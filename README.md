<div align="center">

# Amanda Martins

`data_engineer.py`

</div>

```python
class AmandaMartins:
    def __init__(self):
        self.experience    = "6+ years in Data"
        self.current_role  = "Data Analyst -> Data Engineering"
        self.background     = "Environmental Engineering"
        self.focus_areas    = ["ETL/ELT Pipelines", "REST API Integration", "Data Architecture"]
        self.stack          = ["Python", "SQL", "ADLS Gen2", "DuckDB", "Power BI", "Claude/LLMs"]
        self.pursuing        = "Post-Graduate in Data Architecture, PUC Minas (2026)"

    def current_work(self):
        return [
            "Designing ETL pipelines and REST API integrations",
            "Building data adapters with Python, SQL, ADLS Gen2, DuckDB",
            "Delivering dashboards, KPI frameworks and reporting solutions",
            "Deploying AI-powered interfaces in production",
        ]
```

---

## About

Data professional with 6+ years of experience translating complex, multi-source datasets into actionable insights and scalable data infrastructure. Currently working as a Data Analyst while progressively taking on Data Engineering responsibilities: designing ETL pipelines, building REST API integrations, and developing data adapters using Python, SQL, ADLS Gen2, and DuckDB.

My background spans Business Intelligence, data governance, and analytical modeling, with a track record of delivering dashboards, KPI frameworks, and reporting solutions across infrastructure, sustainability (ESG), and education sectors.

As a trained Environmental Engineer, I bring domain expertise in spatial data (QGIS/ArcGIS), ESG regulatory frameworks (GRI, ISE B3, DJSI), and environmental monitoring data — adding a strategic, cross-domain layer to my analytics work that purely technical profiles often lack.

Currently pursuing a Post-Graduate degree in Data Architecture at PUC Minas (2026), reinforcing my path toward senior and architect-level data roles.

---

## Technical Stack

*Split by where each skill was used. **Professional**: day-to-day in my current and past roles. **Portfolio**: applied hands-on in the projects below (project numbers in parentheses).*

| Area | Professional | Portfolio |
|---|---|---|
| **Languages** | Python · SQL · JavaScript | Python · SQL |
| **Data Engineering** | ETL/ELT · REST API integration · ADLS Gen2 · DuckDB · data adapters | dbt + DuckDB (01-03) · Medallion architecture with Parquet/PyArrow (03) · entity resolution on dirty public data (13) |
| **Orchestration & Infra** | GitHub Actions · Azure DevOps | Airflow + Docker (02) · Terraform on AWS: Lambda, RDS PostgreSQL, EventBridge, Secrets Manager, IAM (04) |
| **Data Quality & Testing** | | Great Expectations (06) · pytest test suites (04-06, 08, 10-13) |
| **Architecture & Governance** | Data governance | ADRs (07, 13) · dimensional modeling decisions (07, 09) · capacity & cost modeling (10) · catalog, lineage & LGPD classification (08) · RBAC & PII masking (11) · schema registry & event-driven design (12) |
| **AI** | AI-powered interfaces in production | Claude API for data quality checks and documentation (05) |
| **BI & Analytics** | Power BI · DAX · data modeling · KPI design · statistical analysis · data storytelling | |
| **Spatial & Domain** | QGIS · ArcGIS · ESG reporting (GRI, ISE B3, DJSI) · environmental monitoring data | Brazilian public environmental sources: INMET, CETESB, IBGE (13) |
| **Methodologies** | Lean Six Sigma Green Belt | |

<div align="left">

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" />
<img src="https://img.shields.io/badge/dbt-FF694B?style=flat-square&logo=dbt&logoColor=white" />
<img src="https://img.shields.io/badge/DuckDB-FFF000?style=flat-square&logo=duckdb&logoColor=black" />
<img src="https://img.shields.io/badge/Airflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white" />
<img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white" />
<img src="https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" />
<img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
<img src="https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black" />
<img src="https://img.shields.io/badge/QGIS-589632?style=flat-square&logo=qgis&logoColor=white" />
<img src="https://img.shields.io/badge/Claude-D97757?style=flat-square&logo=anthropic&logoColor=white" />

</div>

---

## Open To

**Senior Data Analyst · Data Engineer · Analytics Engineer**

Remote · Hybrid — National & International

---

## Projects

*Projects in progress — each documented with context, architecture and technical decisions.*

### 01 · ETL/ELT Pipeline for Environmental Data
`Python` `dbt` `PostgreSQL` `Power BI`
Ingestion and transformation of public environmental data (air quality / climate / water resources), with dimensional modeling and analytical dashboard.
📁 [Repository](https://github.com/amanda-martins-data/pipeline-qualidade-ar)

---

### 02 · Pipeline Orchestration with Airflow
`Airflow` `Python` `Docker`
Production-grade pipeline orchestration: scheduling, retries, failure alerts and task dependencies.
📁 [Repository](https://github.com/amanda-martins-data/orquestracao-airflow-qualidade-ar)

---

### 03 · Medallion Architecture (Bronze/Silver/Gold)
`Data Lake` `Parquet` `ADR`
Layered data lake with documented architectural decisions (ADRs) on partitioning, file formats and schema evolution.
📁 [Repository](https://github.com/amanda-martins-data/arquitetura-medallion-qualidade-ar)

---

### 04 · Infrastructure as Code for a Cloud Pipeline
`Terraform` `AWS/GCP` `IaC`
Data pipeline provisioned via Terraform: storage, serverless function and managed database versioned as code.
📁 [Repository](https://github.com/amanda-martins-data/iac-pipeline-cloud-qualidade-ar)

---

### 05 · AI-Integrated Pipeline
`Claude` `LLMs` `Data Quality`
AI agent applied to data quality checks and automatic pipeline documentation generation.
📁 [Repository](https://github.com/amanda-martins-data/ai-pipeline-qualidade-ar)

---

### 06 · Data Observability & Quality
`dbt tests` `Great Expectations` `Monitoring`
Data tests and monitoring dashboard for quality and freshness across the pipelines above.
📁 [Repository](https://github.com/amanda-martins-data/observabilidade-qualidade-ar)

---

### 07 · Architecture Decision Records
`ADR` `System Design` `Data Governance`
Formal ADRs documenting the architecture trade-offs behind the pipelines above, plus prospective decisions on modeling, schema evolution and streaming.
📁 [Repository](https://github.com/amanda-martins-data/adr-arquitetura-dados)

---

### 08 · Data Governance & Catalog
`Governance` `Data Catalog` `LGPD`
Governance framework (roles, RACI, retention policy, LGPD-mapped classification) plus a working data catalog that validates YAML dataset definitions and renders lineage across the pipelines above.
📁 [Repository](https://github.com/amanda-martins-data/governanca-catalogo-dados)

---

### 09 · Corporate Data Architecture Blueprint
`System Design` `Star Schema` `Multi-tenant`
Full architecture document (conceptual, logical, physical models, NFRs, DR) for a fictional multi-tenant environmental monitoring org - no code, the kind of deliverable produced before implementation starts.
📁 [Repository](https://github.com/amanda-martins-data/blueprint-arquitetura-corporativa)

---

### 10 · Capacity Planning & Cost Model
`Scalability` `AWS Cost` `Capacity Planning`
Tested cost and capacity model for the real Project 04 infrastructure - exact breakpoint (Lambda timeout at 45.2x baseline volume) computed algebraically, not guessed, with a prioritized re-architecture plan.
📁 [Repository](https://github.com/amanda-martins-data/capacity-planning-qualidade-ar)

---

### 11 · Data Security & Access Architecture
`RBAC` `PII Masking` `Audit Trail`
Tested RBAC engine applying the Project 08 catalog's roles and sensitivity levels - PII masking as a second, independent defense layer plus an append-only audit log.
📁 [Repository](https://github.com/amanda-martins-data/seguranca-acesso-dados)

---

### 12 · Event-Driven Architecture (Streaming)
`Kafka-style` `Schema Registry` `Event-Driven`
Tested schema registry (backward/forward/full compatibility) and in-memory event bus (partitioning, ordering, at-least-once delivery), comparing batch vs streaming latency on the real Project 10 baseline.
📁 [Repository](https://github.com/amanda-martins-data/streaming-qualidade-ar)

---

### 13 · Multi-Source Environmental Pipeline
`Entity Resolution` `Dirty Data` `Data Integration`
Real, dirty public data from three sources (INMET weather, CETESB air quality via OpenAQ, IBGE) joined on the municipality dimension - 5M+ rows of latin-1 CSVs, and a tested layered resolver built on the finding that 9.4% of Brazilian municipalities cannot be identified by name alone.
[Repository](https://github.com/amanda-martins-data/pipeline-multi-fonte-ambiental)

---

## Contact

<div align="left">

<a href="https://www.linkedin.com/in/amandamartinsdts/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="mailto:amanda_mdantas@outlook.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>

</div>
