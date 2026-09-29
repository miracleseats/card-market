"use client";

import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Result = { id: number; label: string };

export default function SearchBox() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);

  async function search() {
    if (!q.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/cards/search?q=${encodeURIComponent(q)}`);
      setResults(await res.json());
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="search">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && search()}
          placeholder="Try: Kobe Bryant Topps Chrome 138"
        />
        <button onClick={search}>{loading ? "Searching..." : "Search"}</button>
      </div>

      {results.length > 0 && (
        <div className="grid">
          {results.map((r) => (
            <a className="card" href={`/cards/${r.id}`} key={r.id}>
              <strong>{r.label}</strong>
              <p className="muted">Open card profile →</p>
            </a>
          ))}
        </div>
      )}
    </>
  );
}
