import { useQuery } from "@tanstack/react-query";
import { matchesApi } from "@/api/matches";
import { MatchSeal } from "@/components/matches/MatchSeal";
import { useTranslation } from "@/i18n/useTranslation";
import { ShieldCheck } from "lucide-react";

export function MatchesPage() {
  const { t } = useTranslation();
  const { data, isLoading, error } = useQuery({
    queryKey: ["matches"],
    queryFn: matchesApi.list,
  });
  if (isLoading) return <p>{t("common.loading")}</p>;
  if (error) return <p className="text-red-600">{t("common.error")}</p>;
  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold">{t("nav.matches")}</h2>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {data?.matches.map((m) => (
          <article key={m.id} className="rounded-lg border border-slate-200 bg-white p-4">
            <header className="flex items-center justify-between">
              <span className="font-mono text-xs text-slate-500">{m.id}</span>
              <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                m.kind === "OFFICIAL" ? "bg-ccifa-100 text-ccifa-700" : "bg-slate-100 text-slate-600"
              }`}>
                {m.kind === "OFFICIAL" ? t("match.official") : t("match.friendly")}
              </span>
            </header>
            <p className="mt-2 font-semibold">
              {m.home_id} <span className="text-slate-400">vs</span> {m.away_id}
            </p>
            {m.result && (
              <p className="mt-1 text-2xl font-bold">
                {m.result.home_score} - {m.result.away_score}
              </p>
            )}
            {m.kind === "OFFICIAL" && m.seal && (
              <div className="mt-3">
                <MatchSeal seal={m.seal} />
              </div>
            )}
            {m.kind === "OFFICIAL" && !m.seal && (
              <p className="mt-3 flex items-center gap-2 text-xs text-amber-700">
                <ShieldCheck className="h-3 w-3" /> {t("match.sealed")}: pending
              </p>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
