"use client";

import { useState, useEffect } from "react";
import { membersApi, loansApi, type LoanWithDetails, type Member } from "@/lib/api";

function formatDate(s: string) {
  try {
    return new Date(s).toLocaleString();
  } catch {
    return s;
  }
}

export function LoansSection() {
  const [loans, setLoans] = useState<LoanWithDetails[]>([]);
  const [members, setMembers] = useState<Member[]>([]);
  const [memberFilter, setMemberFilter] = useState<string>("");
  const [activeOnly, setActiveOnly] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const loadMembers = async () => {
    try {
      const data = await membersApi.list();
      setMembers(data);
    } catch {
      setMembers([]);
    }
  };

  const loadLoans = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await loansApi.list({
        member_id: memberFilter || undefined,
        active_only: activeOnly,
      });
      setLoans(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load loans");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMembers();
  }, []);

  useEffect(() => {
    loadLoans();
  }, [memberFilter, activeOnly]);

  const handleReturn = async (loanId: string) => {
    setError(null);
    setMessage(null);
    try {
      await loansApi.return(loanId);
      setMessage("Book returned.");
      loadLoans();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to return");
    }
  };

  return (
    <div className="panel">
      <h2 style={{ marginTop: 0 }}>Loans</h2>
      <p className="muted">List borrowed books. Filter by member or show only active (not yet returned).</p>
      <div className="form-row">
        <label>
          Member
          <select
            value={memberFilter}
            onChange={(e) => setMemberFilter(e.target.value)}
          >
            <option value="">All members</option>
            {members.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
        </label>
        <label style={{ flexDirection: "row", alignItems: "center", gap: "0.5rem" }}>
          <input
            type="checkbox"
            checked={activeOnly}
            onChange={(e) => setActiveOnly(e.target.checked)}
          />
          Active only
        </label>
        <button type="button" className="btn" onClick={() => loadLoans()}>
          Refresh
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}

      {loading ? (
        <p className="muted">Loading…</p>
      ) : loans.length === 0 ? (
        <p className="muted">No loans match the filter.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Member</th>
              <th>Book</th>
              <th>Copy</th>
              <th>Borrowed</th>
              <th>Due</th>
              <th>Returned</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {loans.map((loan) => (
              <tr key={loan.id}>
                <td>{loan.member_name}</td>
                <td>{loan.book_title} — {loan.book_author}</td>
                <td>{loan.copy_code}</td>
                <td>{formatDate(loan.borrowed_at)}</td>
                <td>{formatDate(loan.due_at)}</td>
                <td>{loan.returned_at ? formatDate(loan.returned_at) : "—"}</td>
                <td>
                  {!loan.returned_at && (
                    <button
                      type="button"
                      className="btn btn-primary btn-sm"
                      onClick={() => handleReturn(loan.id)}
                    >
                      Return
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
