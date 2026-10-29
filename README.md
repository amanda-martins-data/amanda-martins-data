**Português** | [English](README.en.md)

<p align="center"><img src="assets/hero-pt.svg" width="860" alt="Amanda Martins, Engenharia e Arquitetura de Dados" /></p>

<p align="center">
<a href="https://www.linkedin.com/in/amandamartinsdts/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="mailto:amanda_mdantas@outlook.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
</p>

<p align="center"><img src="https://www.gitskins.com/api/section/city?username=amanda-martins-data&theme=retro" width="860" alt="Skyline de contribuições no GitHub" /></p>

## 01 / Em 30 segundos

```python
class AmandaMartins:
    def __init__(self):
        self.experience   = "6+ years in Data"
        self.role         = "Data Engineering & Architecture"
        self.focus_areas  = ["Data Pipelines", "Data Architecture", "Data for AI"]
        self.stack        = ["Python", "SQL", "dbt", "Airflow", "DuckDB", "Terraform", "Azure/AWS"]
        self.education    = "Post-Graduate in Data Architecture, PUC Minas"
```

| | |
|---|---|
| **O que eu faço** | Projeto e mantenho pipelines ELT, camadas de dados (Bronze/Silver/Gold) e a governança em volta delas |
| **Diferencial** | Registro em cada projeto as decisões que tomei, as limitações e o gatilho para revisá-las. Os erros que encontrei pelo caminho também ficam documentados |
| **Projetos** | 13 publicados. No mais recente trabalhei com dados públicos reais: 594 estações do INMET, 5.570 municípios do IBGE e leituras da CETESB |
| **Procuro** | Engenheira de Dados (Pleno) ou Analytics Engineer |

## 02 / Três pilares

<table>
<tr>
<td valign="top" width="33%"><h3>🏛 Arquitetura com decisões documentadas</h3>Solução proporcional ao estágio do problema, com o gatilho para mudar registrado.<br><br><sub>Projetos <a href="https://github.com/amanda-martins-data/adr-arquitetura-dados">07</a> · <a href="https://github.com/amanda-martins-data/blueprint-arquitetura-corporativa">09</a> · <a href="https://github.com/amanda-martins-data/capacity-planning-qualidade-ar">10</a></sub></td>
<td valign="top" width="33%"><h3>🧰 Pipelines confiáveis sobre fontes heterogêneas</h3>Orquestração, idempotência, testes de dados e resolução de entidades em dado sujo.<br><br><sub>Projetos <a href="https://github.com/amanda-martins-data/pipeline-qualidade-ar">01</a> · <a href="https://github.com/amanda-martins-data/orquestracao-airflow-qualidade-ar">02</a> · <a href="https://github.com/amanda-martins-data/arquitetura-medallion-qualidade-ar">03</a> · <a href="https://github.com/amanda-martins-data/pipeline-multi-fonte-dados-publicos">13</a></sub></td>
<td valign="top" width="33%"><h3>🚀 Dados para IA</h3>IA aplicada à checagem de qualidade de dados; RAG e servidor MCP sobre a camada Gold em construção.<br><br><sub>Projeto <a href="https://github.com/amanda-martins-data/ai-pipeline-qualidade-ar">05</a></sub></td>
</tr>
</table>

## 03 / Distrito de projetos

<p align="center"><img src="assets/projects-pt.svg" width="860" alt="Projetos em destaque" /></p>

### Pipelines e camadas de dados

