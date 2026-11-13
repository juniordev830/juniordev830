# Perfil GitHub — documentação de manutenção: guia técnico

## Escopo real

Repositório especial de perfil com SVGs de apoio aos estudos, imagem de banner e script Python de contribuições. O README visual é o conteúdo público central.

## Arquivos relacionados

`README.md`, `scripts/render_daily_contributions.py`, `tests/test_daily_contributions.py`, `assets/` e `docs/`.

## Procedimento de validação

`python -m pytest tests -q` para validar o script; revisar SVG/Markdown em desktop e celular antes de publicar alterações de perfil.

Se algo não puder ser executado, registrar como pendente, sem afirmar sucesso. Preservar resultados reais de CI vinculados aos commits relevantes.

## Casos para revisão

Conferir fontes das contagens, intervalos de cache, datas UTC/horário local e links absolutos/relativos; não inserir métricas inventadas para aumentar o gráfico.

## Próxima evolução

O gráfico do GitHub é calculado pela própria plataforma, não pode ser alterado pelo README. Evitar commits artificiais, manipulação de datas ou promessas de contribuições não computadas.

## Para submeter uma mudança

- [ ] Especificar problema e comportamento esperado.
- [ ] Anexar evidência de teste ou reprodução real.
- [ ] Revisar acessibilidade, privacidade e licenças quando aplicável.
- [ ] Submeter em branch separada e revisar antes de merge.

## Sincronização do painel de contribuições

O painel exibido no README não lê o contador em tempo real: o GitHub Actions agenda consultas ao calendário oficial pela API GraphQL e publica **três saídas** quando a contagem ou o dia muda:

- `README.md`: imagem do painel com URL versionada, além da sequência oculta `CONTRIBUTIONS:METRICS` consumida por integrações antigas.
- `assets/contribuicoes-diarias.svg`: visual do painel incorporado ao perfil, com parâmetro de versão para atualizar o cache quando os números mudam.
- `assets/contribuicoes-diarias.json`: feed estável para uma interface interativa independente consumir. O feed contém `schema_version`, `source`, `login`, `timezone`, `calendar_date`, `today`, `yesterday`, `last_7_days`, `last_12_months` e `last_14_days`.

O endereço público do feed após a primeira publicação é:

`https://raw.githubusercontent.com/juniordev830/juniordev830/main/assets/contribuicoes-diarias.json`

O aplicativo externo precisa **buscar esse JSON** e invalidar seu próprio cache; alterar o repositório **não modifica automaticamente o código do site externo**. A API do GitHub e o agendador podem ter atrasos. O histórico mostrado é o oficial de contribuições contabilizadas, não a soma de todas as atividades, pushes ou PRs.

### Diagnóstico em caso de atraso

1. Abrir o [workflow de contribuições](https://github.com/juniordev830/juniordev830/actions/workflows/contribuicoes-diarias.yml) e observar a última execução de `main`.
2. Se a consulta GraphQL passar e o push falhar com `fetch first`, o workflow deve atualizar a cópia local do branch e repetir consulta/commit/push, até cinco tentativas. **Nunca usar force-push para corrigir o painel.**
3. Conferir se o JSON, o SVG e o comentário `CONTRIBUTIONS:METRICS` no README representam os mesmos valores; comparar datas em horário de Fortaleza.
4. Se a execução finalizar com sucesso e o GitHub mostrar números antigos, verificar a contagem no perfil oficial e o cache de imagens. Se só o painel externo continuar antigo, revisar o fetch/cache do site externo.
5. Não criar commits artificiais ou atualizar carimbo de horário somente para forçar atividade. Os arquivos não são regravados quando as contagens permanecem iguais.

Para testar localmente sem chamar a API:

```bash
python -m unittest discover -s tests -p 'test_daily_contributions.py' -v
```

## Continuidade dos gráficos e alternativa ao cron do GitHub

O agendamento nativo usa `3-58/5 * * * *` (UTC), solicitando uma atualização a cada cinco minutos.
**Isso não é uma garantia de execução a cada cinco minutos.** O GitHub pode atrasar ou omitir execuções de `schedule`.
O workflow mantém `workflow_dispatch` (execução manual) e aceita também `repository_dispatch` do tipo
`refresh-profile` (disparo externo autenticado). Não usar commits artificiais para substituir consultas.

### Executar manualmente agora

Abrir [GitHub Actions — Atualizar contribuições diárias](https://github.com/juniordev830/juniordev830/actions/workflows/contribuicoes-diarias.yml),
selecionar **Run workflow**, escolher `main` e acionar. Marcar `refresh_portfolio` quando quiser
revalidar os repositórios mesmo dentro da janela de seis horas.

### Configurar disparo externo independente (opcional)

Para reduzir o risco de janelas sem execução, configurar um serviço externo de agendamento que faça
`POST` a cada cinco ou dez minutos para `/repos/juniordev830/juniordev830/dispatches` com
`{"event_type":"refresh-profile"}`, autenticado com um token de acesso restrito a este
repositório e permissão **Contents: write**. O token deve permanecer exclusivamente no cofre de
segredos do provedor: nunca colocá-lo no repositório, README, URLs ou logs.

Exemplo para executar localmente, com token já fornecido pelo ambiente:

```bash
curl --fail-with-body --request POST \
  --url "https://api.github.com/repos/juniordev830/juniordev830/dispatches" \
  --header "Accept: application/vnd.github+json" \
  --header "Authorization: Bearer ${GITHUB_TOKEN}" \
  --header "X-GitHub-Api-Version: 2022-11-28" \
  --data '{"event_type":"refresh-profile"}'
```

Esse serviço externo **ainda precisa ser ativado** na plataforma escolhida; habilitar
`repository_dispatch` sozinho não constitui agendamento externo. Como alternativa, use
o botão manual do GitHub Actions. O workflow serializa execuções, preserva a `main` em
falhas e evita commits quando nada mudou.

### Frequência do painel de projetos

A auditoria de árvores de arquivos é custosa e usa janelas UTC de seis horas:
00:00–05:59, 06:00–11:59, 12:00–17:59 e 18:00–23:59. Uma execução que ocorrer
na mesma janela não faz nova varredura, exceto quando `refresh_portfolio` for ativado.
Essas janelas são **limites de frequência**, não promessas de execução pontual.
O inventário preserva o último resultado verificável se uma consulta falhar.

### Detectar divergências

O workflow executa `python scripts/verify_profile_panels.py` antes de publicar.
A validação compara os 14 dias e totais no JSON, as barras do SVG e as métricas
ocultas do README, além de verificar a estrutura do gráfico e relatório de projetos.
Dados inconsistentes impedem a publicação. Uma execução sem commit pode significar
apenas que o GitHub retornou as mesmas contagens.

O dashboard externo utiliza o feed público `assets/contribuicoes-diarias.json`.
Seu código e seu cache são independentes do GitHub Actions; a atualização correta
deste repositório **não comprova** que o site externo esteja atualizado ou disponível.
É preciso validar seu fetch HTTP e o tratamento de cache separadamente.
