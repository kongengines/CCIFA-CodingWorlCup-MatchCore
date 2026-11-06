import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// CCIFA Coding World Cup showcase — 11 certified locales.
export default defineConfig({
  site: "https://worldcup.ccifa.org",
  integrations: [
    starlight({
      title: "Coding World Cup",
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
      sidebar: [
        { label: "Home", slug: "index" },
        { label: "About", slug: "about" },
        { label: "Hosts", slug: "hosts" },
        { label: "Honours", slug: "honours" },
      ],
    }),
  ],
});
