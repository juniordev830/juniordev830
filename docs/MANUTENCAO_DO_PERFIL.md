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

- `README.md`: resumo e tabela de 14 dias, além da sequência oculta `CONTRIBUTIONS:METRICS` consumida por integrações antigas.
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
