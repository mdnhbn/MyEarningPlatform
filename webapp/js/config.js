// নিজের backend URL আর API key বসাও
const BACKEND_BASE_URL = "https://your-backend-url.onrailway.app";
const API_KEY = "changeme"; // backend/core/utils.py -> API_SECRET এর সমান হবে

function apiGet(path, params = {}) {
  const url = new URL(BACKEND_BASE_URL + path);
  Object.keys(params).forEach(k => url.searchParams.append(k, params[k]));

  return fetch(url, {
    headers: {
      "X-API-Key": API_KEY
    }
  }).then(r => r.json());
}

function apiPost(path, body = {}) {
  return fetch(BACKEND_BASE_URL + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY
    },
    body: JSON.stringify(body)
  }).then(r => r.json());
}
