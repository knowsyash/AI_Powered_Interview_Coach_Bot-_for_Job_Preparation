import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        
        const backendUrl = process.env.BACKEND_URL || 'http://localhost:5000';
        const response = await fetch(`${backendUrl}/get_hint`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();
        
        if (!response.ok) {
            return NextResponse.json(
                { error: data.error || 'Failed to get hint' },
                { status: response.status }
            );
        }

        return NextResponse.json(data);
    } catch (error) {
        console.error('Error getting hint:', error);
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        );
    }
}
