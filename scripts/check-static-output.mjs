import { readdir, readFile, stat } from "node:fs/promises";
import path from "node:path";

const outputDirectory = path.resolve("dist");
const errors = [];
const htmlFiles = [];

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  for (const entry of entries) {
    const absolutePath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      await walk(absolutePath);
    } else if (entry.isFile() && entry.name.endsWith(".html")) {
      htmlFiles.push(absolutePath);
    }
  }
}

async function exists(filePath) {
  try {
    return (await stat(filePath)).isFile();
  } catch {
    return false;
  }
}

function localTarget(rawValue) {
  if (!rawValue || rawValue.startsWith("#") || rawValue.startsWith("//")) return null;
  if (/^(mailto:|tel:|sms:|javascript:|data:)/i.test(rawValue)) return null;

  let pathname;
  try {
    const parsed = new URL(rawValue, "https://abbaslotfinasab.ir");
    if (parsed.origin !== "https://abbaslotfinasab.ir") return null;
    pathname = decodeURIComponent(parsed.pathname);
  } catch {
    errors.push(`Invalid URL in generated HTML: ${rawValue}`);
    return null;
  }

  return pathname;
}

await walk(outputDirectory);

if (htmlFiles.length === 0) {
  throw new Error("No generated HTML files found in dist/");
}

for (const htmlFile of htmlFiles) {
  const html = await readFile(htmlFile, "utf8");
  const source = path.relative(outputDirectory, htmlFile);

  if (!/<title>\\s*[^<]+\\s*<\\/title>/i.test(html)) {
    errors.push(`${source}: missing or empty page title`);
  }

  const descriptions = [...html.matchAll(/<meta\\s+name=["']description["']\\s+content=["']([^"']*)["'][^>]*>/gi)];
  if (descriptions.length !== 1 || !descriptions[0][1].trim()) {
    errors.push(`${source}: expected exactly one non-empty meta description`);
  }

  const canonicals = [...html.matchAll(/<link\\s+rel=["']canonical["']\\s+href=["']([^"']+)["'][^>]*>/gi)];
  if (canonicals.length !== 1) {
    errors.push(`${source}: expected exactly one canonical URL`);
  } else {
    try {
      const canonicalUrl = new URL(canonicals[0][1]);
      if (canonicalUrl.origin !== "https://abbaslotfinasab.ir") {
        errors.push(`${source}: canonical URL is outside the configured site origin`);
      }
    } catch {
      errors.push(`${source}: canonical URL is not absolute and valid`);
    }
  }

  const imagesWithoutAlt = [...html.matchAll(/<img\\b(?![^>]*\\balt=)[^>]*>/gi)];
  if (imagesWithoutAlt.length > 0) {
    errors.push(`${source}: ${imagesWithoutAlt.length} image(s) missing alt attributes`);
  }

  const attributes = html.matchAll(/\b(?:href|src)\s*=\s*["']([^"'<>]+)["']/gi);

  for (const [, rawValue] of attributes) {
    const pathname = localTarget(rawValue);
    if (pathname === null) continue;

    const relativePath = pathname.replace(/^\/+/, "");
    const candidates = pathname.endsWith("/")
      ? [path.join(outputDirectory, relativePath, "index.html")]
      : [
          path.join(outputDirectory, relativePath),
          path.join(outputDirectory, relativePath, "index.html"),
        ];

    let found = false;
    for (const candidate of candidates) {
      if (await exists(candidate)) {
        found = true;
        break;
      }
    }

    if (!found) {
      const source = path.relative(outputDirectory, htmlFile);
      errors.push(`${source}: broken local reference "${rawValue}"`);
    }
  }
}

for (const requiredFile of [
  "index.html",
  "about/index.html",
  "ventures/index.html",
  "experience/index.html",
  "insights/index.html",
  "projects/index.html",
  "contact/index.html",
  "robots.txt",
  "sitemap.xml",
]) {
  if (!(await exists(path.join(outputDirectory, requiredFile)))) {
    errors.push(`Missing required output: ${requiredFile}`);
  }
}

const sitemap = await readFile(path.join(outputDirectory, "sitemap.xml"), "utf8");
if (!sitemap.includes("<urlset") || !sitemap.includes("https://abbaslotfinasab.ir/")) {
  errors.push("sitemap.xml is missing a valid urlset or the canonical site homepage");
}

if (errors.length > 0) {
  console.error("Static output validation failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exitCode = 1;
} else {
  console.log(`Static output validation passed: ${htmlFiles.length} HTML files, required routes, robots.txt, sitemap.xml, and local href/src references.`);
}
