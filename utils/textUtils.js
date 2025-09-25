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
      
    // Remove YouTube-specific formatting
    cleanText = cleanText
      .replace(/\n\n+/g, '\n\n') // Multiple line breaks to double
      .replace(/^\s+|\s+$/g, '') // Trim whitespace
      
    // Remove or replace emoji/special characters that might cause issues
    // Keep most Unicode characters but clean up problematic ones
    cleanText = cleanText.replace(/[\u200B-\u200D\uFEFF]/g, '') // Zero-width characters
    
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