# Mapa de código — lote 08

Árvore Git e leitura amostral de um arquivo por projeto; sem execução.

## oficina-digital

[Repositório](https://github.com/juniordev830/oficina-digital) · árvore `6441f76ca0fcfa2a890b0dca60093949ecda19ef`

- Código (4 arquivos filtrados): `src/OficinaDigital/Cadastro.cs`, `src/OficinaDigital/Domain.cs`, `src/OficinaDigital/Gestao.cs`, `src/OficinaDigital/Orcamentos.cs`.
- Build/dependências: `src/OficinaDigital/OficinaDigital.csproj`, `tests/OficinaDigital.Tests/OficinaDigital.Tests.csproj`.
- Arquivo lido: [src/OficinaDigital/Domain.cs](https://github.com/juniordev830/oficina-digital/blob/main/src/OficinaDigital/Domain.cs) · blob `877d02979d74`.
- Declarações: `OficinaDigital`, `StatusOrdem`, `OrdemServico`, `OficinaService`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (1 arquivos por convenção): `tests/OficinaDigital.Tests/Program.cs`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## orcamento-freelancer

[Repositório](https://github.com/juniordev830/orcamento-freelancer) · árvore `0563daf6300988dbd4c6118fb36d9eac1687000c`

- Código (4 arquivos filtrados): `cli/proposal.mjs`, `src/calculator.ts`, `src/formatter.ts`, `src/proposal.ts`.
- Build/dependências: `package.json`.
- Arquivo lido: [src/proposal.ts](https://github.com/juniordev830/orcamento-freelancer/blob/main/src/proposal.ts) · blob `42858e3908e5`.
- Declarações: `PaymentStageInput`, `ProposalInput`, `ProposalItem`, `PaymentStage`, `Proposal`, `calendarDay`, `percentageToBasisPoints`, `requireName`, `toCents`, `distributeCents`, `createPaymentPlan`, `createProposal`, `isProposalExpired`.
- Imports: `./calculator.js`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (4 arquivos por convenção): `test/calculator.test.ts`, `test/formatter.test.ts`, `test/precision.test.ts`, `test/proposal.test.ts`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## order-service-csharp

[Repositório](https://github.com/juniordev830/order-service-csharp) · árvore `0cd22eecbf699bdf9b3d3c4912313a11c455bc51`

- Código (5 arquivos filtrados): `Order.cs`, `OrderFinancials.cs`, `OrderInsights.cs`, `OrderRepository.cs`, `Program.cs`.
- Build/dependências: `OrderService.csproj`, `tests/OrderService.Tests/OrderService.Tests.csproj`.
- Arquivo lido: [Program.cs](https://github.com/juniordev830/order-service-csharp/blob/main/Program.cs) · blob `1a4a5440bd5f`.
- Declarações: `OrderService`, `Program`.
- Imports: `System`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): `OrderRepository.cs`.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (4 arquivos por convenção): `tests/OrderService.Tests/OrderFinancialsTests.cs`, `tests/OrderService.Tests/OrderInsightsTests.cs`, `tests/OrderService.Tests/OrderLifecycleTests.cs`, `tests/OrderService.Tests/OrderRepositoryTests.cs`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## panorama-biblico-interativo

[Repositório](https://github.com/juniordev830/panorama-biblico-interativo) · árvore `cc79aff7cc7b14366a1bb8aa2f37b6be2c090a12`

- Código (5 arquivos filtrados): `src/App.tsx`, `src/canon.ts`, `src/content.ts`, `src/main.tsx`, `vite.config.ts`.
- Build/dependências: `package.json`.
- Arquivo lido: [src/App.tsx](https://github.com/juniordev830/panorama-biblico-interativo/blob/main/src/App.tsx) · blob `5fce1cf5d79d`.
- Declarações: `App`, `selectBook`.
- Imports: `react`, `./content.ts`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (1 arquivos por convenção): `tests/content.test.ts`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## payment-service-java

[Repositório](https://github.com/juniordev830/payment-service-java) · árvore `85f024effa660e7a7e36fffc541718b58161a45b`

- Código (9 arquivos filtrados): `src/main/java/br/com/joao/pagamentos/ApiExceptionHandler.java`, `src/main/java/br/com/joao/pagamentos/CriarPagamentoRequest.java`, `src/main/java/br/com/joao/pagamentos/MicrosservicoPagamentosApplication.java`, `src/main/java/br/com/joao/pagamentos/Pagamento.java`, `src/main/java/br/com/joao/pagamentos/PagamentoController.java`, `src/main/java/br/com/joao/pagamentos/PagamentoRepository.java`, `src/main/java/br/com/joao/pagamentos/PaymentAccessFilter.java`, `src/main/java/br/com/joao/pagamentos/ResumoMoedaResponse.java`, `src/main/java/br/com/joao/pagamentos/StatusPagamento.java`.
- Build/dependências: `pom.xml`.
- Arquivo lido: [src/main/java/br/com/joao/pagamentos/PagamentoController.java](https://github.com/juniordev830/payment-service-java/blob/main/src/main/java/br/com/joao/pagamentos/PagamentoController.java) · blob `0ffc76bb7176`.
- Declarações: `PagamentoController`, `StatusRequest`.
- Imports: `jakarta.validation.Valid`, `jakarta.validation.constraints.NotNull`, `java.math.BigDecimal`, `java.util.LinkedHashMap`, `java.util.List`, `java.util.Locale`, `java.util.Map`, `org.springframework.data.domain.PageRequest`, `org.springframework.data.domain.Sort`, `org.springframework.http.HttpStatus`, `org.springframework.http.ResponseEntity`, `org.springframework.transaction.annotation.Transactional`, `org.springframework.web.bind.annotation.GetMapping`, `org.springframework.web.bind.annotation.PathVariable`, `org.springframework.web.bind.annotation.PostMapping`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): `src/main/java/br/com/joao/pagamentos/PagamentoRepository.java`.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (6 arquivos por convenção): `src/test/java/br/com/joao/pagamentos/DesfechoPagamentoTests.java`, `src/test/java/br/com/joao/pagamentos/MicrosservicoPagamentosApplicationTests.java`, `src/test/java/br/com/joao/pagamentos/PagamentoStatusFilterTests.java`, `src/test/java/br/com/joao/pagamentos/PaymentAccessFilterTests.java`, `src/test/java/br/com/joao/pagamentos/PaymentAccessRouteTests.java`, `src/test/java/br/com/joao/pagamentos/ResumoMoedaTests.java`.
- CI: `.github/workflows/ci.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## physics-lab-playground

[Repositório](https://github.com/juniordev830/physics-lab-playground) · árvore `863818f7df4d0f4be0ac94d053919eafb47ba979`

- Código (8 arquivos filtrados): `core.py`, `src/main.cpp`, `src/physics/analysis.py`, `src/physics/collision.py`, `src/physics/forces.py`, `src/physics/motion.py`, `src/physics/vector2.py`, `src/physics/world.py`.
- Build/dependências: `CMakeLists.txt`.
- Arquivo lido: [src/main.cpp](https://github.com/juniordev830/physics-lab-playground/blob/main/src/main.cpp) · blob `3d4639735d1e`.
- Declarações: não detectado.
- Imports: `physics.hpp`, `SFML/Graphics.hpp`, `algorithm`, `array`, `cmath`, `optional`, `string`.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (11 arquivos por convenção): `tests/physics_test.cpp`, `tests/test_analysis.py`, `tests/test_collision.py`, `tests/test_contact_resolution.py`, `tests/test_core.py`, `tests/test_forces.py`, `tests/test_motion.py`, `tests/test_motion_diagnostics.py`, `tests/test_vector2.py`, `tests/test_vector_geometry.py`, `tests/test_world.py`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/python-physics.yml`, `.github/workflows/sfml-laboratory.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## pixel-farm-seasons

[Repositório](https://github.com/juniordev830/pixel-farm-seasons) · árvore `97c5ca17706d4c6e7d5b06de518cb9971c6c2550`

- Código (43 arquivos filtrados): `game.js`, `gameplay/daily_needs.py`, `gameplay/day_night.py`, `gameplay/house_interactions.py`, `godot/building_collision.gd`, `godot/day_night_controller.gd`, `godot/farm_environment.gd`, `godot/farm_hud.gd`, `godot/farm_props.gd`, `godot/farm_workshop.gd`, `godot/farmer_needs.gd`, `godot/farmer_visual.gd`, `godot/farmhouse_details.gd`, `godot/farmhouse_interior.gd`, `godot/garage_door.gd`, `godot/ground_collision.gd`, `godot/interactive_bed.gd`, `godot/interactive_fridge.gd`, `godot/interactive_front_door.gd`, `godot/player_controller.gd`, `godot/scripts/asset_quality_pass.gd`, `godot/scripts/campaign_ending.gd`, `godot/scripts/cozy_game_hud.gd`, `godot/scripts/cozy_reference_art.gd`, `godot/scripts/environment_art_pass.gd`, `godot/scripts/farm_missions.gd`, `godot/scripts/farm_world.gd`, `godot/scripts/farmer_art_v1.gd`, `godot/scripts/farmer_controller.gd`, `godot/scripts/farming_system.gd`.
- Build/dependências: `godot/project.godot`, `legacy/godot-2d/project.godot`.
- Arquivo lido: [godot/player_controller.gd](https://github.com/juniordev830/pixel-farm-seasons/blob/main/godot/player_controller.gd) · blob `0777ecfab742`.
- Declarações: `_ready`, `_unhandled_input`, `_physics_process`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (21 arquivos por convenção): `godot/tests/animated_farmer_smoke.gd`, `godot/tests/asset_quality_smoke.gd`, `godot/tests/campaign_ending_smoke.gd`, `godot/tests/capture_gameplay.gd`, `godot/tests/car_motion_smoke.gd`, `godot/tests/cozy_hud_smoke.gd`, `godot/tests/cozy_reference_smoke.gd`, `godot/tests/event_clock_smoke.gd`, `godot/tests/farm_missions_smoke.gd`, `godot/tests/farmer_art_smoke.gd`, `godot/tests/farming_smoke.gd`, `godot/tests/main_menu_smoke.gd`.
- CI: `.github/workflows/godot-export-windows.yml`, `.github/workflows/godot-life-sim.yml`, `.github/workflows/godot-screenshots.yml`, `.github/workflows/godot-smoke.yml`, `.github/workflows/python-gameplay.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## plataforma-de-recrutamento

[Repositório](https://github.com/juniordev830/plataforma-de-recrutamento) · árvore `b305a5520a6e64ab0cb8b6b775daa112f6c784a8`

- Código (3 arquivos filtrados): `playwright.config.cjs`, `registration.js`, `server.js`.
- Build/dependências: `package.json`.
- Arquivo lido: [server.js](https://github.com/juniordev830/plataforma-de-recrutamento/blob/main/server.js) · blob `3f3af58c9688`.
- Declarações: `run`, `get`, `all`, `initializeDatabase`, `TEXT`, `createToken`, `dummyHashForCost`, `passwordMaterial`, `hashPassword`, `verifyPassword`, `resetAuthAttemptBuckets`, `authAttemptLimiter`, `authMiddleware`, `parsePageParameter`, `parseJobId`, `requireCandidate`, `inlineBlockHashes`, `provisionCompany`, `start`.
- Imports: não detectado.
- Rotas literais: `POST /api/logout`, `GET /api/health`, `POST /api/register`, `POST /api/login`, `GET /api/jobs`, `POST /api/jobs`, `GET /api/saved-jobs`, `PUT /api/saved-jobs/:jobId`, `DELETE /api/saved-jobs/:jobId`, `POST /api/applications`, `GET /api/applications`, `GET /api/privacy/export`, `GET /`.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (5 arquivos por convenção): `e2e/recruitment.spec.js`, `tests/api.test.js`, `tests/documentation.test.js`, `tests/frontend.test.js`, `tests/verified-registration.test.js`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/interface-chrome.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.


---

## puzzle-adventure-ts

[Repositório](https://github.com/juniordev830/puzzle-adventure-ts) · árvore `63378be7647b4e641516d518ec0f78dc8c56622a`

- Código (1 arquivos filtrados): `src/index.ts`.
- Build/dependências: `package.json`.
- Arquivo lido: [src/index.ts](https://github.com/juniordev830/puzzle-adventure-ts/blob/main/src/index.ts) · blob `32ec90981dff`.
- Declarações: `Point`, `GridBoard`, `main`.
- Imports: não detectado.
- Rotas literais: não detectado.
- Persistência/modelagem (nomes candidatos): não detectado.
- Segurança/validação (nomes candidatos): não detectado.
- Testes (1 arquivos por convenção): `src/index.test.ts`.
- CI: `.github/workflows/ci.yml`, `.github/workflows/portfolio-checks.yml`.

Evidência estática amostral; não comprova execução nem cobertura de todas as chamadas.

