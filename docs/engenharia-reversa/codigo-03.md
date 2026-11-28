# Mapa de código — lote 03

Árvore Git e leitura amostral de um arquivo por projeto; sem execução.

## catalogo-municipios

[Repositório](https://github.com/juniordev830/catalogo-municipios) · árvore `d3d2df1b901c40f3362e143dcad415659ea271f1`

- Código (3 arquivos filtrados): `catalog.php`, `main.php`, `src/Catalog.php`.
- Build/dependências: não detectado.
- Arquivo lido: [main.php](https://github.com/juniordev830/catalogo-municipios/blob/main/main.php) · blob `f6c8abba0bd1`.
- Declarações: `normalizeSearch`, `searchCities`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (1 arquivos por convenção): `tests/test_catalog.php`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## cifras-transpositor

[Repositório](https://github.com/juniordev830/cifras-transpositor) · árvore `b089923e17536af3da12f23c123b097e3c8f40c7`

- Código (3 arquivos filtrados): `src/main.rs`, `src/music.rs`, `src/songbook.rs`.
- Build/dependências: `Cargo.toml`.
- Arquivo lido: [src/main.rs](https://github.com/juniordev830/cifras-transpositor/blob/main/src/main.rs) · blob `ceaf39fda31e`.
- Declarações: `note`, `chord`, `bracketed_line`, `line`, `transpose`, `render`, `run`, `main`, `bom_does_not_hide_first_chord_or_directive`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (0 arquivos por convenção): não detectado.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## codax-assirtende-engenharia-ia-

[Repositório](https://github.com/juniordev830/codax-assirtende-engenharia-ia-) · árvore `b4335daa2ce0f5b7118baf9a5058db910f444a0f`

- Código (20 arquivos filtrados): `backend/app/__init__.py`, `backend/app/ai_code_review.py`, `backend/app/code_inspection.py`, `backend/app/github_readonly.py`, `backend/app/main.py`, `backend/app/multi_file_review.py`, `backend/app/security.py`, `backend/app/sessions.py`, `frontend/src/App.jsx`, `frontend/src/CodeReviewPanel.jsx`, `frontend/src/MultiReviewPanel.jsx`, `frontend/src/chatExport.mjs`, `frontend/src/chatHistory.mjs`, `frontend/src/chatRequestGate.mjs`, `frontend/src/codeReviewApi.mjs`, `frontend/src/githubApi.mjs`, `frontend/src/githubRequestUtils.mjs`, `frontend/src/main.jsx`, `frontend/src/multiReviewApi.mjs`, `frontend/vite.config.mjs`.
- Build/dependências: `backend/requirements.txt`, `frontend/package.json`.
- Arquivo lido: [backend/app/main.py](https://github.com/juniordev830/codax-assirtende-engenharia-ia-/blob/main/backend/app/main.py) · blob `d796c7e86f9d`.
- Declarações: `_limited`, `access_control`, `github_repositories`, `github_repository_files`, `github_repository_source`, `AIReviewRequest`, `github_ai_review`, `SourceSelection`, `LocalMultiFileRequest`, `DiffProposalRequest`, `github_review_batch`, `github_diff_proposal`, `github_repository`, `SessionRequest`, `session`, `logout_session`, `ChatTurn`, `ChatRequest`, `validate_history_budget`, `health`, `capabilities`, `local_reply`, `chat`.
- Imports: `asyncio`, `os`, `sqlite3`, `re`, `hmac`, `time`, `collections`, `threading`, `datetime`, `dotenv`, `fastapi`, `fastapi.responses`, `fastapi.middleware.cors`, `openai`, `pydantic`.
- Rotas literais: `GET /api/github/repos`, `GET /api/github/repos/{repo_name}/files`, `GET /api/github/repos/{repo_name}/source`, `POST /api/github/repos/{repo_name}/ai-review`, `POST /api/github/repos/{repo_name}/review-batch`, `POST /api/github/repos/{repo_name}/diff-proposal`, `GET /api/github/repos/{repo_name}`, `POST /api/session`, `POST /api/session/logout`, `GET /api/health`, `GET /api/capabilities`, `POST /api/chat`.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): `backend/app/security.py`, `backend/app/sessions.py`.
- Testes (17 arquivos por convenção): `backend/tests/conftest.py`, `backend/tests/test_access.py`, `backend/tests/test_ai_code_review.py`, `backend/tests/test_api.py`, `backend/tests/test_codax_profiles.py`, `backend/tests/test_code_inspection.py`, `backend/tests/test_github_readonly.py`, `backend/tests/test_history.py`, `backend/tests/test_local_reply.py`, `backend/tests/test_multi_file_review.py`, `frontend/tests/chatExport.test.mjs`, `frontend/tests/chatHistory.test.mjs`.
- CI: `.github/workflows/backend-tests.yml`, `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## code-security-scanner

[Repositório](https://github.com/juniordev830/code-security-scanner) · árvore `8156ee109e5f142c7f0ebd10daf0b60fe7004d00`

- Código (1 arquivos filtrados): `scanner.py`.
- Build/dependências: não detectado.
- Arquivo lido: [scanner.py](https://github.com/juniordev830/code-security-scanner/blob/main/scanner.py) · blob `11734970b937`.
- Declarações: `sarif_report`, `mask_python_literals`, `python_call_findings`, `incomplete_finding`, `scan`, `on_walk_error`, `main`.
- Imports: `__future__`, `argparse`, `ast`, `io`, `json`, `os`, `re`, `stat`, `tokenize`, `pathlib`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (7 arquivos por convenção): `tests/test_incomplete_scan.py`, `tests/test_incomplete_scan_regressions.py`, `tests/test_options.py`, `tests/test_os_system_rule.py`, `tests/test_pruned_walk.py`, `tests/test_python_call_names.py`, `tests/test_scanner.py`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## comparador-json

[Repositório](https://github.com/juniordev830/comparador-json) · árvore `eeaafa294a8b4a536f0c9fce2f7da70a65dd7617`

- Código (3 arquivos filtrados): `cli/inspect.php`, `main.php`, `src/JsonInspector.php`.
- Build/dependências: não detectado.
- Arquivo lido: [main.php](https://github.com/juniordev830/comparador-json/blob/main/main.php) · blob `d376b3bc5483`.
- Declarações: `pointer`, `diff`, `readJson`, `expect`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (2 arquivos por convenção): `tests/CliTest.php`, `tests/JsonInspectorTest.php`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## concordancia-biblica

[Repositório](https://github.com/juniordev830/concordancia-biblica) · árvore `a99f910afe97abd33a9ee2daf7129d7d1f0b7a37`

- Código (9 arquivos filtrados): `backend/__init__.py`, `backend/corpus.py`, `backend/main.py`, `backend/search.py`, `src/App.tsx`, `src/main.tsx`, `src/search.ts`, `src/storage.ts`, `vite.config.ts`.
- Build/dependências: `package.json`, `requirements.txt`.
- Arquivo lido: [src/App.tsx](https://github.com/juniordev830/concordancia-biblica/blob/main/src/App.tsx) · blob `d2faba3344f7`.
- Declarações: `App`, `run`, `favorite`, `downloadPage`.
- Imports: `react`, `./search.ts`, `./storage.ts`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): `src/storage.ts`.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (2 arquivos por convenção): `backend/tests/test_search.py`, `tests/search.test.ts`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## consumo-energia

[Repositório](https://github.com/juniordev830/consumo-energia) · árvore `3c25788fb22863a3dc56a5dc17db486369078c1e`

- Código (4 arquivos filtrados): `src/ConsumoEnergia/AnaliseOrcamento.cs`, `src/ConsumoEnergia/ComparadorCenarios.cs`, `src/ConsumoEnergia/Program.cs`, `src/ConsumoEnergia/SimuladorHoras.cs`.
- Build/dependências: `src/ConsumoEnergia/ConsumoEnergia.csproj`.
- Arquivo lido: [src/ConsumoEnergia/Program.cs](https://github.com/juniordev830/consumo-energia/blob/main/src/ConsumoEnergia/Program.cs) · blob `4db5aec6fa89`.
- Declarações: `ConsumoEnergia`, `Aparelho`, `Cenario`, `ConsumoAparelho`, `Relatorio`, `Estimador`, `Program`.
- Imports: `System.Globalization`, `System.Text.Json`, `System.Text.Json.Serialization`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (0 arquivos por convenção): não detectado.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## contratos-prazos

[Repositório](https://github.com/juniordev830/contratos-prazos) · árvore `0dc5f7a4cdf139ce64ab0e05ec1431e24a09e1bd`

- Código (6 arquivos filtrados): `src/contratos_prazos/__init__.py`, `src/contratos_prazos/cli.py`, `src/contratos_prazos/core.py`, `src/contratos_prazos/exporting.py`, `src/contratos_prazos/records.py`, `src/contratos_prazos/storage.py`.
- Build/dependências: `pyproject.toml`.
- Arquivo lido: [src/contratos_prazos/cli.py](https://github.com/juniordev830/contratos-prazos/blob/main/src/contratos_prazos/cli.py) · blob `e54c4bbf2e9a`.
- Declarações: `parser`, `main`.
- Imports: `__future__`, `argparse`, `datetime`, `pathlib`, `sys`, `.records`, `.storage`, `.exporting`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): `src/contratos_prazos/storage.py`.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (6 arquivos por convenção): `tests/test_cli.py`, `tests/test_core.py`, `tests/test_exporting.py`, `tests/test_records.py`, `tests/test_renew_preview.py`, `tests/test_storage.py`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## corrida-maluca-

[Repositório](https://github.com/juniordev830/corrida-maluca-) · árvore `8385c96e21c2ab5464d53a07296c953be6823d06`

- Código (2 arquivos filtrados): `game.js`, `scripts/build-web.mjs`.
- Build/dependências: `package.json`.
- Arquivo lido: [game.js](https://github.com/juniordev830/corrida-maluca-/blob/main/game.js) · blob `709c2fa41dcd`.
- Declarações: `resizeCanvas`, `laneX`, `localStorage_get`, `localStorage_set`, `highScoreKey`, `readHighScore`, `selectedDifficulty`, `spawnObstacle`, `spawnStar`, `spawnParticles`, `rectsOverlap`, `drawRoundedCar`, `drawObstacle`, `update`, `draw`, `drawStar`, `resetClock`, `loop`, `startGame`, `endGame`, `togglePause`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (2 arquivos por convenção): `tests/frame-rate.test.js`, `tests/game.test.mjs`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/portfolio-checks.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.

