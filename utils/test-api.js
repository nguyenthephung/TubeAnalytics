// Test file for YouTube API functionality
// You can copy-paste this into browser console to test the API

const testYouTubeAPI = async () => {
  const testUrl = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' // Rick Roll - should always work
  
  try {
    const response = await fetch('/api/youtube', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: testUrl })
    })
    
    const data = await response.json()
    
    if (response.ok) {
      console.log('✅ API Test successful!')
      console.log('Video Title:', data.video.title)
      console.log('Channel:', data.video.channelTitle)
      console.log('Views:', data.video.viewCount)
      console.log('Comments found:', data.comments.length)
      return data
    } else {
      console.error('❌ API Test failed:', data.error)
      return null
    }
  } catch (error) {
    console.error('❌ Network error:', error)
    return null
  }
}

// Usage: testYouTubeAPI()
export default testYouTubeAPI