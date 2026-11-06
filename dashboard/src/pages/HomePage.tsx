import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "@/i18n/useTranslation";
import { federationApi } from "@/api/federation";
import { Link } from "react-router-dom";
import { Trophy, ShieldCheck, Globe2 } from "lucide-react";

export function HomePage() {
  const { t } = useTranslation();
  const { data, isLoading } = useQuery({
    queryKey: ["federation"],
    queryFn: federationApi.get,
  });
  return (
    <section className="space-y-6">
      <div className="rounded-xl bg-gradient-to-br from-ccifa-600 to-ccifa-900 p-8 text-white">
        <h2 className="text-3xl font-bold">{t("app.title")}</h2>
        <p className="mt-2 text-ccifa-100">{t("app.subtitle")}</p>
        <div className="mt-6 flex gap-3">
          <Link to="/matches" className="rounded-md bg-white px-4 py-2 text-sm font-semibold text-ccifa-700">
            {t("nav.matches")}
          </Link>
          <Link to="/worldcup" className="rounded-md border border-white/30 px-4 py-2 text-sm font-semibold">
            {t("nav.worldcup")}
          </Link>
        </div>
      </div>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card icon={<Trophy className="h-5 w-5 text-ccifa-600" />} title={t("nav.worldcup")} value={data ? String(data.licensed_coders) : "—"} />
        <Card icon={<ShieldCheck className="h-5 w-5 text-emerald-600" />} title={t("seal.title")} value="Sovereign" />
        <Card icon={<Globe2 className="h-5 w-5 text-sky-600" />} title={t("federation.confederations")} value={data ? String(Object.keys(data.confederations).length) : "—"} />
      </div>
      {isLoading && <p className="text-sm text-slate-500">{t("common.loading")}</p>}
    </section>
  );
}

function Card({ icon, title, value }: { icon: React.ReactNode; title: string; value: string }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <div className="flex items-center gap-2 text-sm text-slate-500">{icon}{title}</div>
      <p className="mt-2 text-2xl font-bold">{value}</p>
    </div>
  );
}
