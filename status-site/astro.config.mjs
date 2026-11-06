import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// CCIFA status site — public incident communication.
export default defineConfig({
  site: "https://status.ccifa.org",
  integrations: [
    starlight({
      title: "CCIFA Status",
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
        { label: "Live status", slug: "index" },
        { label: "Incidents", slug: "incidents" },
        { label: "Sovereign Ledger health", slug: "ledger" },
      ],
    }),
  ],
});
