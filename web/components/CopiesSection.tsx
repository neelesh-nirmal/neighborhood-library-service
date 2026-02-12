"use client";

import { useState, useEffect } from "react";
import { booksApi, copiesApi, type Book, type BookCopy } from "@/lib/api";

export function CopiesSection() {
  const [books, setBooks] = useState<Book[]>([]);
  const [selectedBookId, setSelectedBookId] = useState<string>("");
  const [copies, setCopies] = useState<BookCopy[]>([]);
  const [copyCode, setCopyCode] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const loadBooks = async () => {
    try {
      const data = await booksApi.list();
      setBooks(data);
      if (data.length && !selectedBookId) setSelectedBookId(data[0].id);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load books");
    }
  };

  const loadCopies = async () => {
    if (!selectedBookId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await copiesApi.listByBook(selectedBookId);
      setCopies(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load copies");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBooks();
  }, []);

  useEffect(() => {
    if (selectedBookId) loadCopies();
    else setCopies([]);
  }, [selectedBookId]);

  const handleAddCopy = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedBookId || !copyCode.trim()) return;
    setError(null);
    setMessage(null);
    try {
      await copiesApi.create(selectedBookId, copyCode.trim());
      setMessage("Copy added.");
      setCopyCode("");
      loadCopies();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to add copy");
    }
  };

  return (
    <div className="panel">
      <h2 style={{ marginTop: 0 }}>Book copies</h2>
      <p className="muted">Add physical copies of a book so members can borrow them.</p>
      <form onSubmit={handleAddCopy}>
        <div className="form-row">
          <label>
            Book
            <select
              value={selectedBookId}
              onChange={(e) => setSelectedBookId(e.target.value)}
            >
              <option value="">Select a book</option>
              {books.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.title} — {b.author}
                </option>
              ))}
            </select>
          </label>
          <label>
            Copy code (barcode/shelf)
            <input
              value={copyCode}
              onChange={(e) => setCopyCode(e.target.value)}
              placeholder="e.g. A-001"
            />
          </label>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={!selectedBookId || !copyCode.trim()}
          >
            Add copy
          </button>
        </div>
      </form>
      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}

      <h3 style={{ marginTop: "1.5rem" }}>Copies for selected book</h3>
      {!selectedBookId ? (
        <p className="muted">Select a book above.</p>
      ) : loading ? (
        <p className="muted">Loading…</p>
      ) : copies.length === 0 ? (
        <p className="muted">No copies for this book yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Copy code</th>
              <th>Copy ID</th>
            </tr>
          </thead>
          <tbody>
            {copies.map((c) => (
              <tr key={c.id}>
                <td>{c.copy_code}</td>
                <td className="muted" style={{ fontFamily: "monospace", fontSize: "0.8rem" }}>{c.id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
