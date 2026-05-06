import { NextResponse } from 'next/server';

export async function GET(request: Request) {
    const { searchParams } = new URL(request.url);
    const category = searchParams.get('category');

    if (!category) {
        return NextResponse.json({ error: 'Category is required' }, { status: 400 });
    }

    try {
        const backendUrl = process.env.BACKEND_URL || 'http://localhost:5000';
        const response = await fetch(`${backendUrl}/get_question?category=${category}`);
        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error('Error fetching question from Python backend:', error);
        return NextResponse.json({ error: 'Failed to fetch question' }, { status: 500 });
    }
}
