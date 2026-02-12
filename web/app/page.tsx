"use client";

import { useState } from "react";
import { LibraryLogo } from "@/components/LibraryLogo";
import { BooksSection } from "@/components/BooksSection";
import { MembersSection } from "@/components/MembersSection";
import { CopiesSection } from "@/components/CopiesSection";
import { BorrowReturnSection } from "@/components/BorrowReturnSection";
import { LoansSection } from "@/components/LoansSection";

type Tab = "books" | "members" | "copies" | "borrow" | "loans";

export default function Home() {
  const [tab, setTab] = useState<Tab>("books");

  return (
    <div className="container">
      <header className="site-header">
        <div className="logo-wrap">
          <LibraryLogo />
        </div>
        <div className="brand">
          <h1 className="brand-title">Neighborhood Library</h1>
          <p className="brand-tagline">Books, members & lending</p>
        </div>
      </header>
      <nav className="tabs">
        <button
          className={tab === "books" ? "active" : ""}
          onClick={() => setTab("books")}
        >
          Books
        </button>
        <button
          className={tab === "members" ? "active" : ""}
          onClick={() => setTab("members")}
        >
          Members
        </button>
        <button
          className={tab === "copies" ? "active" : ""}
          onClick={() => setTab("copies")}
        >
          Copies
        </button>
        <button
          className={tab === "borrow" ? "active" : ""}
          onClick={() => setTab("borrow")}
        >
          Borrow / Return
        </button>
        <button
          className={tab === "loans" ? "active" : ""}
          onClick={() => setTab("loans")}
        >
          Loans
        </button>
      </nav>

      {tab === "books" && <BooksSection />}
      {tab === "members" && <MembersSection />}
      {tab === "copies" && <CopiesSection />}
      {tab === "borrow" && <BorrowReturnSection />}
      {tab === "loans" && <LoansSection />}
    </div>
  );
}
