import { NextResponse } from 'next/server'

const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:8000'

export async function POST(request) {
  try {
    const { comments, videoTitle } = await request.json()
    
    if (!comments || !Array.isArray(comments) || comments.length === 0) {
      return NextResponse.json({ error: 'Comments are required' }, { status: 400 })
    }

    console.log(`🔍 Testing RAW Hume AI with ${comments.length} comments`)

    // Transform comments to match FastAPI format
    const transformedComments = comments.map(comment => ({
      id: comment.id || `comment_${Date.now()}_${Math.random()}`,
      text: comment.textOriginal || comment.text || '',
      author: comment.authorDisplayName || comment.author || 'Unknown',
      likeCount: parseInt(comment.likeCount || 0),
      publishedAt: comment.publishedAt || new Date().toISOString()
    }))

    // Call RAW FastAPI analysis endpoint 
    console.log(`📤 Calling ${FASTAPI_URL}/analyze-raw`)
    
    const analysisResponse = await fetch(`${FASTAPI_URL}/analyze-raw`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        comments: transformedComments,
        video_title: videoTitle || '',
        analysis_type: 'raw'
      }),
    })

    const analysisData = await analysisResponse.json()

    if (!analysisResponse.ok) {
      console.error('❌ FastAPI error:', analysisData)
      return NextResponse.json({ 
        error: 'AI analysis service unavailable',
        details: analysisData 
      }, { status: 500 })
    }

    console.log(`✅ RAW Analysis successful: ${analysisData.successful_responses}/${analysisData.total_comments}`)

    return NextResponse.json({
      success: true,
      raw_analysis: analysisData,
      analysis_type: "Hume AI Raw Data Test",
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('❌ AI Raw Analysis Error:', error)
    return NextResponse.json({ 
      error: 'Failed to perform raw AI analysis',
      details: error.message 
    }, { status: 500 })
  }
}