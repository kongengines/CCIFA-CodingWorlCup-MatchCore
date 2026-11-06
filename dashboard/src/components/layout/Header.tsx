import { useTranslation } from "@/i18n/useTranslation";
import { LanguageSwitcher } from "./LanguageSwitcher";
import { Trophy } from "lucide-react";

export function Header() {
  const { t } = useTranslation();
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="flex items-center justify-between px-6 py-3">
        <div className="flex items-center gap-3">
          <Trophy className="h-6 w-6 text-ccifa-600" />
          <div>
            <h1 className="text-lg font-bold text-slate-900">{t("app.title")}</h1>
            <p className="text-xs text-slate-500">{t("app.subtitle")}</p>
          </div>
        </div>
        <LanguageSwitcher />
      </div>
    </header>
  );
}
