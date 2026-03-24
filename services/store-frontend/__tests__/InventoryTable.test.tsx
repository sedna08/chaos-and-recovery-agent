import { render, screen } from '@testing-library/react';
import { InventoryTable } from '@/components/ui/InventoryTable';

describe('InventoryTable Component', () => {
  const mockData = [
    { id: '1', name: 'Mechanical Keyboard', stock: 42, price: 150.00 }
  ];

  it('renders empty state when no items are provided', () => {
    render(<InventoryTable items={[]} />);
    expect(screen.getByText(/No inventory found/i)).toBeInTheDocument();
  });

  it('renders inventory data correctly', () => {
    render(<InventoryTable items={mockData} />);
    expect(screen.getByText('Mechanical Keyboard')).toBeInTheDocument();
    expect(screen.getByText('42 in stock')).toBeInTheDocument();
    expect(screen.getByText('$150.00')).toBeInTheDocument();
  });
});