# Phase 9 — Static Performance Guardrails

## Delivered

- Added `npm run validate:performance` to measure the generated `dist/` output.
- Added conservative size budgets for total output, HTML, CSS, JavaScript, fonts, and individual raster/vector image files.
- Large images above 350 KiB are reported as warnings; oversized images above the hard per-image limit fail validation.
- Added the performance budget check to the Astro GitHub Actions workflow after build and route validation.

## Current budget

| Output | Budget |
|---|---:|
| Total generated output | 8 MiB |
| HTML total | 250 KiB |
| CSS total | 200 KiB |
| JavaScript total | 300 KiB |
| Fonts total | 500 KiB |
| Individual image | 1.5 MiB |
| Large-image warning | 350 KiB |

These are guardrails, not claims about measured page speed or Core Web Vitals. The budgets are intentionally conservative and should be tightened after real content and optimized assets are in place.

## Deliberate limitations

- No font was added: the intended Persian font files and their redistribution license have not yet been verified.
- Existing legacy images remain preserved. In particular, the large legacy logo asset should only be removed or converted after confirming whether any migrated content still references it.
- No image conversion was attempted through GitHub's file editor.
- No Lighthouse, browser rendering, mobile-device, or network-throttling measurements were available in this phase. This phase does not claim LCP, INP, CLS, or PageSpeed improvements.
- No dependencies were added, no production configuration was changed, and no deployment was performed.

## Next release gates

1. Verify the exact image usage and rights, then convert only assets that are actually used.
2. Add the licensed local Persian font and tune font loading after confirming the chosen family and weights.
3. Run desktop/mobile browser QA and Lighthouse on a preview build.
4. Revisit budgets using the measured output and actual performance data.
