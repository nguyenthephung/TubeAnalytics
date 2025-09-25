// Utility functions for cleaning and formatting text content

export const cleanHtmlText = (text) => {
  if (!text) return ''
  
  // Decode HTML entities
  const decodeHtml = (html) => {
    const txt = document.createElement('textarea')
    txt.innerHTML = html
    return txt.value
  }
  
  let cleanText = text
  
  try {
    // Decode HTML entities like &quot; &amp; &lt; &gt;
    cleanText = decodeHtml(cleanText)
    
    // Remove HTML tags
    cleanText = cleanText.replace(/<[^>]*>/g, '')
    
    // Replace common HTML entities manually as backup
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
      
    // Remove YouTube-specific formatting
    cleanText = cleanText
      .replace(/\n\n+/g, '\n\n') // Multiple line breaks to double
      .replace(/^\s+|\s+$/g, '') // Trim whitespace
      
    // Remove zero-width characters and other problematic Unicode
    cleanText = cleanText.replace(/[\u200B-\u200D\uFEFF]/g, '') // Zero-width characters
    
    // Clean up extra spaces
    cleanText = cleanText.replace(/\s+/g, ' ').trim()
    
    return cleanText
  } catch (error) {
    console.warn('Error cleaning text:', error)
    return text // Return original if cleaning fails
  }
}

export const truncateText = (text, maxLength = 200) => {
  if (!text || text.length <= maxLength) return text
  
  const truncated = text.substring(0, maxLength)
  const lastSpace = truncated.lastIndexOf(' ')
  
  // Cut at last space to avoid cutting words
  if (lastSpace > maxLength * 0.8) {
    return truncated.substring(0, lastSpace) + '...'
  }
  
  return truncated + '...'
}

export const formatCommentText = (text, maxLength = 300) => {
  const cleaned = cleanHtmlText(text)
  return truncateText(cleaned, maxLength)
}

// Check if text contains HTML tags
export const hasHtmlTags = (text) => {
  const htmlRegex = /<[^>]*>/
  return htmlRegex.test(text)
}

// Extract mentions from text
export const extractMentions = (text) => {
  const mentionRegex = /@[\w\s]+/g
  return text.match(mentionRegex) || []
}

// Extract URLs from text  
export const extractUrls = (text) => {
  const urlRegex = /(https?:\/\/[^\s]+)/g
  return text.match(urlRegex) || []
}