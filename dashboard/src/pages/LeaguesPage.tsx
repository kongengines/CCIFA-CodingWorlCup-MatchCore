import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/api/client";
import { useTranslation } from "@/i18n/useTranslation";

export function LeaguesPage() {
  const { t } = useTranslation();
  const { data, isLoading } = useQuery({
    queryKey: ["leagues"],
    queryFn: () => apiGet<{ leagues: unknown[] }>("/leagues"),
  });
  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold">{t("nav.leagues")}</h2>
      {isLoading && <p>{t("common.loading")}</p>}
      {data && (data.leagues.length === 0 ? (
        <p className="text-slate-500">No leagues registered yet.</p>
      ) : (
        <pre className="overflow-auto rounded-lg bg-slate-900 p-4 text-xs text-slate-100">
          {JSON.stringify(data.leagues, null, 2)}
        </pre>
      ))}
    </section>
  );
}
