// src/components/ui/InventoryTable.tsx
export interface InventoryItem {
  id: string;
  name: string;
  stock: number;
  price: number;
}

export function InventoryTable({ items }: { items: InventoryItem[] }) {
  if (!items.length) {
    return (
      <div className="flex items-center justify-center p-12 border rounded-2xl border-dashed border-gray-300 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/20 text-gray-500">
        No inventory found.
      </div>
    );
  }

  return (
    <div className="overflow-hidden border rounded-2xl border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 shadow-sm">
      <table className="w-full text-left text-sm whitespace-nowrap">
        <thead className="bg-gray-50/50 dark:bg-gray-900/50 border-b border-gray-200 dark:border-gray-800">
          <tr>
            <th className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">Product Name</th>
            <th className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">Stock Level</th>
            <th className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100 text-right">Unit Price</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
          {items.map((item) => (
            <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-gray-900/20 transition-colors">
              <td className="px-6 py-4 text-gray-700 dark:text-gray-300">{item.name}</td>
              <td className="px-6 py-4">
                <span className={`inline-flex px-2.5 py-1 rounded-md text-xs font-medium ${item.stock > 10 ? 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300' : 'bg-orange-50 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'}`}>
                  {item.stock} in stock
                </span>
              </td>
              <td className="px-6 py-4 text-right font-medium text-gray-900 dark:text-gray-100">
                ${item.price.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}