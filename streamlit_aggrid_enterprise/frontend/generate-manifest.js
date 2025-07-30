const fs = require("fs");
const path = require("path");

function createManifest(distDir) {
  const manifest = {};
  const files = fs.readdirSync(distDir);

  for (const file of files) {
    if (file.endsWith(".js")) manifest["main.js"] = file;
    if (file.endsWith(".css")) manifest["style.css"] = file;
  }

  const manifestPath = path.join(distDir, "manifest.json");
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log(`✅ manifest.json generated in ${distDir}`);
}

const aggridPath = path.join(__dirname, "dist/aggrid");
const chartPath = path.join(__dirname, "dist/chart");

if (fs.existsSync(aggridPath)) createManifest(aggridPath);
if (fs.existsSync(chartPath)) createManifest(chartPath);
