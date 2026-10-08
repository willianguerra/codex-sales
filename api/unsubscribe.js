// GET  /api/unsubscribe?e=…&l=EN|ES&t=…  → confirmation page with a button (link scanners only GET, so they can't unsubscribe anyone)
// POST /api/unsubscribe?e=…&l=EN|ES&t=…  → marks the Resend contact as unsubscribed
//      Also answers Gmail/Apple one-click unsubscribe (List-Unsubscribe-Post, RFC 8058).
// Unsubscribed contacts are skipped by every Resend broadcast/automation (the email sequence).
const { verify } = require("./_unsubscribe-token.js");
const { support_email: SUPPORT } = require("./_content.js");

const T = {
  EN: {
    lang: "en", title: "Unsubscribe", back: "Back to the site",
    ask: "Stop receiving emails from The Ethiopian Codex at <strong>{email}</strong>?",
    button: "Unsubscribe",
    done: "Done. <strong>{email}</strong> won't receive any more emails from us.",
    bad: "This link is invalid or incomplete. To unsubscribe, write to <a href=\"mailto:{support}\">{support}</a>.",
    fail: "Something went wrong. Please try again, or write to <a href=\"mailto:{support}\">{support}</a> and we'll remove you by hand.",
  },
  ES: {
    lang: "es", title: "Darse de baja", back: "Volver al sitio",
    ask: "¿Dejar de recibir correos de El Códice Etíope en <strong>{email}</strong>?",
    button: "Darme de baja",
    done: "Listo. <strong>{email}</strong> no recibirá más correos nuestros.",
    bad: "Este enlace no es válido o está incompleto. Para darte de baja, escribe a <a href=\"mailto:{support}\">{support}</a>.",
    fail: "Algo salió mal. Inténtalo de nuevo o escribe a <a href=\"mailto:{support}\">{support}</a> y te daremos de baja manualmente.",
  },
};

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function page(res, status, lang, message, form) {
  const t = T[lang];
  res.statusCode = status;
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Robots-Tag", "noindex");
  res.end(`<!doctype html>
<html lang="${t.lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>${t.title}</title>
<style>
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#0F0D0B;color:#E9DCC0;font:18px/1.6 Georgia,"Times New Roman",serif;padding:24px 16px;box-sizing:border-box}
main{max-width:480px;text-align:center}
h1{font-size:26px;font-weight:normal;color:#D9B46A;margin:0 0 16px}
p{margin:0 0 24px}
a{color:#D9B46A}
button{font:700 17px/1.2 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif;background:#D9A441;color:#14100C;border:0;border-radius:8px;padding:16px 28px;min-height:48px;cursor:pointer}
.back{display:inline-block;margin-top:8px;font:14px -apple-system,"Segoe UI",Helvetica,Arial,sans-serif}
</style></head>
<body><main>
<h1>${t.title}</h1>
<p>${message}</p>
${form || ""}
<a class="back" href="/${t.lang}">${t.back}</a>
</main></body></html>`);
}

module.exports = async function handler(req, res) {
  const q = req.query || Object.fromEntries(new URL(req.url, "http://x").searchParams);
  const lang = q.l === "ES" ? "ES" : "EN";
  const t = T[lang];
  const fill = (s, email) => s.replace(/\{email\}/g, esc(email || "")).replace(/\{support\}/g, SUPPORT);

  let who = null;
  try { who = verify(q.e, q.l, q.t); } catch (e) { console.error("unsubscribe:", e.message); }
  if (!who) return page(res, 400, lang, fill(t.bad));

  if (req.method === "GET") {
    const action = "/api/unsubscribe?e=" + encodeURIComponent(q.e) + "&l=" + lang + "&t=" + encodeURIComponent(q.t);
    return page(res, 200, lang, fill(t.ask, who.email),
      `<form method="post" action="${esc(action)}"><button type="submit">${t.button}</button></form>`);
  }
  if (req.method !== "POST") {
    res.setHeader("Allow", "GET, POST");
    return page(res, 405, lang, fill(t.bad));
  }

  const key = process.env.RESEND_API_KEY;
  const headers = { Authorization: "Bearer " + key, "Content-Type": "application/json" };
  try {
    let r = await fetch("https://api.resend.com/contacts/" + encodeURIComponent(who.email), {
      method: "PATCH", headers: headers, body: JSON.stringify({ unsubscribed: true }),
    });
    // Not in Resend yet (e.g. signed up before contacts were stored): create it already unsubscribed,
    // so a later broadcast can't reach them.
    if (r.status === 404) {
      r = await fetch("https://api.resend.com/contacts", {
        method: "POST", headers: headers, body: JSON.stringify({ email: who.email, unsubscribed: true }),
      });
    }
    if (!r.ok) throw new Error("Resend " + r.status + " " + (await r.text()));
  } catch (e) {
    console.error("unsubscribe:", e.message);
    return page(res, 502, lang, fill(t.fail));
  }
  return page(res, 200, lang, fill(t.done, who.email));
};
