# Writing project entries

Create one Markdown or MDX file per verified project in src/content/projects/.

```yaml
---
title: "Project title"
summary: "A concise, factual summary."
status: draft
category: "Product engineering"
role: "My verified role"
technologies:
  - "Technology"
website: https://example.com
tags: []
seoTitle: "Optional SEO title"
seoDescription: "Optional search description"
canonicalPath: "/projects/project-slug/"
---
```

- The filename becomes the content slug and public URL segment.
- Keep status as draft until the description and publication rights are reviewed.
- Do not add NDA-bound details, invented metrics, or unverified claims.
- Use a local asset path for coverImage when a licensed image is available.