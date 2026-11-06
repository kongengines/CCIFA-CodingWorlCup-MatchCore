import { apiGet, apiPost } from "./client";
import type { Match } from "@/types/match";

export const matchesApi = {
  list: () => apiGet<{ matches: Match[] }>("/matches"),
  get: (id: string) => apiGet<{ match: Match }>(`/matches/${id}`),
  play: (id: string, body: { home_score: number; away_score: number; arbiter_id?: string }) =>
    apiPost<{ match: Match }>(`/matches/${id}/play`, body),
};
