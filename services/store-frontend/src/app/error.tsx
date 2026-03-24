// src/app/error.tsx
'use client';

import { useEffect } from 'react';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { AlertOctagon } from 'lucide-react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Client-side reporting could go here. Server logging was already handled in page.tsx.
    console.error('UI Boundary Caught:', error);
  }, [error]);

  return (
    <main className="min-h-screen bg-gray-50/30 dark:bg-black flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white dark:bg-gray-950 border border-gray-200 dark:border-gray-800 rounded-3xl p-8 shadow-sm text-center flex flex-col items-center">
        <div className="w-16 h-16 bg-red-50 dark:bg-red-900/20 rounded-2xl flex items-center justify-center mb-6">
          <AlertOctagon className="w-8 h-8 text-red-600 dark:text-red-500" />
        </div>
        
        <StatusBadge status="degraded" />
        
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mt-6 mb-2">
          System Degraded
        </h2>
        <p className="text-gray-500 dark:text-gray-400 mb-8 text-sm">
          The inventory backend is currently unresponsive. Our Healer Agents have been notified via logs and are taking action.
        </p>
        
        <button
          onClick={() => reset()}
          className="w-full py-2.5 px-4 bg-gray-900 hover:bg-gray-800 dark:bg-white dark:hover:bg-gray-200 text-white dark:text-gray-900 font-medium rounded-xl transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
        >
          Retry Connection
        </button>
      </div>
    </main>
  );
}