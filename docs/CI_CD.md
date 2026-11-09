# ALH CI/CD

## Architecture

ALH uses GitHub Actions for continuous integration and Cloudflare Worker Builds for continuous deployment.

```text
feature/fix/docs branch
        |
        v
   Pull Request
        |
        v
     develop
        |
        v
  PR: develop -> main
        |
        v
      main
        |
        v
 PR: main -> production
        |
        v
   production push
        |
        v
 Cloudflare Worker Build
        |
        +-- npm audit
        +-- npm run build
        +-- npm run validate:output
        +-- npm run validate:performance
        |
        v
  npx wrangler deploy
        |
        v
 https://abbaslotfinasab.ir
```

## Continuous integration (GitHub Actions)

Workflow: `.github/workflows/astro-static.yml`

Triggers:
- Push to `develop`, `main`, and `production`
- Pull requests targeting `develop`, `main`, and `production`

Checks:
- `npm audit`
- `npm run build`
- `npm run validate:output`
- `npm run validate:performance`

Pull requests targeting `main` must originate from `develop`; the `Require develop as PR source` job enforces this rule.

## Continuous deployment (Cloudflare)

Cloudflare Worker Builds configuration:

| Setting | Value |
| --- | --- |
| Repository | `abbaslotfinasab/ALH` |
| Watched branch | `production` |
| Worker | `alh` |
| Automatic builds | Enabled |
| Production build | `npm audit && npm run build && npm run validate:output && npm run validate:performance` |
| Production deploy | `npx wrangler deploy` |
| Preview build | Same validation command |
| Preview deploy | `npx wrangler preview` |

A push to `production` automatically starts the Cloudflare build. Wrangler deploy runs only after the build command succeeds. If any audit, build, output, or performance validation fails, the deploy step is not reached and the currently active Worker version remains in service.

## Release procedure

1. Create a short-lived branch from `develop`.
2. Open and merge a PR into `develop` after CI passes.
3. Open a PR from `develop` to `main`; merge after required checks pass.
4. Open a PR from `main` to `production`; merge after CI passes.
5. Monitor the Cloudflare Worker Build for the new `production` commit.
6. Verify the public site after the build outcome is successful.

Do not push directly to `main` or `production`. Do not use force pushes on long-lived branches.

## GitHub ruleset action still required

The current `production` ruleset already requires pull requests, but it does not yet require a GitHub Actions status check. Add the `Build and validate` check to the `production` ruleset:

GitHub → ALH → Settings → Rules → Rulesets → production → Edit → Require status checks to pass → Add `Build and validate` → Save.

This prevents merging a production PR while GitHub CI is failing. Cloudflare independently runs the same release-critical validations before deployment.
