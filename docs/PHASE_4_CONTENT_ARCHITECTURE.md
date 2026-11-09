# Phase 4 — Static Content Architecture

## Delivered
- Added Astro build-time content collections for projects and insights.
- Added typed frontmatter schemas for titles, summaries, publication status, dates, tags, SEO metadata, canonical paths, and project/article-specific fields.
- Added project and insight index pages that show only entries marked published.
- Added static detail routes at /projects/<slug>/ and /insights/<slug>/.
- Added editorial layouts for listing cards and long-form content.
- Added content-authoring guides under src/content/projects/ and src/content/insights/.
- Connected the experience page to the project archive.
- Updated the migration documentation: there is no Production database or live content source to export from.

## Publishing rules
- Markdown/MDX files are the content source of truth.
- The file name defines the URL slug.
- New entries default to draft; draft entries are excluded from generated public pages.
- Dates, canonical paths, SEO fields, image rights, and factual descriptions must be reviewed before publication.
- No sample articles, invented project details, or placeholder publication dates were added.

## Not included
- No CMS, database, API, authentication, comments, or runtime content service.
- No legacy database export or database migration.
- No redirects have been invented; legacy route mapping remains dependent on verified source paths and actual content.
- No Production hosting, DNS, deployment, or live site changes.

## Validation status
- Astro Content Collections APIs were checked against the current Astro documentation.
- The astro/zod export is used for schema definitions.
- A GitHub Actions build is required to confirm TypeScript diagnostics and static route generation after these changes.
- Browser/device visual QA remains outstanding.