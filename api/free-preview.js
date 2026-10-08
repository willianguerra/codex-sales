// POST /api/free-preview  —  { email, language: "EN" | "ES", consent: "yes", website: "" }
// Sends the free-preview email (template + preview PDF in the visitor's language) through Resend.
//
// Environment variables (Vercel → Project → Settings → Environment Variables):
//   RESEND_API_KEY            required  re_...
//   RESEND_FROM               required  "The Ethiopian Codex <codex@your-verified-domain.com>"
//   RESEND_REPLY_TO           optional  support address that receives replies
//   RESEND_AUDIENCE_ID_EN     optional  Resend audience that collects EN leads (for the email sequence)
//   RESEND_AUDIENCE_ID_ES     optional  same for ES
const CONTENT = require("./_content.js");

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function resend(path, key, payload, extraHeaders) {
  return fetch("https://api.resend.com" + path, {
    method: "POST",
    headers: Object.assign({ Authorization: "Bearer " + key, "Content-Type": "application/json" }, extraHeaders || {}),
    body: JSON.stringify(payload),
  });
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  let body = req.body || {};
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch (e) { body = {}; }
  }

  // Bots fill the hidden "website" field; answer as if it worked and send nothing.
  if (body.website) return res.status(200).json({ ok: true });

  const email = String(body.email || "").trim().toLowerCase();
  const lang = String(body.language || "").toUpperCase() === "ES" ? "ES" : "EN";
  if (email.length > 254 || !EMAIL_RE.test(email)) return res.status(400).json({ ok: false, error: "invalid_email" });
  if (body.consent !== "yes") return res.status(400).json({ ok: false, error: "consent_required" });

  const key = process.env.RESEND_API_KEY;
  const from = process.env.RESEND_FROM;
  if (!key || !from) {
    console.error("free-preview: RESEND_API_KEY or RESEND_FROM is not set");
    return res.status(500).json({ ok: false, error: "not_configured" });
  }

  const c = CONTENT[lang];
  const message = {
    from: from,
    to: [email],
    subject: c.subject,
    html: c.html,
    text: c.text,
    attachments: [{ filename: c.filename, content: c.pdf_base64 }],
    tags: [{ name: "flow", value: "free_preview" }, { name: "lang", value: lang }],
  };
  if (process.env.RESEND_REPLY_TO) message.reply_to = process.env.RESEND_REPLY_TO;

  // Same address + language within 24 h is sent only once (double clicks, refreshes).
  const day = new Date().toISOString().slice(0, 10);
  const sent = await resend("/emails", key, message, { "Idempotency-Key": "free-preview/" + lang + "/" + day + "/" + email });
  if (!sent.ok) {
    console.error("free-preview: Resend " + sent.status + " " + (await sent.text()));
    return res.status(502).json({ ok: false, error: "send_failed" });
  }

  // Keep the lead for the follow-up sequence. A failure here never blocks the visitor.
  const audience = process.env["RESEND_AUDIENCE_ID_" + lang];
  if (audience) {
    try {
      const r = await resend("/audiences/" + audience + "/contacts", key, { email: email, unsubscribed: false });
      if (!r.ok) console.error("free-preview: contact " + r.status + " " + (await r.text()));
    } catch (e) {
      console.error("free-preview: contact error", e);
    }
  }

  return res.status(200).json({ ok: true });
};
