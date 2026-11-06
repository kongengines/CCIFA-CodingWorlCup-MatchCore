import http from "k6/http";
import { check, sleep } from "k6";

const BASE = __ENV.BASE_URL || "http://localhost:8000";

export const options = {
  stages: [
    { duration: "1m", target: 100 },
    { duration: "5m", target: 500 },
    { duration: "3m", target: 1000 },
    { duration: "2m", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<1000"],
    http_req_failed: ["rate<0.01"],
  },
};

export default function () {
  // Simulate World Cup traffic: heavy reads on /worldcup and /rankings.
  const r1 = http.get(`${BASE}/worldcup`);
  check(r1, { "worldcup ok": (r) => r.status === 200 });
  const r2 = http.get(`${BASE}/rankings`);
  check(r2, { "rankings ok": (r) => r.status === 200 });
  const r3 = http.get(`${BASE}/matches`);
  check(r3, { "matches ok": (r) => r.status === 200 });
  sleep(0.05);
}
