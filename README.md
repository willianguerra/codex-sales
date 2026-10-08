# The Ethiopian Codex — páginas de vendas (EN / ES)

## Estrutura
 
| Caminho | O que é |
|---|---|
| `sales-page-EN.html`, `sales-page-ES.html` | Páginas de vendas (geradas) |
| `upsell-audio-*.html`, `downsell-audio-*.html` | Ofertas após a compra (geradas) |
| `emails/free-preview-*.html` | Template do e-mail da prévia grátis (gerado — abra no navegador para ver) |
| `api/free-preview.js` | Função que envia o e-mail pelo **Resend** com a prévia em PDF no idioma do visitante |
| `api/unsubscribe.js` | Link de descadastro do rodapé (e botão nativo do Gmail): marca o contato como `unsubscribed` no Resend |
| `emails/sequence-footer-*.html` | Rodapé com link de descadastro para colar nos e-mails da sequência (gerado) |
| `api/_content.js` | Gerado: assunto, HTML, texto e PDF (base64) do e-mail |
| `previews/` | PDFs de prévia anexados ao e-mail |
| `config.json` | Preços, links, URLs, pixels, testes A/B |
| `src/copy.EN.json`, `src/copy.ES.json` | Todos os textos (página + e-mail) |
| `src/styles.css`, `src/main.js` | Estilo e scripts (vão inline nas páginas) |
| `build.py` | Monta tudo |
| `dev-server.js` | Servidor local de teste |

Mudou texto, preço ou PDF de prévia? Rode:

```bash
python build.py
```

## Testar localmente

```bash
node dev-server.js
```

Abra http://localhost:8765. Sem `RESEND_API_KEY` ele roda em **modo simulado**: nada é enviado, e o terminal mostra o que iria para o Resend (destinatário, assunto, anexo).

## Publicar (Vercel)

A função `api/free-preview.js` segue o formato da Vercel (pasta `api/`). As páginas são estáticas.

1. **Resend → Domains:** adicione e verifique o domínio de envio (registros DNS). Sem domínio verificado, o Resend só entrega para o e-mail do dono da conta.
2. **Resend → API Keys:** crie uma chave com permissão de envio.
3. **Resend → Segments:** já existem `Ethiopian Codex — leads EN` e `— leads ES`. O formulário salva cada lead no segmento do idioma, com o link de descadastro dele na propriedade `unsubscribe_url`.
4. **Vercel → Settings → Environment Variables:**

   | Variável | Exemplo |
   |---|---|
   | `RESEND_API_KEY` | `re_...` |
   | `RESEND_FROM` | `The Ethiopian Codex <noreply@ethiopian-codex.com>` |
   | `RESEND_REPLY_TO` | não usado: o e-mail de prévia sai de `noreply@` (o suporte é `suporte@ethiopian-codex.com`, caixa no Resend) |
   | `RESEND_SEGMENT_ID_EN` / `RESEND_SEGMENT_ID_ES` | IDs dos segmentos de leads |
   | `UNSUBSCRIBE_SECRET` | texto aleatório longo que assina os links de descadastro (não troque: invalida os links já enviados) |

5. Em `config.json`, ajuste `site_url` (o e-mail usa essa URL para mostrar a capa), os links de checkout e o resto das pendências listadas em `qa-report.md`. Rode `python build.py` e publique.

Todo e-mail tem link de descadastro no rodapé (na sequência, via `{{{contact.unsubscribe_url}}}`). O do dia 0 também tem o cabeçalho `List-Unsubscribe` (botão "Cancelar inscrição" do Gmail). Quem se descadastra fica `unsubscribed` no Resend e é pulado por qualquer broadcast ou automação.

O mesmo e-mail no mesmo idioma recebe a prévia no máximo uma vez por dia (Idempotency-Key do Resend). Um campo oculto barra bots simples; se aparecer abuso, adicione um rate limit na Vercel (Firewall).
