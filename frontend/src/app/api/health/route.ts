import { NextResponse } from 'next/server';

export async function GET() {
    try {
        // Fallback to localhost for local dev, otherwise use Render URL
        const backendUrl = process.env.BACKEND_URL || 'http://localhost:5000';
        
        const response = await fetch(`${backendUrl}/health`, {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache',
            },
            // Fast timeout so the UI knows if it's sleeping
            signal: AbortSignal.timeout(5000) 
        });

        if (response.ok) {
            return NextResponse.json({ status: 'ok', message: 'Backend is awake' });
        }
        
        return NextResponse.json({ status: 'error', message: 'Backend is sleeping' }, { status: 503 });
    } catch (error) {
        return NextResponse.json({ status: 'error', message: 'Backend unreachable' }, { status: 503 });
    }
}
