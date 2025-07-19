// app/layout.tsx
import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "Minimal Fashion Shop",
  description: "AI Fashion Recommender",
};

// export default function RootLayout({ children }) {
import { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {

  return (
    <html lang="th">
      <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;700&display=swap" />
      </head>
      <body>
        <header className="header">
          <div className="logo">Minimal<span className="accent">Fashion</span></div>
          <nav>
            <Link href="/" className="nav-link">Home</Link>
            <Link href="/shirt" className="nav-link">Shirts</Link>
            <Link href="/pants" className="nav-link">Pants</Link>
          </nav>
        </header>
        <div className="main-content">
          {children}
        </div>
        <footer className="footer">
          <p>&copy; 2025 Minimal Fashion Shop. All rights reserved.</p>
        </footer>
      </body>
    </html>
  );
}
