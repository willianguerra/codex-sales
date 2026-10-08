# Checkout Hotmart — textos prontos para colar

Preços vêm do `config.json` (EN: bump `$7` · ES: bump `US$ 7`). Ajuste lá e aqui se mudar.

## 1. Personalização visual (Checkout Builder)

| Campo | Valor |
|---|---|
| Cor principal | `#B8893B` |
| Fundo do banner | `#0F0D0B` |
| Banner superior EN (1200 × 300) | `assets/checkout-banner-EN.png` |
| Banner superior ES (1200 × 300) | `assets/checkout-banner-ES.png` |
| Imagem do produto | `assets/cover-EN.webp` / `assets/cover-ES.webp` (exporte para PNG/JPG se a Hotmart não aceitar WebP) |
| Selo de garantia | Ativar o selo de 7 dias ao lado do botão de pagamento |

**Texto do banner (já aplicado nas imagens):**

- EN: **The Ethiopian Codex** — Enoch · Jubilees · Meqabyan — every source cited · Read on your phone
- ES: **El Códice Etíope** — Enoc · Jubileos · Meqabyan — cada fuente citada · Léelo en tu celular

> Mudança em relação ao briefing: o briefing sugeria "81 books explained / 81 libros explicados". O e-book **não explica os 81 livros** (explica Enoque, Jubileus, Meqabyan e o cânone amplo, e mostra como se chega a 81). Para cumprir a regra 1.1 e evitar reembolso por promessa não cumprida, troquei pela lista real.

## 2. Complemento no checkout (order bump)

### EN

**Title:**
YES! Add *The Gospel of Nicodemus* for only $7

**Description:**
The ancient text behind the belief that Jesus descended into the realm of the dead between the Cross and the Resurrection — explained, with sources. A short companion guide (≈ 25 pages). *Note: this text is not part of the Ethiopian 81-book canon.*

### ES

**Título:**
¡SÍ! Agrega *El Evangelio de Nicodemo* por solo US$ 7

**Descripción:**
El texto antiguo detrás de la creencia de que Jesús descendió al lugar de los muertos entre la Cruz y la Resurrección, explicado con fuentes. Una guía breve (≈ 25 páginas). *Nota: este texto no forma parte del canon etíope de 81 libros.*

> A nota "não faz parte do cânone etíope" é coerente com o próprio e-book (Parte IV, afirmação nº 6: a descida aos mortos vem do Evangelho de Nicodemos, que não está em nenhuma das listas etíopes). Mantenha-a.

## 3. Ofertas após a compra (Funil de Vendas Hotmart)

| Etapa | Página | Preço (config) |
|---|---|---|
| Oferta 1 clique (áudio completo) | `upsell-audio-EN.html` / `upsell-audio-ES.html` | `upsell_price` |
| Se recusar → oferta menor (plano de 30 dias em áudio) | `downsell-audio-EN.html` / `downsell-audio-ES.html` | `downsell_price` |

Cole o código do widget de 1 clique da Hotmart (ele já traz os botões "Sim" e "Não") em `config.json → hotmart_widget_html` (`upsell_EN`, `upsell_ES`, `downsell_EN`, `downsell_ES`) e rode `python build.py`. Enquanto estiver vazio, a página mostra um quadro tracejado marcando o lugar do widget.

O link discreto "No thanks" da página de upsell leva para `upsell_next_url` (a oferta menor). Se a Hotmart já controlar o redirecionamento pelo funil, troque esse valor pelo link que ela fornecer.
