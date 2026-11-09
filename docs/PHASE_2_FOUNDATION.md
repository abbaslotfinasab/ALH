# Phase 2 — Astro Foundation & Design System

## Decisions
- Astro 7.4.7 with TypeScript 5.9.x.
- Static output only (`output: "static"`).
- Existing legacy assets remain under `static/`; Astro copies that directory as the public asset directory.
- No Django, database, API, server-side runtime, or third-party UI framework is required by the new site.
- Persian-first, RTL layout.
- Existing brand navy and teal palette retained and refined.
- Existing Django source, templates, migrations, and media references remain untouched.

## Implemented foundation
- Astro project manifest and configuration.
- Shared TypeScript profile, navigation, venture, and principles data.
- Global design tokens and responsive component styles.
- Shared layout, navigation, and footer.
- Static pages: home, about, ventures, experience, insights, and contact.
- SEO title, description, canonical, Open Graph, Twitter card, and favicon defaults.
- Accessible skip link, semantic landmarks, keyboard focus, reduced-motion support, and responsive mobile navigation.

## Existing assets
The existing `static/images/` files are preserved and served from `/images/` by Astro's configured public directory. The existing logo, hero image, and favicon can be reviewed and reused without copying or deleting their source files.

The old stylesheet remains present for legacy reference but is not imported into the new site.

## Deferred items
- Local font files are not present in the inspected repository. The new CSS uses a Vazirmatn/Vazir-first font stack with system fallbacks; font self-hosting requires adding properly licensed font files.
- Production database and uploaded media exports are not part of this phase.
- Experience and Insights records need a read-only export and content review before migration.
- Analytics scripts were intentionally not copied; measurement IDs, consent, and privacy behavior require an explicit decision.
- No redirects or DNS/deployment changes are included.
- No production environment was accessed or modified.

## Validation
GitHub source files were added, but no local npm install, Astro check, build, browser, or Lighthouse run was executed in this phase. Those checks must be run in a local/CI environment before merge.

## Verified CI result (2026-11-09)

- GitHub Actions workflow: `.github/workflows/astro-static.yml`
- Result: passed.
- Astro diagnostics: 0 errors, 0 warnings, 0 hints.
- Static output: 6 routes generated and verified.
- npm security audit: 0 vulnerabilities after upgrading to the patched Astro toolchain.
- Runtime output: static HTML; no server adapter is configured.

## Remaining foundation hardening

- Commit and maintain `package-lock.json` before production deployment for deterministic installs.
- Review the final font licensing and add local WOFF2 files.
- Run visual/browser checks at mobile, tablet, and desktop widths; CI currently validates compilation and generated route files, not visual appearance.
