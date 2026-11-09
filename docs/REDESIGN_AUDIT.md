# ALH Static Brand Redesign — Repository Audit

**Repository:** `abbaslotfinasab/ALH`  
**Baseline branch:** `main`  
**Baseline commit:** `f2f4251642f4e05170b3ab49c4882a73e875f6ae`  
**Working branch:** `redesign/static-brand`  
**Audit type:** Read-only source inspection; no production access or runtime changes.

## 1. Redesign decisions

- Framework: Astro + TypeScript.
- Rendering: Static Site Generation (prebuilt HTML/CSS/JS).
- Design direction: Evolve the existing visual identity rather than replace it wholesale.
- Git workflow: isolated feature branch; keep `main` untouched until review and approval.
- Runtime target: static hosting; no Django runtime, application database, or server-side template rendering for the redesigned public website.

## 2. Current repository snapshot

The inspected `main` tree contains 136 tracked files across 26 directories, including:

- 93 Python files.
- 12 Django HTML templates.
- One primary stylesheet: `static/css/style.css`.
- 9 image assets under `static/images/`.
- Django project configuration and apps for home, experience, posts, blog, services, collaboration, handwrite, and SEO.

The repository is currently a Django 4.2 application using Django REST Framework, PostgreSQL-oriented settings, Django templates, Bootstrap 5, and a database-backed content model.

This count describes the Git tree only. It does not include Production database records or ignored media files.

## 3. Existing design language to preserve and evolve

Observed in `templates/base.html` and `static/css/style.css`:

- Persian-first presentation with `lang="fa"` and RTL direction.
- Vazir typography.
- Navy `#003c70` and teal `#22c7b7` as recognizable brand colors.
- Light surfaces, generous whitespace, rounded components, subtle shadows.
- Responsive Bootstrap-based layout.
- Existing logo and image assets in `static/images/`.

Redesign direction: retain the recognizable palette, RTL support, typography character, and restrained visual tone. Improve layout hierarchy, spacing, responsive behavior, accessibility, and component consistency. Avoid copying the old page composition literally.

## 4. Current public routes discovered

Routes are registered in `ALH/urls.py` and app URL modules:

| Existing route | Current purpose | Proposed static destination |
|---|---|---|
| `/` | Home | `/` |
| `/about/` | About | `/about/` |
| `/experience/` | Experience and projects | `/experience/` |
| `/experience/<slug>/` | Company/experience detail | Preserve route where useful; otherwise redirect to a mapped detail page |
| `/post/` | Short-form feed | `/insights/` or a dedicated archive route after content review |
| `/post/<slug>/` | Post detail | Preserve or explicitly redirect each published slug |
| `/blogs/` | Long-form blog archive | `/insights/` |
| `/blogs/<slug>/` | Blog detail | Prefer preserving `/blogs/<slug>/` unless a complete redirect map is approved |
| `/collab/` | Collaboration forms | `/contact/` |
| `/service/` and `/service/<slug>/` | Service pages | Review content; map valuable pages individually |
| `/handwrite/` and `/handwrite/<slug>/` | Code snippets/notes | Review content; move useful material into Insights |
| `/sitemap.xml` | Dynamic sitemap | Generated static sitemap |
| `/robots.txt` | Robots policy | Static robots file |

The proposed destinations are planning decisions, not implemented redirects. Existing URLs must not be discarded before the content inventory and redirect map are complete.

## 5. Existing content sources

The source code confirms the following database-backed content entities:

- **Experience:** Company, Experience, Project. Includes company name/slug/logo/website, role, dates, descriptions, project descriptions, technology strings, demo links, and screenshots.
- **Blog:** title, slug, body content, publication date, image, meta title, meta description, and keyword relations.
- **Post/feed:** title, content, image, video, publication flag, timestamps, engagement counters, slug, SEO metadata, Open Graph image, canonical URL, and keyword relations.
- **Handwrite/snippets:** title, slug, short description, code body, language, project name, lesson, publication flag, order, and timestamps.
- **Services:** title, slug, short description, long content, image, icon, active flag, and technology relations.
- **SEO:** page-level title/description and keyword records.
- **Availability:** current status and message.
- **Collaboration requests:** project/hire forms and their submitted records.

The actual records and uploaded media are not present in this Git tree. They require a separate authorized export from the existing Production database and media storage. No records have been exported or changed in this phase.

## 6. External dependencies currently visible in the base template

The existing base template references external assets/scripts including:

- Bootstrap through Django Bootstrap integration.
- Vazir font stylesheet hosted on jsDelivr.
- Font Awesome kit.
- Jalali date picker from unpkg.
- Swiper from jsDelivr.
- Ahrefs Analytics.
- Google Analytics 4.
- Google Tag Manager.

The static redesign should self-host essential fonts and local assets where licensing permits. Analytics identifiers and consent/privacy behavior should be reviewed before migration; do not silently drop or blindly copy tracking scripts.

## 7. Repository hygiene observations

- `.gitignore` already excludes Python caches, virtual environments, local databases, and `media/`.
- The tracked tree nevertheless includes Python bytecode under `__pycache__` and IDE-specific `.idea/` files.
- `static/images/simple-logo.png` is approximately 999 KB and should be inspected/optimized before reuse.
- The repository has no root `README.md` or frontend package manifest at the audited baseline.
- `requirements.txt` pins Django and Python dependencies; it will become legacy-only once the static site fully replaces Django.

Do not delete tracked legacy files as part of initial preparation. Cleanup should happen only after the static replacement is complete and the migration/rollback plan is approved.

## 8. Safety and migration constraints

1. Do not deploy, change DNS, alter Production services, or modify the Production database in this phase.
2. Do not remove Django source, templates, migrations, or old static assets yet.
3. Export and verify database content and uploaded media before retiring Django.
4. Preserve published slugs, canonical URLs, metadata, and meaningful inbound links.
5. Generate an explicit old-URL → new-URL redirect map before launch.
6. Keep the redesign isolated on `redesign/static-brand`; do not merge into `main` without review.
7. Treat analytics IDs, contact details, and any private data as configuration/content requiring deliberate review.

## 9. Phase 1 outcome

Completed:
- Created the isolated redesign branch from the audited `main` commit.
- Recorded the repository structure, design language, routes, content entities, and migration risks.
- Preserved all existing application source and assets unchanged.

Not yet completed:
- Production database export.
- Uploaded media export.
- Per-record content inventory and URL redirect manifest.
- Astro scaffold and visual implementation.
- Build, accessibility, SEO, and responsive verification.

These remaining tasks are intentionally deferred; this audit did not access Production.
