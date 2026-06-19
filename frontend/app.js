const API = "http://127.0.0.1:8000";

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

const api = {
  getTrending:          ()          => apiFetch("/movies/trending"),
  searchMovies:         (q, page=1) => apiFetch(`/movies/search?q=${encodeURIComponent(q)}&page=${page}`),
  getMovie:             (id)        => apiFetch(`/movies/${id}`),
  getWatchlist:         (watched)   => { const q = watched !== undefined ? `?watched=${watched}` : ""; return apiFetch(`/watchlist/${q}`); },
  addToWatchlist:       (movie)     => apiFetch("/watchlist/", { method: "POST", body: JSON.stringify(movie) }),
  updateItem:           (id, data)  => apiFetch(`/watchlist/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  removeFromWatchlist:  (id)        => apiFetch(`/watchlist/${id}`, { method: "DELETE" }),
  getRecommendations:   ()          => apiFetch("/ai/recommendations"),
};

// ── Toast ──────────────────────────────────────────────────
let toastTimer;
function showToast(msg, type = "") {
  const el = document.getElementById("toast");
  if (!el) return;
  el.textContent = msg;
  el.className = `show ${type}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.className = ""; }, 2600);
}

// ── Movie card ─────────────────────────────────────────────
function movieCard(m, { badge } = {}) {
  const poster = m.poster_path
    ? `<img src="${m.poster_path}" alt="${m.title}" loading="lazy">`
    : `<div class="poster-placeholder">🎬</div>`;

  const score = m.vote_average
    ? `<span class="score-pill">★ ${m.vote_average.toFixed(1)}</span>`
    : "";

  const badgeHtml = badge
    ? `<span class="badge ${badge === "Watched" ? "badge-watched" : "badge-list"}">${badge}</span>`
    : "";

  return `
    <div class="movie-card" onclick="location.href='movie.html?id=${m.tmdb_id}'">
      <div class="movie-card-poster">
        ${poster}
        ${score}
        ${badgeHtml}
      </div>
      <div class="movie-card-body">
        <div class="movie-card-title">${m.title}</div>
        <div class="movie-card-year">${m.release_year || "—"}</div>
      </div>
    </div>`;
}

// ── Active nav link ────────────────────────────────────────
document.querySelectorAll(".nav-links a").forEach(a => {
  if (a.href === location.href) a.classList.add("active");
});