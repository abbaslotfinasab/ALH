# Legacy Django Cleanup

## Merge and cleanup sequence

1. The Astro redesign branch `redesign/static-brand` was merged into `main` via PR #1.
2. The cleanup was prepared separately on `cleanup/remove-legacy-django` so the deletion set can be reviewed before it reaches `main`.

## Removed

- Django project configuration and entry points: `ALH/`, `manage.py`, and `requirements.txt`.
- Retired Django apps: `blog/`, `collab/`, `experience/`, `handwrite/`, `home/`, `post/`, `seo/`, and `service/`.
- Django-rendered templates in `templates/`.
- Tracked Python bytecode/cache files.
- PyCharm project metadata in `.idea/`.
- Legacy stylesheet `static/css/style.css`, which is not imported by the Astro site.
- Legacy images not referenced by the current Astro source.

## Preserved

- `static/images/logo.png`, used by the Astro layout as the favicon and default Open Graph image.
- `static/robots.txt`, used by the static site.
- All Astro source, styles, content architecture, scripts, CI workflow, documentation, and verified migrated content.

## Safety notes

- No database existed to migrate, and no Production website was deployed.
- No hosting, DNS, deployment, or Production service was modified.
- No collaboration-request records or private data were migrated into public content.
- Git history retains the removed files in earlier commits; this cleanup removes them from the current working tree, not from history.

## Validation

The cleanup branch is intended to run the existing Astro CI workflow before merging. Browser/device QA, Lighthouse, font-license verification, and social-image review remain separate release gates.
