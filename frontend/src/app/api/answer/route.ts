import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { question, answer, category, session_id } = body;

        if (!question || !answer || !category || !session_id) {
            return NextResponse.json({ error: 'Question, answer, category, and session_id are required' }, { status: 400 });
        }

        // Use Render URL if provided, otherwise localhost
        const backendUrl = process.env.BACKEND_URL || 'http://localhost:5000';
        const response = await fetch(`${backendUrl}/evaluate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });
        const data = await response.json();

        if (!response.ok) {
            return NextResponse.json({ error: data?.error || 'Failed to submit answer' }, { status: response.status });
        }

        return NextResponse.json(data);
    } catch (error) {
        console.error('Error submitting answer to Python backend:', error);
        return NextResponse.json({ error: 'Failed to submit answer' }, { status: 500 });
    }
}
