# Complemento — linguagens e ferramentas fora do filtro inicial

Os quatro projetos abaixo não foram reconhecidos pelo filtro de extensões inicial. A leitura direta dos módulos de domínio corrige essa lacuna. Análise estática; testes não executados.

## caderno-offline

Fonte: [bin/notebook.dart](https://github.com/juniordev830/caderno-offline/blob/main/bin/notebook.dart), blob `20f3c4664a2d`. Dart; build por `pubspec.yaml`.

`NoteRecord` reúne ID, título, conteúdo, tags e data de modificação; `Notebook` opera sobre uma pasta de arquivos Markdown. O fluxo é validar o identificador e a pasta, ler o arquivo regular, extrair título e tags e criar o registro. Criação e atualização usam arquivo temporário e renomeação; a busca normaliza acentos, aplica filtros e paginação. Há limites de tamanho e quantidade, rejeição de NUL e verificações de links simbólicos. Essas verificações não constituem prova de segurança contra concorrência no filesystem. Teste identificado: `bin/notebook_test.dart`. Entrada CLI: `bin/main.dart`.

## infrastructure-as-code-lab

Fonte: [terraform/main.tf](https://github.com/juniordev830/infrastructure-as-code-lab/blob/main/terraform/main.tf), blob `5dc4bc00fbe3`. Terraform/HCL, versão mínima declarada 1.5.

O módulo usa `terraform_data.environment` para modelar ambiente, proprietário e serviço; não provisiona recursos de nuvem. As precondições opcionais rejeitam orçamento inválido, custo acima do limite, alocação incompatível e previsões mensais ou acumuladas que excedam o orçamento. As variáveis, cálculos e outputs estão distribuídos pelos arquivos `variables.tf`, `allocation.tf`, `budget.tf`, `forecast.tf`, `horizon_budget.tf`, `alerts.tf`, `risk.tf` e `outputs.tf`. O diretório `terraform/tests` possui oito arquivos de teste HCL. Verificar a compatibilidade da versão de Terraform com os testes antes de executar.

## quiz-sala

Fonte: [tournament.exs](https://github.com/juniordev830/quiz-sala/blob/main/tournament.exs), blob `df9f1611abc1`. Elixir.

`QuizTournament` usa GenServer para serializar operações sobre o estado em memória: banco de questões, equipes, perguntas usadas, rodada ativa, histórico e eventos. A API expõe registro, início de rodada, respostas, pausa/retomada, encerramento, ranking, histórico, relatórios e CSV. A inicialização normaliza o banco; validações incluem limites de equipes e questões, IDs positivos, alternativas de 1 a 4 e pontuação de 1 a 100. O registro fecha após o início da competição. A persistência após reinício e a exposição por rede não foram verificadas. Arquivos: `main.exs`, `tournament_test.exs`.

## trilhas-locais

Fonte: [lib/trails.dart](https://github.com/juniordev830/trilhas-locais/blob/main/lib/trails.dart), blob `36d51b6018b5`. Dart.

`Trail` é o modelo validado de trilha: ID, nome, distância, dificuldade e observações. `TrailCatalog` armazena trilhas e favoritos em memória, rejeita duplicatas, filtra por distância/dificuldade e ordena por distância e ID. A serialização JSON registra versão de esquema; a importação valida tipos, quantidade, duplicatas e referências de favoritos. Não utiliza GPS no módulo lido. `lib/persistent_trails.dart`, `lib/storage.dart` e `lib/pace.dart` são módulos adicionais ainda não rastreados. Testes identificados em `test/catalog_test.dart`, `test/pace_test.dart` e `test/storage_test.dart`.
