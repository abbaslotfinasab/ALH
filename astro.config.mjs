import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://abbaslotfinasab.ir",
  output: "static",
  publicDir: "./static",
  build: {
    format: "directory",
    assets: "_astro",
  },
  trailingSlash: "always",
});
