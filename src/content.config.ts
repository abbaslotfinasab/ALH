import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";

const editorialFields = {
  title: z.string().min(1),
  summary: z.string().min(1).max(320),
  status: z.enum(["draft", "published"]).default("draft"),
  publishedAt: z.coerce.date().optional(),
  updatedAt: z.coerce.date().optional(),
  tags: z.array(z.string()).default([]),
  coverImage: z.string().optional(),
  coverAlt: z.string().optional(),
  seoTitle: z.string().optional(),
  seoDescription: z.string().max(320).optional(),
  canonicalPath: z.string().optional(),
};

const projects = defineCollection({
  loader: glob({ base: "./src/content/projects", pattern: "**/*.{md,mdx}" }),
  schema: z.object({
    ...editorialFields,
    category: z.string().optional(),
    role: z.string().optional(),
    technologies: z.array(z.string()).default([]),
    website: z.string().url().optional(),
  }),
});

const insights = defineCollection({
  loader: glob({ base: "./src/content/insights", pattern: "**/*.{md,mdx}" }),
  schema: z.object({
    ...editorialFields,
    category: z.string().optional(),
    readingMinutes: z.number().int().positive().optional(),
  }),
});

export const collections = { projects, insights };
