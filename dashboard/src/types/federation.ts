export interface Confederation {
  code: string;
  name: string;
  region: string;
  national_leagues: string[];
  continental_leagues: string[];
  national_teams: string[];
}

export interface Organigram {
  president: string;
  committees: Record<string, string[]>;
}

export interface Federation {
  name: string;
  short_name: string;
  organigram: Organigram;
  confederations: Record<string, Confederation>;
  licensed_coders: number;
  accredited_arbiters: string[];
  created_at: string;
}
