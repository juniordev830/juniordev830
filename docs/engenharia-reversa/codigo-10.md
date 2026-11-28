# Mapa de código — lote 10

Árvore Git e leitura amostral de um arquivo por projeto; sem execução.

## roteiro-grupo-biblico

[Repositório](https://github.com/juniordev830/roteiro-grupo-biblico) · árvore `ae60c374cbe3ff8223f9bb19e33c0ef24056fa15`

- Código (2 arquivos filtrados): `app.py`, `relatorio_csv.py`.
- Build/dependências: não detectado.
- Arquivo lido: [app.py](https://github.com/juniordev830/roteiro-grupo-biblico/blob/main/app.py) · blob `f42b78b28d8f`.
- Declarações: `texto`, `inteiro`, `chave`, `run`, `objeto_sem_campos_repetidos`, `rejeitar_constante_json`, `main`.
- Imports: `unicodedata`, `argparse`, `contextlib`, `sys`, `relatorio_csv`, `json`, `pathlib`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (5 arquivos por convenção): `test_app.py`, `test_json_size_limit.py`, `test_saida_csv.py`, `test_stdin.py`, `test_validation.py`.
- CI: `.github/workflows/testes.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## rpg-quest-python

[Repositório](https://github.com/juniordev830/rpg-quest-python) · árvore `b6650139fb709d7882d395e0aa8a5cdf281053da`

- Código (1 arquivos filtrados): `main.py`.
- Build/dependências: não detectado.
- Arquivo lido: [main.py](https://github.com/juniordev830/rpg-quest-python/blob/main/main.py) · blob `ee1c81f03c36`.
- Declarações: `validated_name`, `Character`, `__init__`, `is_alive`, `take_damage`, `battle`, `valid_rounds`, `main`.
- Imports: `argparse`, `json`, `random`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (3 arquivos por convenção): `tests/test_cli.py`, `tests/test_main.py`, `tests/test_name_validation.py`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## secure-api-gateway

[Repositório](https://github.com/juniordev830/secure-api-gateway) · árvore `486d71ba106fe4b586119e229f20262ba3ae6858`

- Código (2 arquivos filtrados): `cmd/gateway/main.go`, `gateway.go`.
- Build/dependências: `go.mod`.
- Arquivo lido: [cmd/gateway/main.go](https://github.com/juniordev830/secure-api-gateway/blob/main/cmd/gateway/main.go) · blob `92335e32dd22`.
- Declarações: `newHTTPServer`, `main`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (2 arquivos por convenção): `cmd/gateway/main_test.go`, `gateway_test.go`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## sentinel-atlas

[Repositório](https://github.com/juniordev830/sentinel-atlas) · árvore `d8366a7e74aace961e10c9df01439e9685e8ab18`

- Código (154 arquivos filtrados): `backend/ai.py`, `backend/alerts.py`, `backend/app.py`, `backend/geo_layers.py`, `backend/location.py`, `backend/orbits.py`, `backend/routing.py`, `backend/shared_limits.py`, `backend/source_clients.py`, `backend/storage.py`, `data/adminBoundaries.js`, `data/adsbLolFallback.js`, `data/aircraftClass.js`, `data/aircraftEmergency.js`, `data/aircraftIcons.js`, `data/aircraftMeta.js`, `data/aircraftNearbyPolicy.js`, `data/aircraftRecession.js`, `data/aisLiveVessels.js`, `data/aisStreamAdapter.js`, `data/aisWatchdog.js`, `data/alprCameras.js`, `data/analystEngine.js`, `data/approxDistance.js`, `data/bhoteKoshiEmbeddedMedia.js`, `data/bhoteKoshiEvent.js`, `data/bhoteKoshiFloodPath.js`, `data/bhoteKoshiIncidentPlaces.js`, `data/bhoteKoshiLocator.js`, `data/bhoteKoshiShotPaths.js`.
- Build/dependências: `Dockerfile`, `backend/requirements.txt`, `compose.yaml`, `docker-compose.yml`.
- Arquivo lido: [backend/app.py](https://github.com/juniordev830/sentinel-atlas/blob/main/backend/app.py) · blob `36727b21f7fc`.
- Declarações: `validate_analysis_items`, `AIAnalyzeInput`, `validate_assets`, `validate_fences`, `AIQueryInput`, `validate_context`, `GeofenceInput`, `PositionInput`, `SessionLoginInput`, `_release_lease`, `_session_digest`, `_valid_session_cookie`, `_is_same_origin`, `optional_token_auth`, `browser_login_page`, `create_browser_session`, `end_browser_session`, `health`, `sources`, `public_config`, `geoint_layers`, `geoint_layer_data`, `satellites`, `starlink`, `aircraft`, `bicycle`, `create_geofence`, `list_geofences`, `delete_geofence`, `position_history`, `valid_map_coordinate`, `map_features`, `location_info`, `ai_analyze`, `ai_query`.
- Imports: `__future__`, `asyncio`, `json`, `math`, `hmac`, `os`, `logging`, `sqlite3`, `sys`, `secrets`, `time`, `urllib.parse`, `dataclasses`, `pathlib`, `typing`.
- Rotas literais: `GET /login`, `POST /api/session`, `POST /api/session/logout`, `GET /api/health`, `GET /api/sources`, `GET /api/public-config`, `GET /api/geoint/layers`, `GET /api/geoint/layers/{layer_id}`, `GET /api/sources/satellites`, `GET /api/sources/starlink`, `GET /api/sources/aircraft`, `GET /api/routes/bicycle`, `POST /api/geofences`, `GET /api/geofences`, `DELETE /api/geofences/{name}`, `GET /api/positions/history`, `GET /api/map/features`, `GET /api/location/info`, `POST /api/ai/analyze`, `POST /api/ai/query`.
- Persistência/modelagem (nomes candidatos): `backend/storage.py`, `data/modelEligibility.js`, `data/modelVisualAnchor.js`, `data/motionModel.js`, `data/regionalModel.js`, `data/trackedModelRegime.js`, `web/assets/models/README.md`, `web/assets/models/airplane.glb`, `web/assets/models/atr72.glb`, `web/assets/models/b789.glb`.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (202 arquivos por convenção): `data/adminBoundaries.test.mjs`, `data/adsbLolFallback.test.mjs`, `data/aircraftClass.test.mjs`, `data/aircraftEmergency.test.mjs`, `data/aircraftEmergencyAnalyst.test.mjs`, `data/aircraftMeta.test.mjs`, `data/aircraftNearbyPolicy.test.mjs`, `data/aircraftRecession.test.mjs`, `data/aisLiveVessels.analyst.test.mjs`, `data/aisLiveVessels.test.mjs`, `data/aisStreamAdapter.test.mjs`, `data/aisStreamSentinels.test.mjs`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## series-de-pregacao

[Repositório](https://github.com/juniordev830/series-de-pregacao) · árvore `88a9ba441da4840545b346b64c6ca873d8288843`

- Código (3 arquivos filtrados): `app.py`, `exportar-agenda.mjs`, `relatorio_csv.py`.
- Build/dependências: não detectado.
- Arquivo lido: [app.py](https://github.com/juniordev830/series-de-pregacao/blob/main/app.py) · blob `f12a8acf51d5`.
- Declarações: `texto`, `textos`, `inteiro`, `run`, `proxima`, `objeto_sem_campos_repetidos`, `rejeitar_constante_json`, `main`.
- Imports: `datetime`, `argparse`, `contextlib`, `sys`, `relatorio_csv`, `json`, `pathlib`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (7 arquivos por convenção): `test_app.py`, `test_calendar_limits.py`, `test_exportacao.py`, `test_json_size_limit.py`, `test_saida_csv.py`, `test_stdin.py`, `test_validation.py`.
- CI: `.github/workflows/testes.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## site-e-commerce-

[Repositório](https://github.com/juniordev830/site-e-commerce-) · árvore `c13ef318b1e93b11837857f05591afe1bd091449`

- Código (27 arquivos filtrados): `backend/prisma/seed.ts`, `backend/src/app.ts`, `backend/src/config.ts`, `backend/src/lib/prisma.ts`, `backend/src/middleware/auth.ts`, `backend/src/middleware/errors.ts`, `backend/src/routes/auth.ts`, `backend/src/routes/orders.ts`, `backend/src/routes/products.ts`, `backend/src/server.ts`, `backend/src/types/express.d.ts`, `frontend/src/App.tsx`, `frontend/src/auth/AuthContext.tsx`, `frontend/src/components/AuthShell.tsx`, `frontend/src/components/ErrorBoundary.tsx`, `frontend/src/components/Field.tsx`, `frontend/src/components/Layout.tsx`, `frontend/src/lib/api.ts`, `frontend/src/lib/cart.ts`, `frontend/src/main.tsx`, `frontend/src/pages/Cart.tsx`, `frontend/src/pages/Home.tsx`, `frontend/src/pages/Login.tsx`, `frontend/src/pages/NotFound.tsx`, `frontend/src/pages/Register.tsx`, `frontend/src/vite-env.d.ts`, `frontend/vite.config.ts`.
- Build/dependências: `backend/package.json`, `frontend/package.json`, `package.json`.
- Arquivo lido: [backend/src/app.ts](https://github.com/juniordev830/site-e-commerce-/blob/main/backend/src/app.ts) · blob `6bf35f4300f7`.
- Declarações: `createApp`.
- Imports: `cookie-parser`, `cors`, `express`, `helmet`, `./config.js`, `./lib/prisma.js`, `./middleware/errors.js`, `./routes/auth.js`, `./routes/products.js`, `./routes/orders.js`.
- Rotas literais: `GET /api/health`, `GET /api/health/live`.
- Persistência/modelagem (nomes candidatos): `backend/prisma/migration_lock.toml`, `backend/prisma/migrations/0001_init/migration.sql`, `backend/prisma/migrations/20261127140000_add_user_token_version/migration.sql`, `backend/prisma/schema.prisma`.
- Segurança/validação (nomes candidatos): `backend/src/middleware/auth.ts`, `backend/src/middleware/errors.ts`, `backend/src/routes/auth.ts`, `frontend/src/auth/AuthContext.tsx`, `frontend/src/components/AuthShell.tsx`.
- Testes (2 arquivos por convenção): `backend/tests/checkout.test.ts`, `frontend/tests/cart.test.mjs`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## space-miner-2d

[Repositório](https://github.com/juniordev830/space-miner-2d) · árvore `c06f703a8577930d1b719107225330cdc29bc337`

- Código (6 arquivos filtrados): `bin/demo.js`, `src/combo.mjs`, `src/main.mjs`, `src/mineracao.js`, `src/rules.mjs`, `vite.config.mjs`.
- Build/dependências: `package.json`.
- Arquivo lido: [src/main.mjs](https://github.com/juniordev830/space-miner-2d/blob/main/src/main.mjs) · blob `cbab97feb8a6`.
- Declarações: `refreshHud`, `createRock`, `mineNearest`.
- Imports: `pixi.js`, `./rules.mjs`, `./combo.mjs`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (3 arquivos por convenção): `test/mineracao.test.js`, `tests/combo.test.mjs`, `tests/rules.test.mjs`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/mining-tests.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## space-shooter-js

[Repositório](https://github.com/juniordev830/space-shooter-js) · árvore `ba3ef6d4db603999069261718609a0afdac3acc2`

- Código (3 arquivos filtrados): `game.js`, `love2d/engine.lua`, `love2d/main.lua`.
- Build/dependências: não detectado.
- Arquivo lido: [love2d/main.lua](https://github.com/juniordev830/space-shooter-js/blob/main/love2d/main.lua) · blob `b35f2c5b015f`.
- Declarações: `love`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (2 arquivos por convenção): `game.test.js`, `love2d/test_engine.lua`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/lua-love2d.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## submarine-abyss

[Repositório](https://github.com/juniordev830/submarine-abyss) · árvore `f73792ac6923e0166ac1fcf8b2718343812bb6c5`

- Código (4 arquivos filtrados): `core.py`, `scripts/ocean.gd`, `scripts/oxygen_rules.gd`, `scripts/submarine.gd`.
- Build/dependências: `project.godot`.
- Arquivo lido: [scripts/oxygen_rules.gd](https://github.com/juniordev830/submarine-abyss/blob/main/scripts/oxygen_rules.gd) · blob `e560ab5e978f`.
- Declarações: `consume_oxygen`, `replenish_oxygen`, `can_collect`, `oxygen_rate_at_depth`, `estimated_oxygen_seconds`, `nearest_target_index`, `sonar_direction`, `sonar_relative_direction`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (2 arquivos por convenção): `tests/test_core.py`, `tests/test_oxygen.gd`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/godot-exploration.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.

