import { NavLink } from "react-router-dom";
import { useTranslation } from "@/i18n/useTranslation";
import {
  Home, Trophy, Flag, Shield, Users, Code2,
  GitBranch, BarChart3, Crown,
} from "lucide-react";

const items = [
  { to: "/", key: "nav.home", icon: Home },
  { to: "/federation", key: "nav.federation", icon: Flag },
  { to: "/leagues", key: "nav.leagues", icon: Trophy },
  { to: "/matches", key: "nav.matches", icon: Shield },
  { to: "/worldcup", key: "nav.worldcup", icon: Crown },
];

export function Sidebar() {
  const { t } = useTranslation();
  return (
    <nav className="hidden md:flex w-56 shrink-0 flex-col gap-1 border-r border-slate-200 bg-white p-3">
      {items.map(({ to, key, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          end={to === "/"}
          className={({ isActive }) =>
            `flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
              isActive
                ? "bg-ccifa-50 text-ccifa-700"
                : "text-slate-600 hover:bg-slate-100"
            }`
          }
        >
          <Icon className="h-4 w-4" />
          {t(key)}
        </NavLink>
      ))}
    </nav>
  );
}
