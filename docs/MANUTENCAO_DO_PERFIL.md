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
