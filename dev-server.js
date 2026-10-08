// Local test server: static files + /api/free-preview.
//   node dev-server.js                 → dry run: nothing is sent, the Resend payload is logged
//   RESEND_API_KEY=re_... RESEND_FROM="Name <you@domain>" node dev-server.js   → sends for real
const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const PORT = Number(process.env.PORT) || 8765;
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json",
  ".webp": "image/webp", ".jpg": "image/jpeg", ".png": "image/png", ".pdf": "application/pdf", ".svg": "image/svg+xml" };

const DRY = !process.env.RESEND_API_KEY;
if (DRY) {
  process.env.RESEND_API_KEY = "dry-run";
  process.env.RESEND_FROM = process.env.RESEND_FROM || "The Ethiopian Codex <dry-run@example.com>";
  process.env.UNSUBSCRIBE_SECRET = process.env.UNSUBSCRIBE_SECRET || "dry-run";
  global.fetch = async (url, opts) => {
    const p = JSON.parse(opts.body);
    console.log("[dry-run]", opts.method, url, "| body:", p.to ? "" : JSON.stringify(p), "| to:", p.to, "| subject:", p.subject,
      "| unsubscribe:", p.headers ? p.headers["List-Unsubscribe"] : "-",
      "| attachment:", p.attachments ? p.attachments[0].filename + " (" + Math.round(p.attachments[0].content.length * 0.75 / 1024) + " KB)" : "-",
      "| idempotency:", opts.headers["Idempotency-Key"] || "-");
    return { ok: true, status: 200, text: async () => "{}" };
  };
}
const API = { "/api/free-preview": require("./api/free-preview.js"), "/api/unsubscribe": require("./api/unsubscribe.js") };

http.createServer((req, res) => {
  const url = new URL(req.url, "http://localhost");
  const handler = API[url.pathname];
  if (handler) {
    req.query = Object.fromEntries(url.searchParams);
    let raw = "";
    req.on("data", (c) => (raw += c));
    req.on("end", () => {
      req.body = raw;
      res.status = (code) => { res.statusCode = code; return res; };
      res.json = (obj) => { res.setHeader("Content-Type", "application/json"); res.end(JSON.stringify(obj)); };
      handler(req, res).catch((e) => { console.error(e); res.statusCode = 500; res.end(); });
    });
    return;
  }
  const file = path.join(ROOT, decodeURIComponent(url.pathname === "/" ? "/sales-page-ES.html" : url.pathname));
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.statusCode = 404; return res.end("Not found"); }
  res.setHeader("Content-Type", TYPES[path.extname(file)] || "application/octet-stream");
  fs.createReadStream(file).pipe(res);
}).listen(PORT, () => console.log(`http://localhost:${PORT}  ${DRY ? "(dry run — no email is sent)" : "(LIVE — emails are sent through Resend)"}`));
