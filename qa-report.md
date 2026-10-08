# QA — Página de vendas "The Ethiopian Codex / El Códice Etíope"

Data: 2026-10-08 · Conferido contra `the-ethiopian-codex-EN.pdf` (100 p.) e `the-ethiopian-codex-ES.pdf` (103 p.), edição 1.0.

## ⚠️ Antes de publicar (pendências do dono)

| # | O que falta | Onde |
|---|---|---|
| 1 | Links reais de checkout Hotmart EN e ES | `config.json → EN/ES.checkout_url` |
| 2 | Preço principal definido: **$17.99** (EN) / **US$ 17,99** (ES). Confirmar se a Hotmart vai cobrar em dólar no ES ou em moeda local; bump/upsell/downsell ainda provisórios | `config.json → *price` |
| 3 | Nome da marca e e-mail de suporte (hoje: `The Ethiopian Codex` / `support@example.com`) | `config.json → brand_name, support_email` |
| 4 | URL do site (para Open Graph e hreflang) | `config.json → site_url` |
| 5 | **Resend:** verificar um domínio de envio (a conta Resend conectada aqui não tem nenhum domínio — sem isso o Resend só envia para o seu próprio e-mail) e definir `RESEND_API_KEY` e `RESEND_FROM` na hospedagem | Resend → Domains; ver `README.md` |
| 6 | Páginas de Termos e Privacidade | `config.json → legal_urls` |
| 7 | ~~PDF da isca~~ → resolvido: a isca agora é a **prévia de 7 páginas** (EN/ES) enviada por e-mail via Resend, com instruções de compra | `api/free-preview.js` |
| 8 | Produtos ainda não fornecidos: guia de Nicodemos (bump), audiolivro (upsell), plano de 30 dias em áudio (downsell). Não ative essas ofertas na Hotmart antes de existirem | Hotmart |
| 9 | Widgets de 1 clique da Hotmart | `config.json → hotmart_widget_html` |
| 10 | Tirar `noindex` quando sair do teste | `config.json → noindex: false` |
| 11 | Pixels (opcional) | `config.json → pixels` |

Depois de editar o `config.json`: `python build.py`.

## [VERIFICAR] resolvidos

| Item do briefing | Resultado (fonte no PDF) |
|---|---|
| Nº de páginas | EN **100**, ES **103** |
| "Why 81 Books?" — nº e nuance | Mantido "81", com a nuance do livro: "os 81 livros" é o nome que a Igreja dá à sua Bíblia, e listas diferentes chegam a 81 de formas diferentes (EN p. 11–12, Cowley 1974) |
| Frase Judas × Enoque | Briefing dizia "almost word for word". O livro diz "closely matches" e "cerca de 72% das palavras em grego" (EN p. 32, 62). Página usa a formulação do livro |
| Versículo ES (RV 1909) | Usado exatamente como no e-book ES (p. 33): "…también profetizó Enoc, séptimo desde Adam, diciendo: He aquí, el Señor es venido con sus santos millares…". Obs.: a RV 1909 impressa grafa "Enoch"; o e-book modernizou para "Enoc". Mantive igual ao livro por coerência |
| Trecho de Enoque | EN: Charles 1917 ("And behold! He cometh with ten thousands of His holy ones…"); ES: tradução do e-book a partir de Charles |
| 3 itens do "Fact or Hype?" | Nºs 2, 8 e 6, com o texto exato do livro, **sem veredito** (selos com "?"). Briefing citava "A council banned the Book of Enoch"; no livro é "A council in 363 AD removed these books" — usei o do livro |
| Nome do capítulo ES | O livro usa "¿Verdad o exageración?" (não "¿Hecho o Exageración?"). Página alinhada ao livro |
| Arcanjos (isca original — substituída pela prévia do livro) | 1 Enoque 20 nomeia **7**: Uriel, Raphael, Raguel, Michael, Saraqael, Gabriel, Remiel (EN p. 26). "7" confirmado |
| "Texto completo de Enoque?" | Resposta reescrita: não o livro inteiro; explica os trechos-chave, **imprime 11 passagens completas** (Parte V) e o plano de 30 dias diz que capítulos ler |

## Promessas da página × conteúdo do PDF

| Promessa | Existe no PDF? |
|---|---|
| Fonte citada em cada afirmação, caixas de fonte | ✅ ("A Note on Sources", caixas 📜 em todo o livro) |
| Vigilantes, Nefilins, arcanjos, viagens de Enoque | ✅ Parte I |
| Jubileus, "Little Genesis" | ✅ Parte II |
| Três livros de Meqabyan ≠ Macabeus | ✅ Parte III |
| 10 afirmações com veredito | ✅ Parte IV |
| 11 passagens completas | ✅ Parte V (acrescentado à página — não estava no briefing) |
| Plano de 30 dias, glossário, bibliografia | ✅ Apêndices A, B, D |
| "Echoes in Your Bible" | ✅ Apêndice C (acrescentado à página) |
| Feito para ler no celular | ✅ formato 6×9 pol. |

