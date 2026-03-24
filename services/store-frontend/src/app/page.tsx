// src/app/page.tsx
import { InventoryTable, type InventoryItem } from '@/components/ui/InventoryTable';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { logger } from '@/lib/logger';

export const dynamic = 'force-dynamic'; 

async function fetchInventory(): Promise<InventoryItem[]> {
  // Read from the environment, fallback to the K8s service name
  const baseUrl = process.env.INVENTORY_API_URL || 'http://inventory-api';
  const endpoint = `${baseUrl}/api/stock`;

  try {
    const response = await fetch(endpoint, { 
      cache: 'no-store' 
    });

    if (!response.ok) {
      throw new Error(`Inventory API returned ${response.status}`);
    }

    return response.json();
  } catch (error) {
    logger.error({ 
      error: error instanceof Error ? error.message : 'Unknown error', 
      dependency: 'inventory-api',
      url: baseUrl // Useful for debugging config issues without high-cardinality dynamic paths
    }, 'Backend dependency failure');
    
    throw error;
  }
}

export default async function Home() {
  logger.info({ route: '/' }, 'Rendering store dashboard');
  const items = await fetchInventory();

  return (
    <main className="min-h-screen bg-gray-50/30 dark:bg-black p-8 md:p-12">
      <div className="mx-auto max-w-5xl space-y-8">
        <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-gray-900 dark:text-white">Store Inventory</h1>
            <p className="text-gray-500 text-sm mt-1">Real-time stock monitoring</p>
          </div>
          <StatusBadge status="healthy" />
        </header>

        <InventoryTable items={items} />
      </div>
    </main>
  );
}