/**
 * @jest-environment node
 */
import { GET } from '@/app/api/health/route';

describe('/api/health Route Handler', () => {
  it('returns a 200 OK status with up indicator', async () => {
    const response = await GET();
    const data = await response.json();
    
    expect(response.status).toBe(200);
    expect(data).toEqual({ status: 'up' });
  });
});