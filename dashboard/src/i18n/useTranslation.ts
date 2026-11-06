import { useTranslation as useT } from "react-i18next";
import { useCallback } from "react";
import { SUPPORTED_LANGUAGES, type SupportedLanguage } from "./index";

export function useTranslation() {
  const { t, i18n, ...rest } = useT();
  const changeLanguage = useCallback(
    (lng: SupportedLanguage) => {
      i18n.changeLanguage(lng);
      localStorage.setItem("ccifa.lang", lng);
    },
    [i18n],
  );
  return {
    t,
    i18n,
    changeLanguage,
    current: (i18n.language?.split("-")[0] ?? "en") as SupportedLanguage,
    supported: SUPPORTED_LANGUAGES,
    ...rest,
  };
}
