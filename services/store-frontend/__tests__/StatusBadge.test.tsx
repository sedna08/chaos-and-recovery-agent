import { render, screen } from '@testing-library/react';
import { StatusBadge } from '@/components/ui/StatusBadge';

describe('StatusBadge Component', () => {
  it('renders a healthy status correctly', () => {
    render(<StatusBadge status="healthy" />);
    expect(screen.getByText('System Operational')).toBeInTheDocument();
  });

  it('renders a degraded status correctly', () => {
    render(<StatusBadge status="degraded" />);
    expect(screen.getByText('System Degraded')).toBeInTheDocument();
  });
});