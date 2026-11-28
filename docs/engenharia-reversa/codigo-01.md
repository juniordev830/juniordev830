# Mapa de código — lote 01

Árvore Git e leitura amostral de um arquivo de código por repositório; extração de declarações, imports, rotas e evidências de testes. Sem execução.

## 2d-platformer-csharp

[Repositório](https://github.com/juniordev830/2d-platformer-csharp) · árvore Git `0d5f1af4ba7bd5a8b3f25b0b93fcd4c9946d11f7`.

- **Código:** 5 arquivos por extensão e filtros; principais: `GameSimulation.cs`, `Player.cs`, `Program.cs`, `Rect.cs`, `Vector2D.cs`.
- **Build e dependências:** `PlatformerGame.csproj`, `tests/PlatformerGame.Tests/PlatformerGame.Tests.csproj`.
- **Arquivo lido:** [Program.cs](https://github.com/juniordev830/2d-platformer-csharp/blob/main/Program.cs) · blob `077c4710df31`.
- **Declarações encontradas:** `PlatformerGame`, `Program`.
- **Imports detectados:** `System`.
- **Rotas literais detectadas:** não detectadas nesta amostra.
- **Persistência/modelagem (nomes candidatos):** não identificada por nome.
- **Segurança/validação (nomes candidatos):** não identificada por nome.
- **Testes:** 2; `tests/PlatformerGame.Tests/JumpBufferTests.cs`, `tests/PlatformerGame.Tests/PhysicsTests.cs`.
- **CI:** `.github/workflows/ci.yml`, `.github/workflows/seguranca-workflows.yml`.

As referências a módulos, imports e rotas são evidências estáticas. Não indicam que todos os caminhos foram analisados nem que os testes passaram.


---

## acessibilidade-checklist

[Repositório](https://github.com/juniordev830/acessibilidade-checklist) · árvore Git `08a768470c4b054bace6294c30cd3d92e5c88e9b`.

- **Código:** 6 arquivos por extensão e filtros; principais: `src/analytics.ts`, `src/cli.ts`, `src/compare.ts`, `src/history.ts`, `src/remediation.ts`, `src/report.ts`.
- **Build e dependências:** `package.json`.
- **Arquivo lido:** [src/cli.ts](https://github.com/juniordev830/acessibilidade-checklist/blob/main/src/cli.ts) · blob `009681200abd`.
- **Declarações encontradas:** `parseInteger`, `readAssessment`, `main`.
- **Imports detectados:** `./report`, `./analytics`, `./compare`, `./history`, `./remediation`.
- **Rotas literais detectadas:** não detectadas nesta amostra.
- **Persistência/modelagem (nomes candidatos):** não identificada por nome.
- **Segurança/validação (nomes candidatos):** não identificada por nome.
- **Testes:** 7; `tests/analytics.test.cjs`, `tests/cli.test.cjs`, `tests/compare.test.cjs`, `tests/history.test.cjs`, `tests/remediation.test.cjs`, `tests/report.test.cjs`, `tests/workflow.test.cjs`.
- **CI:** `.github/workflows/ci.yml`.

As referências a módulos, imports e rotas são evidências estáticas. Não indicam que todos os caminhos foram analisados nem que os testes passaram.


---

## achados-perdidos

[Repositório](https://github.com/juniordev830/achados-perdidos) · árvore Git `38a2e84a633f22d1b1bae2f926c735ee8fcfd8a4`.

- **Código:** 6 arquivos por extensão e filtros; principais: `main.php`, `operations.php`, `reports.php`, `src/CatalogReports.php`, `src/Operations.php`, `src/ReturnReceipt.php`.
- **Build e dependências:** não identificados por nome.
- **Arquivo lido:** [main.php](https://github.com/juniordev830/achados-perdidos/blob/main/main.php) · blob `a1f711c51d60`.
- **Declarações encontradas:** `dateIsValid`, `items`, `addFound`, `markReturned`, `pending`, `readData`, `saveData`, `updateDataFile`, `selfTest`.
- **Imports detectados:** não detectados pelo padrão textual.
- **Rotas literais detectadas:** não detectadas nesta amostra.
- **Persistência/modelagem (nomes candidatos):** não identificada por nome.
- **Segurança/validação (nomes candidatos):** não identificada por nome.
- **Testes:** 5; `tests/ConcurrentWritesTest.php`, `tests/OperationsCliTest.php`, `tests/OperationsTest.php`, `tests/ReportsTest.php`, `tests/return_receipt_test.php`.
- **CI:** `.github/workflows/ci.yml`.

As referências a módulos, imports e rotas são evidências estáticas. Não indicam que todos os caminhos foram analisados nem que os testes passaram.


---

## agenda-servicos

[Repositório](https://github.com/juniordev830/agenda-servicos) · árvore Git `43fb8a403d03d6edabb8301f19fb2b9add3d4e66`.

- **Código:** 8 arquivos por extensão e filtros; principais: `src/main/java/br/junior/agendamentos/AgendaProfissionais.java`, `src/main/java/br/junior/agendamentos/AgendaService.java`, `src/main/java/br/junior/agendamentos/Agendamento.java`, `src/main/java/br/junior/agendamentos/CalendarioTrabalho.java`, `src/main/java/br/junior/agendamentos/CatalogoServicos.java`, `src/main/java/br/junior/agendamentos/Intervalo.java`, `src/main/java/br/junior/agendamentos/RelatoriosAgenda.java`, `src/main/java/br/junior/agendamentos/Servico.java`.
- **Build e dependências:** `pom.xml`.
- **Arquivo lido:** [src/main/java/br/junior/agendamentos/AgendaService.java](https://github.com/juniordev830/agenda-servicos/blob/main/src/main/java/br/junior/agendamentos/AgendaService.java) · blob `62158c39e3c0`.
- **Declarações encontradas:** `AgendaService`.
- **Imports detectados:** `java.time.LocalDate`, `java.time.LocalDateTime`, `java.util.ArrayList`, `java.util.Comparator`, `java.util.List`, `java.util.Objects`.
- **Rotas literais detectadas:** não detectadas nesta amostra.
- **Persistência/modelagem (nomes candidatos):** não identificada por nome.
- **Segurança/validação (nomes candidatos):** não identificada por nome.
- **Testes:** 5; `src/test/java/br/junior/agendamentos/AgendaProfissionaisTest.java`, `src/test/java/br/junior/agendamentos/AgendaServiceConcorrenciaTest.java`, `src/test/java/br/junior/agendamentos/AgendaServiceTest.java`, `src/test/java/br/junior/agendamentos/CatalogoCalendarioTest.java`, `src/test/java/br/junior/agendamentos/RelatoriosAgendaTest.java`.
- **CI:** `.github/workflows/ci.yml`, `.github/workflows/revisao-dependencias.yml`.

As referências a módulos, imports e rotas são evidências estáticas. Não indicam que todos os caminhos foram analisados nem que os testes passaram.


---

## ai-incident-analyzer

[Repositório](https://github.com/juniordev830/ai-incident-analyzer) · árvore Git `71d4da3bc1427627b09f8ac7983425e6a8ff3bec`.

- **Código:** 3 arquivos por extensão e filtros; principais: `analyzer.py`, `incident_cli.py`, `incident_engine.py`.
- **Build e dependências:** não identificados por nome.
- **Arquivo lido:** [incident_engine.py](https://github.com/juniordev830/ai-incident-analyzer/blob/main/incident_engine.py) · blob `8d435e3169c6`.
- **Declarações encontradas:** `AnalysisConfig`, `validate`, `Event`, `Rejection`, `Incident`, `AnalysisReport`, `as_dict`, `severity_counts`, `has_incidents`, `parse_timestamp`, `parse_event`, `quantile`, `baseline`, `score_latency`, `incident_identifier`, `service_summary`, `analyze_incidents`, `render_summary`, `render_markdown`, `render_sarif`.
- **Imports detectados:** `__future__`, `collections`, `dataclasses`, `datetime`, `hashlib`, `math`, `statistics`, `typing`.
- **Rotas literais detectadas:** não detectadas nesta amostra.
- **Persistência/modelagem (nomes candidatos):** não identificada por nome.
- **Segurança/validação (nomes candidatos):** não identificada por nome.
- **Testes:** 5; `tests/test_analyzer.py`, `tests/test_incident_cli.py`, `tests/test_incident_engine.py`, `tests/test_strict_jsonl.py`, `tests/test_threshold_cli.py`.
- **CI:** `.github/workflows/ci.yml`.

As referências a módulos, imports e rotas são evidências estáticas. Não indicam que todos os caminhos foram analisados nem que os testes passaram.


---

## ai-service-python

[Repositório](https://github.com/juniordev830/ai-service-python) · árvore Git `ff7c170c5da9daa5e9f438df4137083a8f0c590e`.

- **Código:** 2 arquivos por extensão e filtros; principais: `src/main.py`, `src/report.py`.
- **Build e dependências:** `requirements.txt`.
- **Arquivo lido:** [src/main.py](https://github.com/juniordev830/ai-service-python/blob/main/src/main.py) · blob `cea05fa1c817`.
- **Declarações encontradas:** `analyze_text`, `batch_analyze`.
- **Imports detectados:** `re`, `unicodedata`, `typing`.
- **Rotas literais detectadas:** não detectadas nesta amostra.
- **Persistência/modelagem (nomes candidatos):** não identificada por nome.
- **Segurança/validação (nomes candidatos):** não identificada por nome.
- **Testes:** 6; `tests/test_comparison.py`, `tests/test_csv_report.py`, `tests/test_main.py`, `tests/test_report.py`, `tests/test_sentiment_boundaries.py`, `tests/test_sentiment_regression.py`.
- **CI:** `.github/workflows/ci.yml`, `.github/workflows/portfolio-checks.yml`.

As referências a módulos, imports e rotas são evidências estáticas. Não indicam que todos os caminhos foram analisados nem que os testes passaram.


---

## airport-control-mini

[Repositório](https://github.com/juniordev830/airport-control-mini) · árvore Git `094fdcf6c4b26dbd7d4cb8f9ae941eb290657af4`.

- **Código:** 5 arquivos por extensão e filtros; principais: `scheduler.py`, `src/main.ts`, `src/rules.ts`, `src/scoring.ts`, `turns.py`.
- **Build e dependências:** `package.json`.
- **Arquivo lido:** [src/main.ts](https://github.com/juniordev830/airport-control-mini/blob/main/src/main.ts) · blob `e904eb667c85`.
- **Declarações encontradas:** `Aircraft`, `AirportScene`.
- **Imports detectados:** `phaser`, `./rules.js`, `./scoring.js`.
- **Rotas literais detectadas:** não detectadas nesta amostra.
- **Persistência/modelagem (nomes candidatos):** não identificada por nome.
- **Segurança/validação (nomes candidatos):** não identificada por nome.
- **Testes:** 5; `tests/rules.test.mjs`, `tests/scoring.test.mjs`, `tests/test_invalid_inputs.py`, `tests/test_scheduler.py`, `tests/test_turns.py`.
- **CI:** `.github/workflows/ci.yml`, `.github/workflows/phaser-simulator.yml`.

As referências a módulos, imports e rotas são evidências estáticas. Não indicam que todos os caminhos foram analisados nem que os testes passaram.


---

## api-test-studio

[Repositório](https://github.com/juniordev830/api-test-studio) · árvore Git `3a305b9d10dedb100365891e08c69707f1d8b656`.

- **Código:** 6 arquivos por extensão e filtros; principais: `src/assertions.js`, `src/cli.js`, `src/collection-cli.js`, `src/collection.js`, `src/report.js`, `src/test-api.js`.
- **Build e dependências:** `package.json`.
- **Arquivo lido:** [src/cli.js](https://github.com/juniordev830/api-test-studio/blob/main/src/cli.js) · blob `84af08c11330`.
- **Declarações encontradas:** nenhuma detectada pelo padrão textual.
- **Imports detectados:** `./test-api.js`, `node:util`.
- **Rotas literais detectadas:** não detectadas nesta amostra.
- **Persistência/modelagem (nomes candidatos):** não identificada por nome.
- **Segurança/validação (nomes candidatos):** não identificada por nome.
- **Testes:** 9; `tests/assertions.test.js`, `tests/collection-cli.test.js`, `tests/collection.test.js`, `tests/content-type.test.js`, `tests/duration.test.js`, `tests/options.test.js`, `tests/report.test.js`, `tests/target-validation.test.js`, `tests/test-api.test.js`.
- **CI:** `.github/workflows/ci.yml`.

As referências a módulos, imports e rotas são evidências estáticas. Não indicam que todos os caminhos foram analisados nem que os testes passaram.

