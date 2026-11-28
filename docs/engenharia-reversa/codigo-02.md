# Mapa de código — lote 02

Árvore Git e leitura amostral de um arquivo por projeto; sem execução.

## arduino-lab

[Repositório](https://github.com/juniordev830/arduino-lab) · árvore `043d3344e43af312acbced63cd5bc6ada44683f5`

- Código (7 arquivos filtrados): `experiments/blink/blink.ino`, `experiments/button-debounce/button-debounce.ino`, `experiments/button-debounce/debounce.c`, `experiments/button-debounce/debounce.h`, `experiments/serial-blink/serial-blink.ino`, `experiments/serial-blink/timing.h`, `tools/debounce_sim.c`.
- Build/dependências: não identificado por padrão textual.
- Arquivo lido: [tools/debounce_sim.c](https://github.com/juniordev830/arduino-lab/blob/main/tools/debounce_sim.c) · blob `ac176729a4be`.
- Declarações: não identificado por padrão textual.
- Imports: `errno.h`, `inttypes.h`, `stdint.h`, `stdio.h`, `stdlib.h`, `string.h`, `../experiments/button-debounce/debounce.h`.
- Rotas literais: não identificado por padrão textual.
- Persistência/modelagem (nomes candidatos): não identificado por padrão textual.
- Segurança/validação (nomes candidatos): não identificado por padrão textual.
- Testes (2 arquivos por convenção): `tests/debounce_test.c`, `tests/serial_blink_test.cpp`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/portfolio-checks.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## atlas-biblico-digital

[Repositório](https://github.com/juniordev830/atlas-biblico-digital) · árvore `e052d287ccdc787a2bbb904858817594d610922a`

- Código (5 arquivos filtrados): `src/App.tsx`, `src/Map.tsx`, `src/main.tsx`, `src/places.ts`, `vite.config.ts`.
- Build/dependências: `package.json`.
- Arquivo lido: [src/App.tsx](https://github.com/juniordev830/atlas-biblico-digital/blob/main/src/App.tsx) · blob `0b497f62e335`.
- Declarações: `App`, `focus`.
- Imports: `react`, `./Map.tsx`, `./places.ts`.
- Rotas literais: não identificado por padrão textual.
- Persistência/modelagem (nomes candidatos): não identificado por padrão textual.
- Segurança/validação (nomes candidatos): não identificado por padrão textual.
- Testes (1 arquivos por convenção): `tests/atlas.test.ts`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## auth-service-go

[Repositório](https://github.com/juniordev830/auth-service-go) · árvore `8acafda942be3262cda46ee3d885f9733cb96aae`

- Código (4 arquivos filtrados): `authorization.go`, `http_authorization.go`, `main.go`, `middleware.go`.
- Build/dependências: `go.mod`.
- Arquivo lido: [main.go](https://github.com/juniordev830/auth-service-go/blob/main/main.go) · blob `dc136bafb7f7`.
- Declarações: `TokenClaim`, `jwtHeader`, `jwtPayload`, `validateSecret`, `GenerateToken`, `TokenFingerprint`, `GenerateJWT`, `VerifyJWT`, `ValidateToken`, `main`.
- Imports: não identificado por padrão textual.
- Rotas literais: não identificado por padrão textual.
- Persistência/modelagem (nomes candidatos): não identificado por padrão textual.
- Segurança/validação (nomes candidatos): `authorization.go`, `http_authorization.go`, `middleware.go`.
- Testes (4 arquivos por convenção): `authorization_test.go`, `http_authorization_test.go`, `main_test.go`, `middleware_test.go`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/seguranca-workflows.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## auxiliar-NF-pj

[Repositório](https://github.com/juniordev830/auxiliar-NF-pj) · árvore `989c29ccae7449a640aad300dd9b6e7aea55783d`

- Código (17 arquivos filtrados): `ControladorGastos/Data/ControladorGastosContext.cs`, `ControladorGastos/Models/Pessoa.cs`, `ControladorGastos/Models/Transacao.cs`, `ControladorGastos/PJ/ApiCredentials.cs`, `ControladorGastos/PJ/AuxiliarPjContext.cs`, `ControladorGastos/PJ/AuxiliarPjEndpoints.cs`, `ControladorGastos/PJ/CredentialRevocations.cs`, `ControladorGastos/Program.cs`, `ControladorGastos/wwwroot/js/app.js`, `ControladorGastos/wwwroot/js/utils.js`, `relatorios/gerar_relatorio.py`, `scripts/backup_crypto.py`, `scripts/backup_sqlite.py`, `swift-client/Package.swift`, `swift-client/Sources/GastosCLI/main.swift`, `swift-client/Sources/GastosClient/GastosClient.swift`, `swift-client/Sources/GastosClient/TransactionCSV.swift`.
- Build/dependências: `ControladorGastos/ControladorGastos.csproj`, `relatorios/requirements.txt`, `scripts/requirements-backup.txt`.
- Arquivo lido: [ControladorGastos/Program.cs](https://github.com/juniordev830/auxiliar-NF-pj/blob/main/ControladorGastos/Program.cs) · blob `30061b5c6cb9`.
- Declarações: `PessoaInput`, `TransacaoInput`.
- Imports: `ControladorGastos.Data`, `ControladorGastos.Models`, `ControladorGastos.PJ`, `Microsoft.EntityFrameworkCore`, `System.Security.Cryptography`, `System.Text`.
- Rotas literais: `GET /api/health`, `GET /api/pessoas`, `POST /api/pessoas`, `DELETE /api/pessoas/{id:int}`, `GET /api/transacoes`, `POST /api/transacoes`, `GET /api/transacoes/totais/mensal`, `GET /api/transacoes/totais/resumo`.
- Persistência/modelagem (nomes candidatos): `ControladorGastos/Data/Migrations/20261119050108_BaselineResidencial.Designer.cs`, `ControladorGastos/Data/Migrations/20261119050108_BaselineResidencial.cs`, `ControladorGastos/Data/Migrations/ControladorGastosContextModelSnapshot.cs`, `ControladorGastos/Models/Pessoa.cs`, `ControladorGastos/Models/Transacao.cs`, `ControladorGastos/PJ/Migrations/20261119050114_BaselineAuxiliarPj.Designer.cs`, `ControladorGastos/PJ/Migrations/20261119050114_BaselineAuxiliarPj.cs`, `ControladorGastos/PJ/Migrations/20261125010000_AuditoriaPj.cs`, `ControladorGastos/PJ/Migrations/20261127010000_CredenciaisPj.cs`, `ControladorGastos/PJ/Migrations/AuxiliarPjContextModelSnapshot.cs`.
- Segurança/validação (nomes candidatos): `ControladorGastos/PJ/ApiCredentials.cs`, `ControladorGastos/PJ/CredentialRevocations.cs`.
- Testes (10 arquivos por convenção): `relatorios/tests/test_chart_edge_cases.py`, `relatorios/tests/test_csv_pj.py`, `relatorios/tests/test_gerar_relatorio.py`, `relatorios/tests/test_precisao.py`, `swift-client/Tests/GastosClientTests/GastosClientTests.swift`, `swift-client/Tests/GastosClientTests/TransactionCSVTests.swift`, `tests/frontend.test.cjs`, `tests/test_backup_sqlite.py`, `tests/test_pj_audit.py`, `tests/test_sqlite_upgrade.py`.
- CI: `.github/workflows/backup.yml`, `.github/workflows/ci.yml`, `.github/workflows/frontend.yml`, `.github/workflows/report-precision.yml`, `.github/workflows/swift-client.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## biblia-plano-de-leitura

[Repositório](https://github.com/juniordev830/biblia-plano-de-leitura) · árvore `2e8c03adb245f7431b52a177cfbeace273c689ac`

- Código (8 arquivos filtrados): `src/App.tsx`, `src/backup.ts`, `src/canon.ts`, `src/dates.ts`, `src/main.tsx`, `src/plan.ts`, `src/storage.ts`, `vite.config.ts`.
- Build/dependências: `package.json`.
- Arquivo lido: [src/App.tsx](https://github.com/juniordev830/biblia-plano-de-leitura/blob/main/src/App.tsx) · blob `e397e11b4982`.
- Declarações: `App`, `updatePlan`, `chooseDay`, `toggleReading`, `exportData`, `importData`.
- Imports: `react`, `./backup.ts`, `./dates.ts`, `./plan.ts`, `./storage.ts`.
- Rotas literais: não identificado por padrão textual.
- Persistência/modelagem (nomes candidatos): `src/storage.ts`.
- Segurança/validação (nomes candidatos): não identificado por padrão textual.
- Testes (2 arquivos por convenção): `tests/backup.test.ts`, `tests/plan.test.ts`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## bike-care

[Repositório](https://github.com/juniordev830/bike-care) · árvore `387d98f6cb0e923b9c15f16f0b94d16b4b3eb34d`

- Código (2 arquivos filtrados): `BikeCare.kt`, `Main.kt`.
- Build/dependências: não identificado por padrão textual.
- Arquivo lido: [Main.kt](https://github.com/juniordev830/bike-care/blob/main/Main.kt) · blob `d8f4d44fa732`.
- Declarações: não identificado por padrão textual.
- Imports: `java.io.File`.
- Rotas literais: não identificado por padrão textual.
- Persistência/modelagem (nomes candidatos): não identificado por padrão textual.
- Segurança/validação (nomes candidatos): não identificado por padrão textual.
- Testes (1 arquivos por convenção): `BikeCareTests.kt`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## caderno-offline

[Repositório](https://github.com/juniordev830/caderno-offline) · árvore `7d85c52c4f75d7a18ff78285673fe93f8d41ceac`

- Código (0 arquivos filtrados): não identificado por padrão textual.
- Build/dependências: não identificado por padrão textual.
- Arquivo lido: nenhum.
- Declarações: não identificado por padrão textual.
- Imports: não identificado por padrão textual.
- Rotas literais: não identificado por padrão textual.
- Persistência/modelagem (nomes candidatos): não identificado por padrão textual.
- Segurança/validação (nomes candidatos): não identificado por padrão textual.
- Testes (0 arquivos por convenção): não identificado por padrão textual.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## candidaturas-tracker

[Repositório](https://github.com/juniordev830/candidaturas-tracker) · árvore `ddf099d306612c18a74397aa5e32519cdd1ecc2d`

- Código (5 arquivos filtrados): `cli/tracker.php`, `main.php`, `src/Applications.php`, `src/CsvExporter.php`, `src/Storage.php`.
- Build/dependências: não identificado por padrão textual.
- Arquivo lido: [main.php](https://github.com/juniordev830/candidaturas-tracker/blob/main/main.php) · blob `43afb4870f8e`.
- Declarações: `transition`, `expect`.
- Imports: não identificado por padrão textual.
- Rotas literais: não identificado por padrão textual.
- Persistência/modelagem (nomes candidatos): `src/Storage.php`.
- Segurança/validação (nomes candidatos): não identificado por padrão textual.
- Testes (2 arquivos por convenção): `tests/ApplicationsTest.php`, `tests/CliTest.php`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## catalogo-comentarios-biblicos

[Repositório](https://github.com/juniordev830/catalogo-comentarios-biblicos) · árvore `c8358271d9c0c94682e47e90da08c37492658b68`

- Código (2 arquivos filtrados): `app.py`, `relatorio_csv.py`.
- Build/dependências: não identificado por padrão textual.
- Arquivo lido: [app.py](https://github.com/juniordev830/catalogo-comentarios-biblicos/blob/main/app.py) · blob `c06876512483`.
- Declarações: `texto`, `textos`, `chave`, `url_editora`, `run`, `objeto_sem_campos_repetidos`, `rejeitar_constante_json`, `main`.
- Imports: `unicodedata`, `urllib.parse`, `argparse`, `contextlib`, `sys`, `relatorio_csv`, `json`, `pathlib`.
- Rotas literais: não identificado por padrão textual.
- Persistência/modelagem (nomes candidatos): não identificado por padrão textual.
- Segurança/validação (nomes candidatos): não identificado por padrão textual.
- Testes (5 arquivos por convenção): `test_app.py`, `test_json_size_limit.py`, `test_saida_csv.py`, `test_stdin.py`, `test_validation.py`.
- CI: `.github/workflows/testes.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.

