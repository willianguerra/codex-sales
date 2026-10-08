// Signed unsubscribe links. The token proves the link came from one of our emails,
// so nobody can unsubscribe someone else by guessing the URL.
//   UNSUBSCRIBE_SECRET   required  long random string (Vercel → Environment Variables)
const crypto = require("crypto");

function b64url(s) {
  return Buffer.from(s, "utf8").toString("base64url");
}

function sign(email, lang) {
  const secret = process.env.UNSUBSCRIBE_SECRET;
  if (!secret) throw new Error("UNSUBSCRIBE_SECRET is not set");
  return crypto.createHmac("sha256", secret).update(lang + ":" + email).digest("base64url").slice(0, 32);
}

function unsubscribeUrl(siteUrl, email, lang) {
  return siteUrl.replace(/\/$/, "") + "/api/unsubscribe?e=" + b64url(email) + "&l=" + lang + "&t=" + sign(email, lang);
}

// Returns { email, lang } when the link is genuine, otherwise null.
function verify(e, l, t) {
  const lang = l === "ES" ? "ES" : "EN";
  let email;
  try { email = Buffer.from(String(e || ""), "base64url").toString("utf8"); } catch (err) { return null; }
  if (!email || !t) return null;
  const want = Buffer.from(sign(email, lang));
  const got = Buffer.from(String(t));
  if (want.length !== got.length || !crypto.timingSafeEqual(want, got)) return null;
  return { email: email, lang: lang };
}

module.exports = { unsubscribeUrl, verify };
