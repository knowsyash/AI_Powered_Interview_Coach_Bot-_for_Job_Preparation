import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        
        const backendUrl = process.env.BACKEND_URL || 'http://localhost:5000';
        const response = await fetch(`${backendUrl}/skip`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();
        
        if (!response.ok) {
            return NextResponse.json(
                { error: data.error || 'Failed to skip question' },
                { status: response.status }
            );
        }

        return NextResponse.json(data);
    } catch (error) {
        console.error('Error skipping question:', error);
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        );
    }
}
