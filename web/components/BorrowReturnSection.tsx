"use client";

import { useState, useEffect } from "react";
import { booksApi, copiesApi, membersApi, loansApi, type BookCopy, type Member } from "@/lib/api";

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
  const [copies, setCopies] = useState<BookCopy[]>([]);
  const [memberId, setMemberId] = useState("");
  const [copyId, setCopyId] = useState("");
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

  const loadCopies = async () => {
    try {
      const books = await booksApi.list();
      const allCopies: BookCopy[] = [];
      for (const b of books) {
        const list = await copiesApi.listByBook(b.id);
        allCopies.push(...list);
      }
      setCopies(allCopies);
      if (allCopies.length && !copyId) setCopyId(allCopies[0].id);
    } catch {
      setCopies([]);
    }
  };

  useEffect(() => {
    loadMembers();
    loadCopies();
  }, []);

  const handleBorrow = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    if (!memberId || !copyId || !dueDate) {
      setError("Select member, copy, and due date.");
      return;
    }
    try {
      await loansApi.borrow({
        member_id: memberId,
        copy_id: copyId,
        due_at: new Date(dueDate).toISOString(),
      });
      setMessage("Book borrowed.");
      loadCopies();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to borrow");
    }
  };

  return (
    <div className="panel">
      <h2 style={{ marginTop: 0 }}>Borrow a book</h2>
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
            Copy
            <select
              value={copyId}
              onChange={(e) => setCopyId(e.target.value)}
              required
            >
              <option value="">Select copy</option>
              {copies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.copy_code} (book: {c.book_id.slice(0, 8)}…)
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
