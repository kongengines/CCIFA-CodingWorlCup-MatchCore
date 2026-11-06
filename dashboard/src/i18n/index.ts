import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

export const SUPPORTED_LANGUAGES = [
  "en", "fr", "es", "it", "de",
  "hi", "pt", "ja", "zh", "ko", "ar",
] as const;

export type SupportedLanguage = (typeof SUPPORTED_LANGUAGES)[number];

export const LANGUAGE_LABELS: Record<SupportedLanguage, string> = {
  en: "English",
  fr: "Français",
  es: "Español",
  it: "Italiano",
  de: "Deutsch",
  hi: "हिन्दी",
  pt: "Português",
  ja: "日本語",
  zh: "中文",
  ko: "한국어",
  ar: "العربية",
};

async function loadResources(lng: string) {
  try {
    const mod = await import(`../public/locales/${lng}/common.json`);
    return mod.default ?? mod;
  } catch {
    return {};
  }
}

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: "en",
    supportedLngs: SUPPORTED_LANGUAGES as unknown as string[],
    interpolation: { escapeValue: false },
    resources: {},
    detection: {
      order: ["localStorage", "navigator"],
      lookupLocalStorage: "ccifa.lang",
      caches: ["localStorage"],
    },
  });

// Lazy-load the active language pack.
i18n.on("languageChanged", async (lng) => {
  if (!i18n.getResourceBundle(lng, "translation")) {
    const pack = await loadResources(lng);
    i18n.addResourceBundle(lng, "translation", pack, true, true);
  }
});

void loadResources(i18n.language || "en").then((pack) => {
  i18n.addResourceBundle(i18n.language || "en", "translation", pack, true, true);
});

export default i18n;
