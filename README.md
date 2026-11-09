# Abbas Lotfi Nasab — Personal Brand Website

Astro-powered, Persian-first personal website for Abbas Lotfi Nasab.

## Stack

- Astro + TypeScript
- Static Site Generation (SSG)
- Persian-first, RTL-aware interface
- Markdown/MDX content collections for projects and insights
- Static SEO metadata, sitemap, robots.txt, and output validation

## Positioning

**Digital Business Architect · Founder · Product Builder**

The site focuses on business architecture, digital product strategy, practical AI and automation, and hospitality technology.

## Development

Requirements: Node.js 22 or newer.

```bash
npm install
npm run dev
npm run check
npm run build
npm run validate:output
npm run validate:performance
npm run preview
```

## Content

- Projects: `src/content/projects/`
- Insights: `src/content/insights/`
- Collection schemas: `src/content.config.ts`
- Authoring guidance: `docs/content-authoring/`

Only content marked `status: published` is included in the generated site. Publish verified information only; do not invent dates, results, client details, or project claims.

## Repository structure

- `src/`: Astro pages, components, layouts, data, styles, and content
- `static/`: public static assets
- `scripts/`: generated-output validation and performance budgets
- `docs/`: audit, migration, phase notes, and authoring guidance

The retired Django application and its unused templates/assets have been removed. There is no live database or Production content source to migrate.

## Validation

GitHub Actions runs dependency installation and audit, Astro checks/build, generated-route and internal-reference validation, and static output size budgets.

## Deployment

This repository currently builds a static site. No deployment, hosting, DNS, or Production changes are performed by the validation workflow. Configure a static host only after separate release approval.

## Documentation

- [Repository audit](docs/REDESIGN_AUDIT.md)
- [Content and URL migration register](docs/CONTENT_MIGRATION.md)
- [Phase 9 performance guardrails](docs/PHASE_9_PERFORMANCE_GUARDRAILS.md)
- [Legacy cleanup record](docs/LEGACY_CLEANUP.md)
