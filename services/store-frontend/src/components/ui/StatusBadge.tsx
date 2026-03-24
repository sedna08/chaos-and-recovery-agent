// src/components/ui/StatusBadge.tsx
import { CheckCircle2, XCircle } from 'lucide-react';

interface StatusBadgeProps {
  status: 'healthy' | 'degraded';
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const isHealthy = status === 'healthy';
  
  return (
    <div 
      className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium transition-colors
        ${isHealthy 
          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/30 dark:text-emerald-400 dark:border-emerald-800' 
          : 'bg-red-50 text-red-700 border border-red-200 dark:bg-red-950/30 dark:text-red-400 dark:border-red-800'
        }`}
    >
      {isHealthy ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
      {isHealthy ? 'System Operational' : 'System Degraded'}
    </div>
  );
}