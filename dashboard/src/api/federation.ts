import { apiGet } from "./client";
import type { Federation, Confederation } from "@/types/federation";

export const federationApi = {
  get: () => apiGet<Federation>("/federation"),
  confederations: () => apiGet<{ confederations: Confederation[] }>("/confederations"),
  worldcup: () =>
    apiGet<{
      name: string;
      cycle: string;
      next_edition: number;
      confederations: Confederation[];
      rankings: unknown[];
    }>("/worldcup"),
};
