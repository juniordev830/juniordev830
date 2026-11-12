# Diagnóstico de contribuições no GitHub

Este projeto apresenta **dois indicadores diferentes**: o calendário oficial do perfil GitHub e o painel SVG/JSON do README. O painel é gerado por `scripts/render_daily_contributions.py` a partir da API GraphQL `contributionsCollection.contributionCalendar` e não deve somar commits por conta própria.

## Verificação rápida

1. Compare o [calendário oficial](https://github.com/juniordev830?tab=overview) com o campo `today` em [assets/contribuicoes-diarias.json](../assets/contribuicoes-diarias.json). Os números podem demorar a atualizar.
2. Abra o [workflow de atualização](https://github.com/juniordev830/juniordev830/actions/workflows/contribuicoes-diarias.yml) e confirme uma execução recente **concluída com sucesso** na `main`. O agendamento de cinco minutos é aproximado: o GitHub pode atrasar ou descartar execuções agendadas em períodos de carga.
3. Compare o JSON com a imagem `assets/contribuicoes-diarias.svg` e com o comentário `CONTRIBUTIONS:METRICS` do README. Se o JSON estiver atualizado e o painel externo não, o problema provavelmente está no cache ou no consumo do JSON pelo site externo.
4. Se o workflow falhar, leia o log da etapa de consulta GraphQL, os testes e o resultado do push. Não substitua falhas por valores estimados.
5. Se o workflow estiver correto, mas o calendário oficial não refletir um commit, verifique o e-mail do autor do commit, se ele está associado à conta, se o commit está na branch padrão (ou `gh-pages`) e se o repositório é fork. Pull Requests e issues têm regras próprias de contagem.

## Atenção à autoria e aos merges

- Um commit feito em uma branch de trabalho não necessariamente aparece no calendário até chegar à branch padrão.
- Commits produzidos pelo usuário `github-actions[bot]` não devem ser tratados como contribuições pessoais de `juniordev830`.
- Um merge não garante que cada commit resultará em uma nova contribuição; autoria, e-mail, branch e regras do GitHub importam.
- Não altere datas ou autoria e não crie commits vazios para inflar o gráfico.

## Diagnóstico desta revisão (12/11/2026)

- O README consultado apresentava **153** contribuições para 12/11, **758** nos últimos sete dias e **2.378** nos últimos doze meses. São valores do painel publicado, não uma nova consulta autenticada ao calendário oficial.
- Os commits dos PRs #30 a #33 de `pixel-farm-seasons` estão na `main` daquele projeto. A atribuição individual deles ao gráfico precisa ser conferida no GitHub.
- O gerador só grava o README quando o conteúdo muda; um painel sem novo commit de atualização pode significar simplesmente que a API retornou os mesmos números.

## Critério de resolução

A correção estará confirmada quando calendário oficial, JSON e SVG apresentarem os mesmos totais para a mesma data e quando o painel externo exibir os valores do JSON sem cache antigo. Registrar horário da coleta, URL da execução e diferenças observadas antes de encerrar o incidente.
