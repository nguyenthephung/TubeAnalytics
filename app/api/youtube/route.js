import { NextResponse } from 'next/server'

export async function POST(request) {
  try {
    const { url } = await request.json()
    
    // Extract video ID from YouTube URL
    const videoId = extractVideoId(url)
    if (!videoId) {
      return NextResponse.json({ error: 'URL YouTube không hợp lệ' }, { status: 400 })
    }

    const apiKey = process.env.YOUTUBE_API_KEY
    
    // Get video details
    const videoResponse = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&part=snippet,statistics,contentDetails&key=${apiKey}`
    )
    
    if (!videoResponse.ok) {
      throw new Error('Failed to fetch video data')
    }
    
    const videoData = await videoResponse.json()
    
    if (!videoData.items || videoData.items.length === 0) {
      return NextResponse.json({ error: 'Video không tồn tại hoặc đã bị xóa' }, { status: 404 })
    }

    const video = videoData.items[0]
    
    // Get comments
    const commentsResponse = await fetch(
      `https://www.googleapis.com/youtube/v3/commentThreads?videoId=${videoId}&part=snippet&order=relevance&maxResults=50&key=${apiKey}`
    )
    
    let comments = []
    if (commentsResponse.ok) {
      const commentsData = await commentsResponse.json()
      console.log('Comments API response status:', commentsResponse.status)
      comments = commentsData.items?.map(item => ({
        id: item.id,
        text: item.snippet.topLevelComment.snippet.textDisplay,
        author: item.snippet.topLevelComment.snippet.authorDisplayName,
        authorImage: item.snippet.topLevelComment.snippet.authorProfileImageUrl,
        likeCount: item.snippet.topLevelComment.snippet.likeCount,
        publishedAt: item.snippet.topLevelComment.snippet.publishedAt,
        replyCount: item.snippet.totalReplyCount || 0
      })) || []
      console.log('Total comments fetched:', comments.length)
    } else {
      console.log('Comments API failed with status:', commentsResponse.status)
      const errorText = await commentsResponse.text()
      console.log('Comments API error:', errorText)
    }

    // Process video data
    const videoInfo = {
      id: video.id,
      title: video.snippet.title,
      description: video.snippet.description,
      thumbnail: video.snippet.thumbnails.maxres?.url || video.snippet.thumbnails.high?.url || video.snippet.thumbnails.medium.url,
      channelTitle: video.snippet.channelTitle,
      channelId: video.snippet.channelId,
      publishedAt: video.snippet.publishedAt,
      viewCount: parseInt(video.statistics.viewCount || 0),
      likeCount: parseInt(video.statistics.likeCount || 0),
      commentCount: parseInt(video.statistics.commentCount || 0),
      duration: video.contentDetails.duration,
      tags: video.snippet.tags || [],
      categoryId: video.snippet.categoryId
    }

    return NextResponse.json({ video: videoInfo, comments })
    
  } catch (error) {
    console.error('YouTube API Error:', error)
    return NextResponse.json({ error: 'Có lỗi xảy ra khi lấy dữ liệu từ YouTube' }, { status: 500 })
  }
}

function extractVideoId(url) {
  const regex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/
  const match = url.match(regex)
  return match ? match[1] : null
}