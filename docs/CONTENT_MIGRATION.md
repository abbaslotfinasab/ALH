# ALH Content and URL Migration Register

**Status:** Preparation only — no Production export has been performed.  
**Source:** Existing Django application on the legacy site.  
**Target:** Astro static content collections and generated pages.

## 1. Content migration inventory

| Content type | Django source | Fields/data to preserve | Static target | Status |
|---|---|---|---|---|
| Profile/site identity | Templates, settings, SEO records | Name, title, bio, portrait/logo, social links, contact links, SEO metadata | `src/data/profile.ts` | Awaiting owner-approved content review |
| Companies | `experience.Company` | Name, slug, logo, website, active state | `src/data/experience.ts` or content collection | Schema inspected; records not exported |
| Work experiences | `experience.Experience` | Company relation, title, employment type, dates, description | Experience collection | Schema inspected; records not exported |
| Projects | `experience.Project` | Experience relation, name, role, description, technologies, demo URL, screenshot | Projects collection | Schema inspected; records not exported |
| Blog articles | `blog.Blog` | Title, slug, body, publication date, image, SEO fields, keywords | Insights collection | Schema inspected; records not exported |
| Short posts | `post.Post` | Title, content, media, publish state, timestamps, slug, SEO, canonical, keywords | Insights collection or separate post collection | Schema inspected; records not exported |
| Comments | `post.Comment` | Post relation, display name, text, timestamp | Usually omit from static v1 unless explicitly required | Schema inspected; decision pending |
| Snippets | `handwrite.Snippet` | Title, slug, description, code, language, project, lesson, order, timestamps | Technical notes collection or Insights | Schema inspected; records not exported |
| Services | `service.Service` | Title, slug, descriptions, content, image, technologies, active state | Selected service/approach pages | Schema inspected; records not exported |
| Technologies | `service.Technology` | Name, slug, icon, description, official website | Project/experience metadata | Schema inspected; records not exported |
| SEO pages/keywords | `seo.SEOPage`, `seo.Keyword` | Titles, descriptions, canonical intent, keyword associations | Per-page frontmatter and generated metadata | Schema inspected; records not exported |
| Availability | `home.Availability` | Status, message, updated timestamp | Optional manually maintained profile data | Schema inspected; owner decision pending |
| Collaboration requests | `collab.ProjectRequest`, `collab.HireRequest` | Submitted requests and personal information | Not migrated to public static site | Private data; do not export into public repository |

## 2. Media migration inventory

The repository's `.gitignore` excludes `media/`, so uploaded images/files are not included in the audited Git tree.

Known upload paths from model definitions:

- `company_logos/`
- `project_shots/`
- `blog_images/`
- `posts/images/`
- `posts/videos/`
- `posts/og/`
- `services/images/`

Required procedure:
1. Obtain authorized read-only access to the existing media storage.
2. Produce a filename/path inventory and file checksums.
3. Match media paths to exported records.
4. Copy only approved public assets into the new static site's `public/media/` (or optimized derivatives).
5. Preserve source filenames or maintain a deterministic old-path → new-path manifest.
6. Do not commit private uploads, request attachments, secrets, or unreferenced personal data.

## 3. URL preservation and redirect register

The route table in [REDESIGN_AUDIT.md](./REDESIGN_AUDIT.md) is a route-family inventory only. A record-level redirect manifest is still required.

Suggested manifest columns:

```csv
old_path,new_path,http_status,content_type,source_slug,verified,notes
```

Rules:
- Preserve existing published blog and post slugs whenever possible.
- Do not redirect every legacy URL to the homepage.
- Use a direct 301 redirect for each retired URL with a clear equivalent.
- Keep canonical URLs self-referencing on the new destination.
- Check query-string behavior for old tag/filter URLs.
- Verify old URLs from Search Console/backlinks before launch.
- Keep `/robots.txt` and `/sitemap.xml` valid on the static host.

## 4. SEO metadata mapping

For every published page/article, preserve or deliberately improve:

- `title` / `meta_title`
- `meta_description`
- canonical URL
- Open Graph title, description, and image
- Twitter card metadata
- publication and modification dates where available
- structured data type and required properties
- indexability and robots directives

Do not generate duplicate pages from both the old and new content systems after cutover.

## 5. Static content format

Preferred formats:

- Stable profile and navigation data: TypeScript/JSON under `src/data/`.
- Long-form articles and case studies: Markdown/MDX content collections.
- Images and downloadable public assets: `public/media/`.
- Redirects: host-specific redirect file generated from the approved manifest.

The exact schema will be finalized after inspecting representative exported records. Do not invent missing dates, roles, metrics, project outcomes, or article content.

## 6. Export acceptance checklist

- [ ] A read-only database export is available.
- [ ] Export counts are recorded per content type.
- [ ] Published/unpublished records are distinguished.
- [ ] Persian and English text round-trips correctly (UTF-8).
- [ ] Relationships (company → experience → project, post → keywords) are preserved.
- [ ] Media references resolve to actual files.
- [ ] SEO fields and canonical URLs are captured.
- [ ] Redirect manifest covers every indexed/published legacy URL.
- [ ] Private collaboration submissions are excluded from public content.
- [ ] Owner reviews and approves the content before public launch.

## 7. Production safety

This register does not authorize or perform database reads, database writes, media transfers, deployments, DNS changes, or Production service changes. Those steps require separate access and explicit approval.
