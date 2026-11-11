# Dados de contribuições para o painel interativo

O gerador `scripts/render_daily_contributions.py` consulta o calendário de
contribuições do GitHub GraphQL. O arquivo `assets/contribuicoes.json` usa
**somente números informados por essa API**. Ele pode ser consumido por um
painel web independente depois da integração desta branch.

## Contrato JSON (schemaVersion 1)

```json
{
  "schemaVersion": 1,
  "user": "juniordev830",
  "dailyGoal": 250,
  "observedOn": "2026-11-11",
  "goalProgress": {
    "remainingToday": 237,
    "reachedToday": false,
    "percentToday": 5.2
  },
  "stats": {
    "today": 13,
    "yesterday": 12,
    "week": 70,
    "year": 2012
  },
  "days": [
    { "date": "2026-10-29", "count": 0 }
  ],
  "source": "https://api.github.com/graphql"
}
```

**Valores acima são apenas um exemplo de formato, não um registro de
contribuições atuais.** Na geração real, `days` contém 14 datas consecutivas
em ordem cronológica e os valores do período são obtidos da API.

- `observedOn`: último dia da janela, no fuso **America/Fortaleza**. Um
  cliente pode comparar com a data atual local para detectar dados defasados.
- `goalProgress.remainingToday`: quanto falta para atingir a meta diária;
  nunca fica negativo.
- `goalProgress.reachedToday`: indica se o dia alcançou a meta.
- `goalProgress.percentToday`: percentual real, **sem limitar a 100%** para
  que o painel reflita dias acima da meta.
- `stats.week`: soma dos últimos 7 dias, incluindo hoje.
- `stats.year`: total retornado pelo calendário do GitHub para a janela anual.

O arquivo é gerado apenas quando a atualização chega à branch principal. O
caminho público esperado é:

```text
https://raw.githubusercontent.com/juniordev830/juniordev830/main/assets/contribuicoes.json
```

O GitHub pode atrasar o agendamento do workflow e o cache do conteúdo. O
consumidor **não deve inventar contribuições nem substituir silenciosamente
contagens ausentes por zero**: exiba o último `observedOn` conhecido e uma
indicação de dados desatualizados ou indisponíveis. Uma meta é um parâmetro de
exibição, e não a quantidade de commits gerados.

O comentário `CONTRIBUTIONS:METRICS` no README continua disponível para
compatibilidade com a versão anterior do painel, mas clientes novos devem
preferir o JSON estruturado.
