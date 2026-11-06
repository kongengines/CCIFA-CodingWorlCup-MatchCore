import { createBrowserRouter } from "react-router-dom";
import { HomePage } from "@/pages/HomePage";
import { MatchesPage } from "@/pages/MatchesPage";
import { WorldCupPage } from "@/pages/WorldCupPage";
import { FederationPage } from "@/pages/FederationPage";
import { LeaguesPage } from "@/pages/LeaguesPage";

export const router = createBrowserRouter([
  { path: "/", element: <HomePage /> },
  { path: "/federation", element: <FederationPage /> },
  { path: "/leagues", element: <LeaguesPage /> },
  { path: "/matches", element: <MatchesPage /> },
  { path: "/worldcup", element: <WorldCupPage /> },
]);
