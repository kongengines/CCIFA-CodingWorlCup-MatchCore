import http from "k6/http";
import { check, sleep } from "k6";

const BASE = __ENV.BASE_URL || "http://localhost:8000";

export const options = {
  vus: 5,
  duration: "30s",
};

export default function () {
  const res = http.get(`${BASE}/health`);
  check(res, { "status 200": (r) => r.status === 200 });
  sleep(0.1);
}
