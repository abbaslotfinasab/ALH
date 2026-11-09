# Phase 8 — Metadata & Accessibility Quality Gates

## Delivered
- Extended the generated-output validator to require exactly one non-empty page title, meta description, and canonical URL for every generated HTML page.
- Canonical URLs must be absolute and remain on the configured canonical origin.
- Added a check that every rendered `img` element includes an `alt` attribute.
- Existing required-route, sitemap, robots.txt, and local `href`/`src` checks remain active.
- These checks run in GitHub Actions after the Astro build.

## Boundaries
- The image check verifies presence of `alt`; it cannot judge whether the alternative text is meaningful.
- The metadata check does not score title/description length, uniqueness of wording, or search intent. Those require editorial review.
- The local-link check is a static HTML scan, not a browser crawler; it does not validate external destinations, JavaScript navigation, or responsive rendering.
- No package lockfile was generated in this phase. CI still uses `npm install`; switching to `npm ci` remains blocked until a genuine lockfile generated from the project's dependency graph can be committed. Do not fabricate one.
- Browser/device QA, Lighthouse/Core Web Vitals, font licensing review, and social-image verification remain open release gates.

## Production safety
All work remains on `redesign/static-brand`. No merge, deployment, DNS, hosting, or Production changes were performed.
