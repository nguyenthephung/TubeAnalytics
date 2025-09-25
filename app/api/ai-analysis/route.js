import { NextResponse } from 'next/server'

const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:8000'

export async function POST(request) {
  try {
    const { comments, videoTitle, analysisType = 'comprehensive' } = await request.json()
    
    if (!comments || !Array.isArray(comments) || comments.length === 0) {
      return NextResponse.json({ error: 'Comments are required' }, { status: 400 })
    }

    // Transform comments to match FastAPI format
    const transformedComments = comments.map(comment => ({
      id: comment.id || `comment_${Date.now()}_${Math.random()}`,
      text: comment.textOriginal || comment.text || '',
      author: comment.authorDisplayName || comment.author || 'Unknown',
      likeCount: parseInt(comment.likeCount || 0),
      publishedAt: comment.publishedAt || new Date().toISOString()
    }))

    // Call FastAPI analysis endpoint
    const analysisResponse = await fetch(`${FASTAPI_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        comments: transformedComments,
        video_title: videoTitle || '',
        analysis_type: analysisType
      })
    })

    if (!analysisResponse.ok) {
      const errorData = await analysisResponse.json()
      console.error('FastAPI Error:', errorData)
      return NextResponse.json(
        { error: 'AI analysis service unavailable', details: errorData }, 
        { status: 503 }
      )
    }

    const analysisData = await analysisResponse.json()
    
    return NextResponse.json({
      success: true,
      analysis: analysisData,
      metadata: {
        processedComments: transformedComments.length,
        analysisType,
        timestamp: new Date().toISOString()
      }
    })

  } catch (error) {
    console.error('Analysis API Error:', error)
    
    // Check if FastAPI is running
    if (error.code === 'ECONNREFUSED' || error.message.includes('fetch failed')) {
      return NextResponse.json(
        { 
          error: 'AI analysis service is not running', 
          suggestion: 'Please start the FastAPI server using start_fastapi.bat'
        }, 
        { status: 503 }
      )
    }
    
    return NextResponse.json(
      { error: 'Internal server error', details: error.message }, 
      { status: 500 }
    )
  }
}

// Health check endpoint
export async function GET() {
  try {
    const healthResponse = await fetch(`${FASTAPI_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })

    if (!healthResponse.ok) {
      return NextResponse.json(
        { status: 'FastAPI service unavailable' }, 
        { status: 503 }
      )
    }

    const healthData = await healthResponse.json()
    
    return NextResponse.json({
      status: 'OK',
      fastapi: healthData,
      nextjs: {
        timestamp: new Date().toISOString(),
        version: '1.0.0'
      }
    })

  } catch (error) {
    return NextResponse.json(
      { 
        status: 'FastAPI service not reachable',
        error: error.message
      }, 
      { status: 503 }
    )
  }
}