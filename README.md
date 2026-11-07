**Português** | [English](README.en.md)

<p align="center"><img src="assets/hero-pt.svg" width="860" alt="Amanda Martins, Engenharia de Dados e Analytics Engineering" /></p>

<p align="center">
<a href="https://www.linkedin.com/in/amandamartinsdts/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="mailto:amanda_mdantas@outlook.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
</p>

Profissional de dados desde 2020, pós-graduada em Arquitetura de Dados (PUC Minas). Hoje construo pipelines em produção com Python e SQL no Azure, com deploy automatizado e decisões de arquitetura documentadas. Busco posições de **Engenharia de Dados** ou **Analytics Engineering**, remotas ou híbridas.

## 01 / Resultados

**Na CPEA** · Analista de Dados Pleno, Engenharia de Dados (out/2025 – atual)

- **5 áreas de negócio atendidas** por pipelines em Python que integram APIs REST (incluindo ArcGIS) ao ADLS Gen2 e à camada analítica em DuckDB e SQL.
- **30% menos tempo de execução** em um dos processos, ao converter um fluxo manual em planilhas em pipeline via API REST, gravando na camada bronze.
- **Zero segredos nos repositórios:** deploy com GitHub Actions e federação de identidade (OIDC); aplicações em Docker no Azure Container Apps, com Key Vault e Entra ID.
- **Aplicações de dados ponta a ponta:** bancos PostgreSQL com migrações versionadas e auditadas, APIs em FastAPI e integração com interfaces web.
- **Organização e governança:** estruturação do roadmap da equipe de dados no Azure DevOps; políticas de uso de IA, mapeamento de riscos e automações com IA (OCR e geração de relatórios).

**Antes** · Análise de dados (2020 – 2025)

- Dashboards e frameworks de KPIs em Power BI para operação, vendas e metas corporativas, em setores como educação, aviação e mobilidade.
- Ciclo de vida completo dos dados para relatórios corporativos anuais: coleta, validação, qualidade e entrega analítica.
- Análises estatísticas e apresentações para liderança, comitês internos e clientes; certificação Lean Six Sigma Green Belt (2024).

**No portfólio público**

- **5.025.594 linhas reais** de três fontes públicas (INMET, IBGE e CETESB) unidas por município.
- **100% de resolução de entidades** com nome e UF, após identificar que 9,4% dos municípios não são alcançáveis só pelo nome.
- **13 projetos publicados, 11 com CI** no GitHub Actions; decisões registradas em ADRs, com alternativas e gatilho de revisão.

## 02 / Projetos em destaque

| Projeto | Problema | Resultado |
|---|---|---|
| [13 · Pipeline multi-fonte](https://github.com/amanda-martins-data/pipeline-multi-fonte-dados-publicos) | Três fontes públicas com chaves que não casam | 5M+ linhas unidas por município; 100% de resolução com nome e UF |
| [03 · Arquitetura Medallion](https://github.com/amanda-martins-data/arquitetura-medallion-qualidade-ar) | Reprocessar sem duplicar dados | Bronze/Silver/Gold em Parquet com dbt; reexecução gera o mesmo resultado |
| [02 · Orquestração com Airflow](https://github.com/amanda-martins-data/orquestracao-airflow-qualidade-ar) | Pipeline manual e sem tolerância a falhas | Agendamento, retries com backoff e alertas; troca de fonte sem redeploy |
| [04 · IaC na AWS](https://github.com/amanda-martins-data/iac-pipeline-cloud-qualidade-ar) | Infraestrutura criada à mão | Lambda, S3 e RDS versionados em Terraform |
| [10 · Capacity planning](https://github.com/amanda-martins-data/capacity-planning-qualidade-ar) | Saber quando a arquitetura quebra | Ponto de ruptura calculado em 45,2x o volume atual; 14/14 testes |
| [11 · Segurança e acesso](https://github.com/amanda-martins-data/seguranca-acesso-dados) | Controle de acesso a dados sensíveis | RBAC testado, mascaramento de PII e trilha de auditoria |

<details>
<summary><b>Todos os 13 projetos</b></summary>

| # | Projeto | Entrega |
|---|---|---|
| 01 | [Pipeline ELT com dbt](https://github.com/amanda-martins-data/pipeline-qualidade-ar) | Ingestão de API pública, modelo dimensional e testes declarativos |
| 02 | [Orquestração com Airflow](https://github.com/amanda-martins-data/orquestracao-airflow-qualidade-ar) | DAG com retries, alertas e ramificação |
| 03 | [Arquitetura Medallion](https://github.com/amanda-martins-data/arquitetura-medallion-qualidade-ar) | Camadas Bronze/Silver/Gold em Parquet |
| 04 | [IaC na AWS](https://github.com/amanda-martins-data/iac-pipeline-cloud-qualidade-ar) | Lambda, S3 e RDS em Terraform |
| 05 | [Pipeline com IA](https://github.com/amanda-martins-data/ai-pipeline-qualidade-ar) | Agentes de IA para qualidade e documentação de dados |
| 06 | [Observabilidade](https://github.com/amanda-martins-data/observabilidade-qualidade-ar) | Great Expectations e checagens de frescor e completude |
| 07 | [ADRs](https://github.com/amanda-martins-data/adr-arquitetura-dados) | Decisões de arquitetura com alternativas e gatilho de revisão |
| 08 | [Governança e catálogo](https://github.com/amanda-martins-data/governanca-catalogo-dados) | RACI, retenção, classificação LGPD e catálogo com linhagem |
| 09 | [Blueprint corporativo](https://github.com/amanda-martins-data/blueprint-arquitetura-corporativa) | Modelos conceitual, lógico e físico e requisitos não funcionais |
| 10 | [Capacity planning](https://github.com/amanda-martins-data/capacity-planning-qualidade-ar) | Ruptura a 10x e 100x, com modelo de custo testado |
| 11 | [Segurança e acesso](https://github.com/amanda-martins-data/seguranca-acesso-dados) | RBAC, mascaramento de PII e auditoria |
| 12 | [Streaming](https://github.com/amanda-martins-data/streaming-qualidade-ar) | Schema registry e event bus com garantias testadas |
| 13 | [Pipeline multi-fonte](https://github.com/amanda-martins-data/pipeline-multi-fonte-dados-publicos) | Três fontes públicas unidas com resolução de entidades |

</details>

## 03 / Stack

<p align="center"><img src="assets/stack-pt.svg" width="860" alt="Stack: Python, SQL, PostgreSQL, dbt, DuckDB, Airflow, Great Expectations, pytest, GitHub Actions, Azure (ADLS Gen2, Container Apps, Key Vault, Entra ID), Terraform, Docker, AWS, FastAPI, Power BI, Claude" /></p>

## 04 / Em construção

- **Lakehouse no Azure como código:** ADLS Gen2, Databricks e Unity Catalog em Terraform, com jobs PySpark e Delta Lake.
- **Dados para IA:** pipeline de RAG e servidor MCP sobre a camada Gold, com o controle de acesso do Projeto 11.

---

<p align="center">
<a href="https://www.linkedin.com/in/amandamartinsdts/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="mailto:amanda_mdantas@outlook.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
</p>

<p align="center"><sub>Amanda Martins · layout inspirado no template <a href="https://www.gitskins.com/readme-generator?template=community-builder-s-workbench-city-edition-9udn">Builder’s Workbench — City Edition</a>, de <a href="https://www.gitskins.com/creators/pengusto">@pengusto</a> no GitSkins</sub></p>
