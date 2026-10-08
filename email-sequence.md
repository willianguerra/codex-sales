# Sequência de e-mails (quem pegou a isca grátis)

O e-mail do dia 0 sai sozinho pelo Resend. Os dias 2, 4 e 6 você monta no Resend (Automations/Broadcasts) usando os segmentos `Ethiopian Codex — leads EN` e `— leads ES`, que o formulário já alimenta separados por idioma. **Em todo e-mail da sequência, coloque o link de descadastro do Resend `{{{RESEND_UNSUBSCRIBE_URL}}}` no rodapé** — o Resend já pula quem se descadastrou (pelo rodapé de qualquer e-mail, inclusive o do dia 0). Links de checkout com origem `email-{n}`, ex.: `https://pay.hotmart.com/XXXXXXXX?src=email-2`.

| Dia | Assunto EN | Assunto ES | Conteúdo |
|---|---|---|---|
| 0 | Your free preview of The Ethiopian Codex | Tu muestra gratis de El Códice Etíope | **Automático** — enviado na hora pelo `api/free-preview.js` (Resend): prévia de 7 páginas em anexo + como comprar. Template em `emails/` |
| 2 | The Bible verse that quotes a "lost" book | El versículo de la Biblia que cita un libro «perdido» | Judas 1:14 × 1 Enoque 1:9, explicado. Menção leve ao Códice |
| 4 | Fact or hype? 1 viral claim, checked | ¿Verdad o exageración? Una afirmación viral, comprobada | Um item completo do capítulo como degustação + link do checkout (`src=email-3`) |
| 6 | Last note about the Codex | Última nota sobre el Códice | Resumo do conteúdo + garantia de 7 dias + link (`src=email-4`) |

## Notas de conteúdo (conferidas contra o e-book)

- **Dia 0 — prévia.** A prévia contém: capa, sumário, abertura da Parte I, 2 páginas sobre Enoque e as afirmações nº 4 (TRUE) e nº 8 (FALSE) do "Fact or Hype?".
- **Dia 2 — Judas × Enoque.** Use a formulação do e-book: Judas 14–15 "closely matches" 1 Enoque 1:9; em grego os dois trechos partilham cerca de 72% das palavras (Gentry & Fountain 2017). Não diga "palavra por palavra".
- **Dia 4 — item de degustação.** Bom candidato: nº 8, "A council in 363 AD removed these books" (veredito: FALSE). Mostra o método do livro sem citar pessoa famosa. Evite o nº 9 (cita um nome famoso — a regra 1.1 proíbe isso nas páginas; nos e-mails, decida você).
