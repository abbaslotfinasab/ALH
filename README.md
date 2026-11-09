# Abbas Lotfi Nasab — Personal Brand Website

This repository is being transitioned from the legacy Django-powered personal website to a statically generated Astro website.

## Redesign direction

- **Positioning:** Digital Business Architect · Founder & Product Builder
- **Focus:** AI-driven business systems, digital product architecture, and hospitality technology
- **Framework target:** Astro + TypeScript
- **Rendering target:** Static Site Generation (SSG)
- **Design direction:** Evolve the existing visual identity (Persian-first, RTL-aware, navy/teal palette, restrained UI)
- **Deployment:** Static hosting after migration and review

## Repository status

The current application source is the legacy Django website. It is intentionally retained while the new static site is prepared.

No Production services, DNS records, database records, or deployed files are changed by work on the redesign branch.

## Content architecture

- Editorial content is managed as Markdown/MDX in `src/content/projects/` and `src/content/insights/`.
- Only entries with `status: published` are included in static output.
- Collection schemas live in `src/content.config.ts`; filenames define URL slugs.
- There is no Production database or live content source to migrate from. Add only verified content; do not create placeholder articles or project claims.

## Documentation

- [Repository audit](docs/REDESIGN_AUDIT.md)
- [Content and URL migration register](docs/CONTENT_MIGRATION.md)

## Working branch

Active redesign work is isolated in `redesign/static-brand`. The `main` branch remains the production baseline until the redesign has been implemented, tested, reviewed, and explicitly approved for release.

## Planned static-site commands

Astro scaffold is now present on the redesign branch. Run these commands from the repository root:

```bash
npm install
npm run dev
npm run build
npm run preview
```

Do not run these commands against the legacy Django app. Install dependencies and run the Astro checks before considering the branch ready to merge.
