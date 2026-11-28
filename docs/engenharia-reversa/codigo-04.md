# Mapa de código — lote 04

Árvore Git e leitura amostral de um arquivo por projeto; sem execução.

## cyber-detective-noir

[Repositório](https://github.com/juniordev830/cyber-detective-noir) · árvore `6c466d98f3db283cb0f4b6fba60c11061ff5bc4a`

- Código (6 arquivos filtrados): `case_report.py`, `casebook.py`, `detective_cli.py`, `investigation.py`, `scripts/case_rules.gd`, `scripts/detective.gd`.
- Build/dependências: `project.godot`.
- Arquivo lido: [scripts/case_rules.gd](https://github.com/juniordev830/cyber-detective-noir/blob/main/scripts/case_rules.gd) · blob `24e7095bb5a3`.
- Declarações: `found_count`, `can_accuse`, `verdict`, `next_hint`, `missing_count`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (6 arquivos por convenção): `test_case_report.py`, `test_casebook.py`, `test_detective_cli.py`, `test_investigation.py`, `test_investigation_extended.py`, `tests/test_case_rules.gd`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/python-investigation.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## database-migration-auditor

[Repositório](https://github.com/juniordev830/database-migration-auditor) · árvore `8e9bce360f0b14e46db07fc38e037bc0cee113b9`

- Código (5 arquivos filtrados): `advanced_audit.py`, `audit.py`, `migration_plan.py`, `sql_lexer.py`, `sql_risk_engine.py`.
- Build/dependências: não detectado.
- Arquivo lido: [sql_risk_engine.py](https://github.com/juniordev830/database-migration-auditor/blob/main/sql_risk_engine.py) · blob `86d013305dcc`.
- Declarações: `Finding`, `__post_init__`, `Rule`, `_words`, `_has_pair`, `_where_is_unrestricted`, `classify`, `audit_sql`, `counts`, `should_fail`, `to_json`, `to_sarif`, `to_markdown`, `to_csv`, `summary`.
- Imports: `__future__`, `collections`, `dataclasses`, `csv`, `io`, `json`, `typing`, `sql_lexer`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): `examples/migration.sql`, `migration_plan.py`.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (6 arquivos por convenção): `tests/test_audit.py`, `tests/test_cli.py`, `tests/test_migration_plan.py`, `tests/test_size_limit.py`, `tests/test_sql_lexer.py`, `tests/test_sql_risk_engine.py`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## despensa-validades

[Repositório](https://github.com/juniordev830/despensa-validades) · árvore `4f61118dc6477c0bd23e41b8759409aff2b1eb9c`

- Código (6 arquivos filtrados): `src/cli.ts`, `src/expiry.ts`, `src/meal-plan.ts`, `src/pantry.ts`, `src/product-risk.ts`, `src/restock.ts`.
- Build/dependências: `package.json`.
- Arquivo lido: [src/cli.ts](https://github.com/juniordev830/despensa-validades/blob/main/src/cli.ts) · blob `fcbdf5a473c1`.
- Declarações: `readJson`, `Scenario`, `parseOptions`.
- Imports: `./pantry`, `./expiry`, `./restock`, `./meal-plan`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (5 arquivos por convenção): `tests/expiry.test.cjs`, `tests/meal-plan.test.cjs`, `tests/pantry.test.cjs`, `tests/product-risk.test.cjs`, `tests/restock.test.cjs`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## devops-control-center

[Repositório](https://github.com/juniordev830/devops-control-center) · árvore `486432f8da1f1397e02f4738a93c7851dd21bed2`

- Código (1 arquivos filtrados): `src/server.js`.
- Build/dependências: `package.json`.
- Arquivo lido: [src/server.js](https://github.com/juniordev830/devops-control-center/blob/main/src/server.js) · blob `563ccab1aeda`.
- Declarações: `createApp`.
- Imports: `node:http`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (2 arquivos por convenção): `tests/server.test.js`, `tests/summary.test.js`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## diario-devocional

[Repositório](https://github.com/juniordev830/diario-devocional) · árvore `77fbbddaa20ca4e34c1b86fe77217b565a0fccd5`

- Código (7 arquivos filtrados): `src/App.tsx`, `src/dates.ts`, `src/download.ts`, `src/journal.ts`, `src/main.tsx`, `src/storage.ts`, `vite.config.ts`.
- Build/dependências: `package.json`.
- Arquivo lido: [src/App.tsx](https://github.com/juniordev830/diario-devocional/blob/main/src/App.tsx) · blob `e4541c1d6a75`.
- Declarações: `App`, `edit`, `save`, `favorite`, `restore`.
- Imports: `react`, `./dates.ts`, `./download.ts`, `./journal.ts`, `./storage.ts`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): `src/storage.ts`.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (1 arquivos por convenção): `tests/journal.test.ts`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## diario-leitura

[Repositório](https://github.com/juniordev830/diario-leitura) · árvore `161de85419699dd1fb3afaa18d7d9ba4846f556a`

- Código (9 arquivos filtrados): `bin/demo.rb`, `bin/diario.rb`, `lib/reading_diary.rb`, `lib/reading_diary/analytics.rb`, `lib/reading_diary/catalog.rb`, `lib/reading_diary/cli.rb`, `lib/reading_diary/export.rb`, `lib/reading_diary/storage.rb`, `lib/reading_journal.rb`.
- Build/dependências: não detectado.
- Arquivo lido: [lib/reading_diary/cli.rb](https://github.com/juniordev830/diario-leitura/blob/main/lib/reading_diary/cli.rb) · blob `a722c0557df5`.
- Declarações: `run`, `dispatch`, `mutate`, `number`, `expect`, `expect_between`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): `lib/reading_diary/storage.rb`.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (7 arquivos por convenção): `test/reading_journal_test.rb`, `test/test_analytics.rb`, `test/test_catalog.rb`, `test/test_cli.rb`, `test/test_diary.rb`, `test/test_export.rb`, `test/test_storage.rb`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/ruby-reading-cli.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## distributed-task-queue

[Repositório](https://github.com/juniordev830/distributed-task-queue) · árvore `4b4e79a4c821d343cee5eba78f30e3075a7194bd`

- Código (4 arquivos filtrados): `src/main/java/dev/juniordev/ReliableTaskQueue.java`, `src/main/java/dev/juniordev/TaskQueue.java`, `src/main/java/dev/juniordev/TaskQueueReports.java`, `src/main/java/dev/juniordev/TaskQueueWorker.java`.
- Build/dependências: `pom.xml`.
- Arquivo lido: [src/main/java/dev/juniordev/TaskQueue.java](https://github.com/juniordev830/distributed-task-queue/blob/main/src/main/java/dev/juniordev/TaskQueue.java) · blob `90c81141f1bc`.
- Declarações: `TaskQueue`, `Job`, `Result`, `Stats`.
- Imports: `java.util.ArrayDeque`, `java.util.Objects`, `java.util.Queue`, `java.util.function.Predicate`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (3 arquivos por convenção): `src/test/java/dev/juniordev/ReliableTaskQueueTest.java`, `src/test/java/dev/juniordev/TaskQueueTest.java`, `src/test/java/dev/juniordev/TaskQueueWorkerReportsTest.java`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## divide-viagem

[Repositório](https://github.com/juniordev830/divide-viagem) · árvore `7e5bb3e85cf67bb95312cf14d77a3c9e970c5196`

- Código (2 arquivos filtrados): `Main.kt`, `TravelLedger.kt`.
- Build/dependências: não detectado.
- Arquivo lido: [Main.kt](https://github.com/juniordev830/divide-viagem/blob/main/Main.kt) · blob `007fc9ba78df`.
- Declarações: não detectado.
- Imports: `java.io.File`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (1 arquivos por convenção): `TravelLedgerTests.kt`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## documentos-validade

[Repositório](https://github.com/juniordev830/documentos-validade) · árvore `ccd1f924a2fdfce0236a82e0fceaa9e5a6bca713`

- Código (1 arquivos filtrados): `Main.kt`.
- Build/dependências: não detectado.
- Arquivo lido: [Main.kt](https://github.com/juniordev830/documentos-validade/blob/main/Main.kt) · blob `fa04a0ad72be`.
- Declarações: `class`.
- Imports: `java.io.File`, `java.nio.ByteBuffer`, `java.nio.charset.CodingErrorAction`, `java.nio.charset.StandardCharsets`, `java.nio.file.AtomicMoveNotSupportedException`, `java.nio.file.Files`, `java.nio.file.StandardCopyOption`, `java.time.LocalDate`, `java.time.format.DateTimeFormatter`, `java.time.temporal.ChronoUnit`, `java.util.UUID`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (1 arquivos por convenção): `Tests.kt`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.

