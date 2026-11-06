import { useTranslation } from "@/i18n/useTranslation";
import { LANGUAGE_LABELS } from "@/i18n";
import { Globe } from "lucide-react";

export function LanguageSwitcher() {
  const { current, changeLanguage, supported, t } = useTranslation();
  return (
    <label className="flex items-center gap-2 text-sm">
      <Globe className="h-4 w-4 text-slate-500" aria-hidden />
      <span className="sr-only">{t("language.label")}</span>
      <select
        value={current}
        onChange={(e) => changeLanguage(e.target.value as never)}
        className="rounded-md border border-slate-300 bg-white px-2 py-1 text-sm"
        aria-label={t("language.label")}
      >
        {supported.map((lng) => (
          <option key={lng} value={lng}>
            {LANGUAGE_LABELS[lng]}
          </option>
        ))}
      </select>
    </label>
  );
}
