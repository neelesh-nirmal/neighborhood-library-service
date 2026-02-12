"use client";

import { useState, useEffect } from "react";
import { booksApi, getErrorMessage, type Book, type BookCreate } from "@/lib/api";

export function BooksSection() {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState<BookCreate>({ title: "", author: "", description: null, isbn: null });
  const [message, setMessage] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await booksApi.list();
      setBooks(data);
    } catch (e) {
      setError(getErrorMessage(e, "Failed to load books. Please try again."));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    if (!form.title.trim() || !form.author.trim()) return;
    try {
      await booksApi.create({
        title: form.title.trim(),
        author: form.author.trim(),
        description: form.description?.trim() || null,
        isbn: form.isbn?.trim() || null,
      });
      setMessage("Book created.");
      setForm({ title: "", author: "", description: null, isbn: null });
      load();
    } catch (e) {
      setError(getErrorMessage(e, "Failed to create book. Please check the form and try again."));
    }
  };

  return (
    <div className="panel">
      <h2 style={{ marginTop: 0 }}>Books (catalog)</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <label>
            Title
            <input
              value={form.title}
              onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
              placeholder="Title"
              required
            />
          </label>
          <label>
            Author
            <input
              value={form.author}
              onChange={(e) => setForm((f) => ({ ...f, author: e.target.value }))}
              placeholder="Author"
              required
            />
          </label>
          <label>
            ISBN
            <input
              value={form.isbn ?? ""}
              onChange={(e) => setForm((f) => ({ ...f, isbn: e.target.value || null }))}
              placeholder="Optional"
            />
          </label>
          <button type="submit" className="btn btn-primary">
            Add book
          </button>
        </div>
        <div className="form-row">
          <label style={{ flex: "1 1 100%" }}>
            Description
            <input
              value={form.description ?? ""}
              onChange={(e) => setForm((f) => ({ ...f, description: e.target.value || null }))}
              placeholder="Optional"
            />
          </label>
        </div>
      </form>
      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}

      <h3 style={{ marginTop: "1.5rem" }}>All books</h3>
      {loading ? (
        <p className="muted">Loading…</p>
      ) : books.length === 0 ? (
        <p className="muted">No books yet. Add one above.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>ISBN</th>
            </tr>
          </thead>
          <tbody>
            {books.map((b) => (
              <tr key={b.id}>
                <td>{b.title}</td>
                <td>{b.author}</td>
                <td>{b.isbn ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
