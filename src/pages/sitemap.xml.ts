import type { APIRoute } from "astro";
import { getCollection } from "astro:content";

export const prerender = true;

const staticPaths = [
  "/",
  "/about/",
  "/ventures/",
  "/projects/",
  "/experience/",
  "/insights/",
  "/contact/",
];

function escapeXml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

export const GET: APIRoute = async ({ site }) => {
  if (!site) {
    throw new Error("Astro site URL must be configured to generate sitemap.xml");
  }

  const [projects, insights] = await Promise.all([
    getCollection("projects", ({ data }) => data.status === "published"),
    getCollection("insights", ({ data }) => data.status === "published"),
  ]);

  type SitemapEntry = { path: string; lastmod?: Date };
  const entries: SitemapEntry[] = [
    ...staticPaths.map((path) => ({ path })),
    ...projects.map((project) => ({
      path: `/projects/${encodeURIComponent(project.id)}/`,
      lastmod: project.data.updatedAt ?? project.data.publishedAt,
    })),
    ...insights.map((entry) => ({
      path: `/insights/${encodeURIComponent(entry.id)}/`,
      lastmod: entry.data.updatedAt ?? entry.data.publishedAt,
    })),
  ];

  const uniqueEntries = [...new Map(entries.map((entry) => [entry.path, entry])).values()];
  const urls = uniqueEntries
    .map(({ path, lastmod }) => {
      const lastmodTag = lastmod
        ? `\n    <lastmod>${lastmod.toISOString()}</lastmod>`
        : "";
      return `  <url>\n    <loc>${escapeXml(new URL(path, site).toString())}</loc>${lastmodTag}\n  </url>`;
    })
    .join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=0, s-maxage=3600",
    },
  });
};
