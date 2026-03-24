// src/app/api/health/route.ts
import { NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

export async function GET() {
  logger.debug({ route: '/api/health' }, 'Health check ping received');
  return NextResponse.json({ status: 'up' }, { status: 200 });
}