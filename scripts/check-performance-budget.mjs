import { readdir, stat } from "node:fs/promises";
import path from "node:path";

const outputDirectory = path.resolve("dist");
const files = [];

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  for (const entry of entries) {
    const absolutePath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      await walk(absolutePath);
    } else if (entry.isFile()) {
      const metadata = await stat(absolutePath);
      files.push({
        path: path.relative(outputDirectory, absolutePath),
        bytes: metadata.size,
        extension: path.extname(entry.name).toLowerCase(),
      });
    }
  }
}

const formatBytes = (bytes) =>
  bytes >= 1024 * 1024
    ? `${(bytes / (1024 * 1024)).toFixed(2)} MiB`
    : `${(bytes / 1024).toFixed(1)} KiB`;

await walk(outputDirectory);

if (files.length === 0) {
  throw new Error("No generated files found in dist/");
}

const groups = {
  html: files.filter((file) => file.extension === ".html"),
  css: files.filter((file) => file.extension === ".css"),
  js: files.filter((file) => file.extension === ".js" || file.extension === ".mjs"),
  images: files.filter((file) => [".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg"].includes(file.extension)),
  fonts: files.filter((file) => [".woff", ".woff2", ".ttf", ".otf"].includes(file.extension)),
};

const limits = {
  total: 8 * 1024 * 1024,
  html: 250 * 1024,
  css: 200 * 1024,
  js: 300 * 1024,
  image: 1536 * 1024,
  fonts: 500 * 1024,
};

const sum = (items) => items.reduce((total, file) => total + file.bytes, 0);
const errors = [];
const warnings = [];
const totalBytes = sum(files);

if (totalBytes > limits.total) {
  errors.push(`Total output ${formatBytes(totalBytes)} exceeds ${formatBytes(limits.total)}`);
}

for (const [name, items] of Object.entries(groups)) {
  const bytes = sum(items);
  const limit = limits[name];
  if (limit !== undefined && bytes > limit) {
    errors.push(`${name} total ${formatBytes(bytes)} exceeds ${formatBytes(limit)}`);
  }
}

for (const image of groups.images) {
  if (image.bytes > limits.image) {
    errors.push(`Image ${image.path} (${formatBytes(image.bytes)}) exceeds ${formatBytes(limits.image)}`);
  } else if (image.bytes > 350 * 1024) {
    warnings.push(`Large image: ${image.path} (${formatBytes(image.bytes)}); consider a modern compressed format and responsive variants when it is used`);
  }
}

console.log("Static output size report:");
console.log(`- Total: ${formatBytes(totalBytes)} across ${files.length} files`);
for (const [name, items] of Object.entries(groups)) {
  console.log(`- ${name}: ${formatBytes(sum(items))} across ${items.length} files`);
}
for (const warning of warnings) console.warn(`WARNING: ${warning}`);

if (errors.length > 0) {
  console.error("Static performance budget failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exitCode = 1;
} else {
  console.log("Static performance budgets passed.");
}
