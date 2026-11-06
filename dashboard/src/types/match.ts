export interface MatchResult {
  home_score: number;
  away_score: number;
  winner_id: string | null;
  finished_at: string;
}

export interface MatchSeal {
  root_hash: string;
  signature: string;
  arbiter_id: string;
  chain_hash: string;
  prev_chain_hash: string;
  ledger_index: number;
  sealed_at: string;
  payload_hash: string;
  seal_id: string;
}

export interface Match {
  id: string;
  home_id: string;
  away_id: string;
  kind: "OFFICIAL" | "FRIENDLY";
  status: "SCHEDULED" | "IN_PROGRESS" | "FINISHED" | "CANCELLED";
  scheduled_at: string;
  started_at: string | null;
  finished_at: string | null;
  arbiter_id: string | null;
  arena_node_id: string | null;
  result: MatchResult | null;
  seal: MatchSeal | null;
}
