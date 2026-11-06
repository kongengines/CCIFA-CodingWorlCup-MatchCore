import http from "k6/http";
import { check, sleep } from "k6";

const BASE = __ENV.BASE_URL || "http://localhost:8000";

export const options = {
  stages: [
    { duration: "2m", target: 600 },
    { duration: "5m", target: 1200 },
    { duration: "2m", target: 0 },
  ],
  thresholds: { http_req_duration: ["p(99)<2500"] },
};

export default function () {
  const res = http.get(`${BASE}/health`);
  check(res, { "status 200": (r) => r.status === 200 });
  sleep(0.1);
}