Títulos dos cards do bloco 5 seguem o sumário real (Opening, Parts I–V, Appendices), com os numerais ge'ez ፩–፭ que o próprio livro usa.

## Imagens (seção 3.4)

| ID | Arquivo | Origem |
|---|---|---|
| PG-01 | `pg-01-{EN,ES}.webp` | Capa (p. 1) |
| PG-02 | `pg-02-*` | Abertura da Parte I (p. 17) |
| PG-03 | `pg-03-*` | Citação de Atos 8:27 + caixa de fonte (p. 9) |
| PG-04 | `pg-04-*` | Judas × Enoque (EN p. 32 / ES p. 33) |
| PG-05 | `pg-05-*` | "Fact or Hype?" nº 4 com selo (EN p. 62 / ES p. 64) — o nº 4 não é um dos 3 teasers, então mostrar o veredito não estraga a surpresa |
| PG-06 | `pg-06-*` | Plano de 30 dias (EN p. 88 / ES p. 90) |
| MK-01 | — | Celular em CSS com a capa real (mais leve e nítido que imagem; melhor LCP) |
| MK-02 | — | Mesa escura + vela + tablet + celular em CSS, com páginas reais |
| CV-01 | `cover-*.webp`, `cover-thumb-*.webp` | Capa |
| OG | `og-{EN,ES}.jpg` 1200×630 | Capa + 2 páginas internas |
| Banner checkout | `checkout-banner-{EN,ES}.png` 1200×300 | Ver `checkout-copy.md` |

Páginas exportadas a 1080 px de largura, WebP. Nenhum placeholder restante.

## Checklist (seção 13)

**Conversão**
- [x] Produto claro em 3 s (selo + H1 + capa no celular)
- [x] Botão visível sem rolar — medido: 360×640 (botão termina em 426 px), 390×844 (742), 430×932 (752). Em telas baixas o botão sobe para antes do mockup
- [x] Barra fixa aparece após o botão do topo e some na seção de oferta, no CTA final, na captura de e-mail e no rodapé
- [x] Carrossel com páginas reais, `scroll-snap`, deslizar com o dedo, setas de 52 px, contador "1 / 6", setas do teclado
- [x] Microtexto de garantia sob todos os botões
- [x] Captura de e-mail no fim, sem pop-up, com consentimento e mensagem de sucesso sem recarregar
- [x] Envio via Resend testado em modo simulado: ES recebe `el-codice-etiope-muestra-ES.pdf` (239 KB), EN recebe `the-ethiopian-codex-preview-EN.pdf` (178 KB); e-mail inválido → 400, sem consentimento → 400, bot (campo oculto) → 200 sem envio; mesmo e-mail no mesmo dia não é reenviado (Idempotency-Key)
- [ ] Envio real pelo Resend — depende do domínio verificado

**Honestidade**
- [x] Nenhum depoimento, contador, escassez ou contagem regressiva. Componente de depoimentos pronto e desligado (`show_testimonials: false`; preencher `src/testimonials.{EN,ES}.json` só com depoimentos reais e autorizados)
- [x] Sem "shocking/terrifying/aterrador", "segredos escondidos" etc. Nenhum nome famoso
- [x] Sem preço riscado (`anchor_price: null`) → usa "Less than the price of a lunch"
- [x] "Only available on this page" no upsell **desligado** (`upsell_only_here: false`) até a oferta estar configurada assim
- [x] Aviso legal no rodapé
- [ ] Pendências 1–11 acima

**Técnica**
- [x] 360 / 390 / 430 px sem rolagem horizontal; desktop centralizado em 680 px
- [ ] Testar dentro do navegador do app do YouTube (Android e iPhone) — precisa estar publicado
- [x] Peso: HTML ≈ 54 KB (CSS e JS inline) + capa 20 KB + 1ª página do carrossel 34 KB; demais imagens com `loading="lazy"`. Bem abaixo de 800 KB. Mockup do topo com `fetchpriority="high"`; todas as imagens com `width`/`height`
- [x] Fontes Google com `display=swap`, só os pesos usados; ge'ez carregado só com os glifos usados (`&text=`)
- [x] `src`, `sck` e `utm_*` repassados a todos os botões; sem `src` → `src=salespage` (testado com `?src=yt-test-desc-lp`)
- [x] Links de checkout separados por idioma (via `config.json`)
- [ ] Open Graph: testar colando o link no WhatsApp depois de publicar
- [x] `lang`, `title`, `description`, OG, `hreflang` EN↔ES, `prefers-reduced-motion`, foco visível, alvos de toque ≥ 48 px
- [x] Teste A/B: `headline_variant` ("A"/"B") e `proof_before_preview` (ordem dos blocos 3 e 4) no `config.json`

**Funil**
- [x] `checkout-copy.md` com banner, cores e complemento
- [x] Upsell e oferta menor EN/ES com espaço do widget Hotmart marcado
- [x] Sequência de 4 e-mails em `email-sequence.md`
