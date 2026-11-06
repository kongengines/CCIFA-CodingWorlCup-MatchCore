import { useQuery } from "@tanstack/react-query";
import { federationApi } from "@/api/federation";
import { useTranslation } from "@/i18n/useTranslation";

export function FederationPage() {
  const { t } = useTranslation();
  const { data, isLoading } = useQuery({
    queryKey: ["federation"],
    queryFn: federationApi.get,
  });
  if (isLoading) return <p>{t("common.loading")}</p>;
  if (!data) return null;
  return (
    <section className="space-y-6">
      <h2 className="text-xl font-bold">{data.name}</h2>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <h3 className="font-semibold">{t("federation.president")}</h3>
          <p className="mt-1 text-slate-700">{data.organigram.president}</p>
          <h3 className="mt-4 font-semibold">{t("federation.committees")}</h3>
          <ul className="mt-1 space-y-1 text-sm">
            {Object.entries(data.organigram.committees).map(([k, v]) => (
              <li key={k}>
                <span className="text-slate-500">{k}:</span>{" "}
                <span className="text-slate-700">{v.length} members</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <h3 className="font-semibold">{t("federation.confederations")}</h3>
          <ul className="mt-2 space-y-2">
            {Object.values(data.confederations).map((c) => (
              <li key={c.code} className="rounded-md bg-slate-50 px-3 py-2">
                <span className="font-mono text-ccifa-700">{c.code}</span> · {c.name}
                <span className="text-xs text-slate-500"> — {c.region}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