| # | Projeto | O que entrega | Stack |
|---|---|---|---|
| 01 | [Pipeline ELT com dbt](https://github.com/amanda-martins-data/pipeline-qualidade-ar) | Ingestão do OpenAQ, modelagem dimensional e testes declarativos | `Python` `dbt` `DuckDB` |
| 02 | [Orquestração com Airflow](https://github.com/amanda-martins-data/orquestracao-airflow-qualidade-ar) | Agendamento, retries com backoff, alertas e ramificação sem redeploy | `Airflow` `Docker` |
| 03 | [Arquitetura Medallion](https://github.com/amanda-martins-data/arquitetura-medallion-qualidade-ar) | Bronze/Silver/Gold em Parquet, idempotência por reescrita de partição | `Parquet` `dbt` |
| 13 | [Pipeline multi-fonte](https://github.com/amanda-martins-data/pipeline-multi-fonte-dados-publicos) | INMET + IBGE + CETESB unidos por município, com resolução em camadas | `Python` `pytest` |

### Arquitetura, governança e segurança

| # | Projeto | O que entrega | Stack |
|---|---|---|---|
| 07 | [ADRs de arquitetura](https://github.com/amanda-martins-data/adr-arquitetura-dados) | Registro de decisões com contexto, alternativas e gatilho de revisão | `ADR` |
| 08 | [Governança e catálogo](https://github.com/amanda-martins-data/governanca-catalogo-dados) | Papéis, RACI, retenção e classificação com mapeamento à LGPD; catálogo gerado de YAML, com linhagem verificada | `Python` `YAML` |
| 09 | [Blueprint corporativo](https://github.com/amanda-martins-data/blueprint-arquitetura-corporativa) | Modelo conceitual, lógico e físico, fluxo de dados e requisitos não funcionais de uma organização fictícia, sem código | `Arquitetura` |
| 10 | [Capacity planning](https://github.com/amanda-martins-data/capacity-planning-qualidade-ar) | Onde cada componente da infraestrutura do Projeto 04 quebra a 10x e 100x, com modelo de custo testado e plano de re-arquitetura | `Python` |
| 11 | [Segurança e acesso](https://github.com/amanda-martins-data/seguranca-acesso-dados) | RBAC testado sobre o catálogo do Projeto 08, mascaramento de PII e trilha de auditoria | `Python` |

### Qualidade, IA e infraestrutura

| # | Projeto | O que entrega | Stack |
|---|---|---|---|
| 04 | [IaC para pipeline cloud](https://github.com/amanda-martins-data/iac-pipeline-cloud-qualidade-ar) | Lambda, S3 e RDS versionados como código | `Terraform` `AWS` |
| 05 | [Pipeline com IA integrada](https://github.com/amanda-martins-data/ai-pipeline-qualidade-ar) | Agente de IA para checagem de qualidade e documentação | `Claude` `LLMs` |
| 06 | [Observabilidade e qualidade](https://github.com/amanda-martins-data/observabilidade-qualidade-ar) | Testes de dados e monitoramento de qualidade | `Great Expectations` |
| 12 | [Streaming orientado a eventos](https://github.com/amanda-martins-data/streaming-qualidade-ar) | Schema registry e event bus em memória com garantias testadas, e modelo de latência batch vs streaming | `Python` |

<h3 align="center"><a href="https://github.com/amanda-martins-data?tab=repositories">Explorar os repositórios ↗</a></h3>

## 04 / Stack

<p align="center"><img src="assets/stack-pt.svg" width="860" alt="Stack do portfólio" /></p>

## 05 / Decisões técnicas em destaque

Cinco decisões que tomei, cada uma com o trade-off e o motivo registrados no repositório.

- **Parquet com dbt lendo e escrevendo os arquivos direto (Projeto 03).** O mesmo arquivo serve a DuckDB, Spark ou pandas sem reprocessar. Abri mão de índices e do controle de acesso nativo de um warehouse, e deixei o gatilho de revisão registrado.
- **Idempotência por reescrita de partição (Projeto 03).** Na Silver eu apago e reescrevo cada partição afetada, então rodar a transformação duas vezes dá o mesmo resultado. Esse método fica caro em volume alto, e o README do projeto registra isso.
- **Resolução de entidades em camadas (Projeto 13).** Descobri que 9,4% dos municípios não são alcançáveis só pelo nome. Resolvo da evidência mais forte para a mais fraca, e o que continua ambíguo vai para quarentena: 100% de resolução com nome e UF, 90,6% só com nome.
- **Streaming sem cluster (Projeto 12).** Na ADR 0010 decidi permanecer em batch. Para estar pronta quando um dos gatilhos aparecer, implementei e testei as garantias que importariam (particionamento, entrega at-least-once e compatibilidade de schema), sem provisionar Kafka.
- **Uma suposição errada minha (Projeto 11).** Um teste apontou que eu tinha entendido mal o papel `data_consumer` e os datasets internos. A falha estava no teste, e eu corrigi e documentei a semântica correta.

## 06 / Como ler meus repositórios

Em cada repositório descrevo o problema, a arquitetura e as limitações, e registro as decisões e as lacunas conhecidas. Há instruções para rodar do zero.

A integração contínua roda no GitHub Actions, com selo de status no README. Oito repositórios executam os testes a cada alteração (04, 05, 06, 08, 10, 11, 12 e 13), e três verificam a sintaxe do Python e rodam o `dbt parse` (01, 02 e 03). Os Projetos 07 e 09 são só documentação e ficam sem CI.

## 07 / Em construção

- **Dados para IA:** pipeline de RAG tratado como engenharia de dados (ingestão, chunking, índice com atualização incremental, qualidade da recuperação) e servidor MCP sobre a camada Gold, com o controle de acesso do Projeto 11.
- **Lakehouse em escala:** versão do Projeto 03 com Spark e formato de tabela Delta ou Iceberg, tratando schema evolution e compactação.
- **Azure e warehouse em nuvem:** infraestrutura do Projeto 04 em Azure e o mesmo modelo dbt rodando em BigQuery ou Snowflake.
- **Contratos de dados:** estender o contrato do catálogo (Projeto 08) para validar as fontes do Projeto 13.


---

<h2 align="center">O próximo bloco começa com uma conversa.</h2>

<p align="center">
<a href="https://www.linkedin.com/in/amandamartinsdts/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="mailto:amanda_mdantas@outlook.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
</p>

<p align="center"><sub>Amanda Martins · layout inspirado no template <a href="https://www.gitskins.com/readme-generator?template=community-builder-s-workbench-city-edition-9udn">Builder’s Workbench — City Edition</a>, de <a href="https://www.gitskins.com/creators/pengusto">@pengusto</a> no GitSkins</sub></p>
