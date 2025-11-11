import { AppProps } from 'next/app';
import { SessionProvider } from 'next-auth/react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import '../styles/globals.css';

// Main App Component
export default function App({ Component, pageProps: { session, ...pageProps } }: AppProps) {
  return (
    <SessionProvider session={session}>
      <Head>
        <title>Next.js Application</title>
        <meta name="description" content="Modern Next.js Application" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </SessionProvider>
  );
}

// Layout Component
function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      <Navigation />
      <main className="flex-1 container mx-auto px-4 py-8">
        {children}
      </main>
      <Footer />
    </div>
  );
}

// Navigation Component
function Navigation() {
  const router = useRouter();

  return (
    <nav className="bg-gray-800 text-white">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex space-x-4">
            <Link href="/" className={router.pathname === '/' ? 'active' : ''}>
              Home
            </Link>
            <Link href="/about" className={router.pathname === '/about' ? 'active' : ''}>
              About
            </Link>
            <Link href="/dashboard" className={router.pathname === '/dashboard' ? 'active' : ''}>
              Dashboard
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

// Footer Component
function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-4">
      <div className="container mx-auto px-4 text-center">
        <p>&copy; 2024 Next.js Application. All rights reserved.</p>
      </div>
    </footer>
  );
}

// pages/index.tsx
export function HomePage() {
  return (
    <div>
      <h1 className="text-4xl font-bold mb-4">Welcome to Next.js</h1>
      <p className="text-lg">Modern React Framework</p>
    </div>
  );
}

// pages/about.tsx
export function AboutPage() {
  return (
    <div>
      <h1 className="text-4xl font-bold mb-4">About</h1>
      <p className="text-lg">This is a Next.js application</p>
    </div>
  );
}

// pages/dashboard.tsx
import { useState } from 'react';

export function DashboardPage() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <h1 className="text-4xl font-bold mb-4">Dashboard</h1>
      <p className="text-lg mb-4">Count: {count}</p>
      <button
        onClick={() => setCount(count + 1)}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Increment
      </button>
    </div>
  );
}

// pages/api/hello.ts
import type { NextApiRequest, NextApiResponse } from 'next';

type Data = {
  message: string;
};

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  res.status(200).json({ message: 'Hello from Next.js API' });
}
