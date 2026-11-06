import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// CCIFA documentation site — 11 certified locales.
export default defineConfig({
  site: "https://docs.ccifa.org",
  integrations: [
    starlight({
      title: "CCIFA MatchCore",
      defaultLocale: "en",
      locales: {
    'en': { label: 'English', lang: 'en' },
    'fr': { label: 'Français', lang: 'fr' },
    'es': { label: 'Español', lang: 'es' },
    'it': { label: 'Italiano', lang: 'it' },
    'de': { label: 'Deutsch', lang: 'de' },
    'hi': { label: 'हिन्दी', lang: 'hi' },
    'pt': { label: 'Português', lang: 'pt' },
    'ja': { label: '日本語', lang: 'ja' },
    'zh': { label: '中文', lang: 'zh' },
    'ko': { label: '한국어', lang: 'ko' },
    'ar': { label: 'العربية', lang: 'ar' },
      },
      social: [
        { icon: "github", href: "https://github.com/ccifa/coding-world-cup" },
      ],
      sidebar: [
        { label: "Introduction", slug: "intro" },
        { label: "Architecture", slug: "architecture" },
        { label: "Sovereign Seal", slug: "seal" },
        { label: "Rule Pack v1.0", slug: "rules" },
      ],
    }),
  ],
});
