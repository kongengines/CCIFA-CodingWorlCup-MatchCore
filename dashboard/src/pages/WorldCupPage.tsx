import { useQuery } from "@tanstack/react-query";
import { federationApi } from "@/api/federation";
import { useTranslation } from "@/i18n/useTranslation";
import { Crown } from "lucide-react";

export function WorldCupPage() {
  const { t } = useTranslation();
  const { data, isLoading } = useQuery({
    queryKey: ["worldcup"],
    queryFn: federationApi.worldcup,
  });
  return (
    <section className="space-y-4">
      <div className="flex items-center gap-3">
        <Crown className="h-6 w-6 text-sovereign-gold" />
        <h2 className="text-xl font-bold">{t("nav.worldcup")}</h2>
      </div>
      {isLoading && <p>{t("common.loading")}</p>}
      {data && (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <div className="rounded-lg border border-slate-200 bg-white p-4">
            <p className="text-sm text-slate-500">{t("nav.worldcup")}</p>
            <p className="text-2xl font-bold">{data.name}</p>
            <p className="text-sm text-slate-600">{data.cycle} · {data.next_edition}</p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white p-4">
            <p className="text-sm text-slate-500">{t("federation.confederations")}</p>
            <ul className="mt-2 space-y-1">
              {data.confederations.map((c) => (
                <li key={c.code} className="font-mono text-sm">
                  <span className="text-ccifa-700">{c.code}</span> · {c.name}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </section>
  );
}
