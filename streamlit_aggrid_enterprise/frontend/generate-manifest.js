// frontend/generate-manifest.js
const fs = require("fs");
const path = require("path");

const distDir = path.join(__dirname, "dist");
const manifest = {};

fs.readdirSync(distDir).forEach((file) => {
  if (file.endsWith(".js") && file.startsWith("frontend.")) {
    manifest["main.js"] = file;
  }
  if (file.endsWith(".css") && file.startsWith("frontend.")) {
    manifest["style.css"] = file;
  }
});

fs.writeFileSync(
  path.join(distDir, "manifest.json"),
  JSON.stringify(manifest, null, 2)
);

console.log("✅ Hashed manifest.json generated!");
