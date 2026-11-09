# Phase 7 — Technical SEO & Static Output Validation

## Delivered
- Added a statically generated `/sitemap.xml` endpoint.
- Sitemap includes the seven verified top-level routes and only published project/insight entries.
- Published editorial entries include `lastmod` when a verified `updatedAt` or `publishedAt` value exists.
- Added `/robots.txt` with crawl access and the canonical sitemap URL.
- Added a Node-based static-output validator that checks required route files, robots/sitemap output, and local `href`/`src` references in generated HTML.
- Extended GitHub Actions to run the static-output validator after the Astro build.

## Validation scope and limitations
- The validator checks references that resolve to generated files; it does not crawl the public internet or assert that third-party links remain available.
- No editorial entries currently exist in either content collection, so the sitemap will include the seven static routes until verified content is added.
- Legacy dynamic URLs and record-level redirects remain a separate migration task. There is no live database or production content export from which to infer missing slugs; do not create blanket redirects or invent old URL mappings.
- Canonical URLs in content metadata should be reviewed before publishing entries, especially if they point outside the canonical site.
- Browser/device testing, Lighthouse/Core Web Vitals, font licensing review, and social-image dimension checks remain separate release gates.
- A dependency lockfile is still not present; CI currently uses `npm install`, not `npm ci`.

## Production safety
All changes are isolated to `redesign/static-brand`. No merge, deployment, DNS, hosting, or Production changes were performed.
