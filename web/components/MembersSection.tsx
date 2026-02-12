"use client";

import { useState, useEffect } from "react";
import { membersApi, type Member, type MemberCreate } from "@/lib/api";

export function MembersSection() {
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState<MemberCreate>({ name: "", email: null, phone: null });
  const [message, setMessage] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await membersApi.list();
      setMembers(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load members");
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
    if (!form.name.trim()) return;
    try {
      await membersApi.create({
        name: form.name.trim(),
        email: form.email?.trim() || null,
        phone: form.phone?.trim() || null,
      });
      setMessage("Member created.");
      setForm({ name: "", email: null, phone: null });
      load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create member");
    }
  };

  return (
    <div className="panel">
      <h2 style={{ marginTop: 0 }}>Members</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <label>
            Name
            <input
              value={form.name}
              onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
              placeholder="Full name"
              required
            />
          </label>
          <label>
            Email
            <input
              type="email"
              value={form.email ?? ""}
              onChange={(e) => setForm((f) => ({ ...f, email: e.target.value || null }))}
              placeholder="Optional"
            />
          </label>
          <label>
            Phone
            <input
              value={form.phone ?? ""}
              onChange={(e) => setForm((f) => ({ ...f, phone: e.target.value || null }))}
              placeholder="Optional"
            />
          </label>
          <button type="submit" className="btn btn-primary">
            Add member
          </button>
        </div>
      </form>
      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}

      <h3 style={{ marginTop: "1.5rem" }}>All members</h3>
      {loading ? (
        <p className="muted">Loading…</p>
      ) : members.length === 0 ? (
        <p className="muted">No members yet. Add one above.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
            </tr>
          </thead>
          <tbody>
            {members.map((m) => (
              <tr key={m.id}>
                <td>{m.name}</td>
                <td>{m.email ?? "—"}</td>
                <td>{m.phone ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
