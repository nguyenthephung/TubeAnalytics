import { NextResponse } from 'next/server'

// Server-side HTML cleaning function
function cleanHtmlText(text) {
  if (!text) return ''
  
  let cleanText = text
  
  // Decode HTML entities
  cleanText = cleanText
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&apos;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#x27;/g, "'")
    .replace(/&#x2F;/g, '/')
    .replace(/&#(\d+);/g, (match, dec) => String.fromCharCode(dec))
    .replace(/&#x([0-9a-fA-F]+);/g, (match, hex) => String.fromCharCode(parseInt(hex, 16)))
    
  // Remove HTML tags
  cleanText = cleanText.replace(/<[^>]*>/g, '')
  
  // Remove emojis and icons
  cleanText = cleanText
    // Remove emoji ranges
    .replace(/[\u{1F600}-\u{1F64F}]/gu, '') // Emoticons
    .replace(/[\u{1F300}-\u{1F5FF}]/gu, '') // Misc Symbols and Pictographs  
    .replace(/[\u{1F680}-\u{1F6FF}]/gu, '') // Transport and Map
    .replace(/[\u{1F1E0}-\u{1F1FF}]/gu, '') // Flags
    .replace(/[\u{2600}-\u{26FF}]/gu, '')   // Misc symbols
    .replace(/[\u{2700}-\u{27BF}]/gu, '')   // Dingbats
    .replace(/[\u{1F900}-\u{1F9FF}]/gu, '') // Supplemental Symbols and Pictographs
    .replace(/[\u{1F018}-\u{1F270}]/gu, '') // Various symbols
    // Remove specific common icons and symbols
    .replace(/[★☆♥♡💙💚💛💜🧡❤️💖💗💓💕💘💝💞💟❣️💔💋👍👎👌✌️🤞🤘🤟🤙👊✊🤜🤛👏🙌🤲🤝🤗🔥💯⚡🎉🎊]/gu, '')
    // Remove arrows and other symbols
    .replace(/[←↑→↓↔↕⬅⬆➡⬇⤴⤵]/gu, '')
    // Remove musical notes and other symbols
    .replace(/[♪♫♬♩🎵🎶]/gu, '')
  
  // Clean up whitespace
  cleanText = cleanText
    .replace(/\n\n+/g, '\n\n') // Multiple line breaks to double
    .replace(/^\s+|\s+$/g, '') // Trim whitespace
    
  // Remove zero-width characters
  cleanText = cleanText.replace(/[\u200B-\u200D\uFEFF]/g, '')
  
  // Final cleanup of extra spaces
  cleanText = cleanText.replace(/\s+/g, ' ').trim()
  
  return cleanText
}

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
        text: cleanHtmlText(item.snippet.topLevelComment.snippet.textDisplay),
        author: cleanHtmlText(item.snippet.topLevelComment.snippet.authorDisplayName),
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
      title: cleanHtmlText(video.snippet.title),
      description: cleanHtmlText(video.snippet.description),
      thumbnail: video.snippet.thumbnails.maxres?.url || video.snippet.thumbnails.high?.url || video.snippet.thumbnails.medium.url,
      channelTitle: cleanHtmlText(video.snippet.channelTitle),
      channelId: video.snippet.channelId,
      publishedAt: video.snippet.publishedAt,
      viewCount: parseInt(video.statistics.viewCount || 0),
      likeCount: parseInt(video.statistics.likeCount || 0),
      commentCount: parseInt(video.statistics.commentCount || 0),
      duration: video.contentDetails.duration,
      tags: video.snippet.tags?.map(tag => cleanHtmlText(tag)) || [],
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