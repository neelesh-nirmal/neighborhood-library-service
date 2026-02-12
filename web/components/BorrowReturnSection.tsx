"use client";

import { useState, useEffect } from "react";
import { booksApi, getErrorMessage, membersApi, loansApi, type Book, type Member } from "@/lib/api";

function formatDateTimeLocal(d: Date): string {
  const pad = (n: number) => n.toString().padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function dueInDays(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() + days);
  d.setHours(18, 0, 0, 0);
  return formatDateTimeLocal(d);
}

export function BorrowReturnSection() {
  const [members, setMembers] = useState<Member[]>([]);
  const [books, setBooks] = useState<Book[]>([]);
  const [memberId, setMemberId] = useState("");
  const [bookId, setBookId] = useState("");
  const [dueDate, setDueDate] = useState(() => dueInDays(14));
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const loadMembers = async () => {
    try {
      const data = await membersApi.list();
      setMembers(data);
      if (data.length && !memberId) setMemberId(data[0].id);
    } catch {
      setMembers([]);
    }
  };

  const loadBooks = async () => {
    try {
      const data = await booksApi.list();
      setBooks(data);
      if (data.length && !bookId) setBookId(data[0].id);
    } catch {
      setBooks([]);
    }
  };

  useEffect(() => {
    loadMembers();
    loadBooks();
  }, []);

  const handleBorrow = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    if (!memberId || !bookId || !dueDate) {
      setError("Select member, book, and due date.");
      return;
    }
    try {
      await loansApi.borrowByBook({
        member_id: memberId,
        book_id: bookId,
        due_at: new Date(dueDate).toISOString(),
      });
      setMessage("Book borrowed. A copy was assigned automatically.");
      loadBooks();
    } catch (e) {
      setError(getErrorMessage(e, "Failed to borrow. Please check your selection and try again."));
    }
  };

  return (
    <div className="panel">
      <h2 style={{ marginTop: 0 }}>Borrow a book</h2>
      <p className="muted">Choose a member and a book; an available copy is assigned automatically.</p>
      <form onSubmit={handleBorrow}>
        <div className="form-row">
          <label>
            Member
            <select
              value={memberId}
              onChange={(e) => setMemberId(e.target.value)}
              required
            >
              <option value="">Select member</option>
              {members.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            Book
            <select
              value={bookId}
              onChange={(e) => setBookId(e.target.value)}
              required
            >
              <option value="">Select book</option>
              {books.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.title} — {b.author}
                </option>
              ))}
            </select>
          </label>
          <label>
            Due date
            <input
              type="datetime-local"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              required
            />
          </label>
          <div style={{ display: "flex", alignItems: "flex-end", gap: "0.5rem", flexWrap: "wrap" }}>
            <span className="muted" style={{ fontSize: "0.85rem", marginRight: "0.25rem" }}>Quick:</span>
            <button type="button" className="btn btn-sm" onClick={() => setDueDate(dueInDays(7))}>
              1 week
            </button>
            <button type="button" className="btn btn-sm" onClick={() => setDueDate(dueInDays(14))}>
              2 weeks
            </button>
            <button type="button" className="btn btn-sm" onClick={() => setDueDate(dueInDays(30))}>
              1 month
            </button>
          </div>
          <button type="submit" className="btn btn-primary">
            Borrow
          </button>
        </div>
      </form>
      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}
      <p className="muted" style={{ marginTop: "1rem" }}>
        To return a book, use the Loans tab and click Return on an active loan.
      </p>
    </div>
  );
}
