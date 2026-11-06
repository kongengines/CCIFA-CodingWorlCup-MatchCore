import { useTranslation } from "@/i18n/useTranslation";
import type { MatchSeal as MatchSealType } from "@/types/match";
import { ShieldCheck, ShieldAlert } from "lucide-react";

interface Props {
  seal: MatchSealType | null;
}

export function MatchSeal({ seal }: Props) {
  const { t } = useTranslation();
  if (!seal) {
    return (
      <div className="flex items-center gap-2 rounded-md bg-amber-50 px-3 py-2 text-sm text-amber-700">
        <ShieldAlert className="h-4 w-4" />
        {t("seal.invalid")}
      </div>
    );
  }
  return (
    <div className="rounded-lg border border-sovereign-seal/10 bg-sovereign-seal p-4 text-sm text-slate-100">
      <div className="mb-2 flex items-center gap-2 font-semibold text-sovereign-gold">
        <ShieldCheck className="h-4 w-4" />
        {t("seal.title")}
      </div>
      <dl className="grid grid-cols-1 gap-1 font-mono text-xs">
        <div>
          <dt className="text-slate-400">{t("match.sealRoot")}</dt>
          <dd className="break-all">{seal.root_hash}</dd>
        </div>
        <div>
          <dt className="text-slate-400">{t("match.signature")}</dt>
          <dd className="break-all">{seal.signature}</dd>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <dt className="text-slate-400">{t("match.arbiter")}</dt>
            <dd>{seal.arbiter_id}</dd>
          </div>
          <div>
            <dt className="text-slate-400">#</dt>
            <dd>{seal.ledger_index}</dd>
          </div>
        </div>
      </dl>
      <p className="mt-2 text-xs text-emerald-400">{t("seal.valid")}</p>
    </div>
  );
}
