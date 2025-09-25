'use client'
import { useState } from 'react'
import { useSession } from 'next-auth/react'
import Image from 'next/image'
import Link from 'next/link'
import Avatar from '../../components/Avatar'
import { truncateText } from '../../utils/textUtils'

export default function AnalyzePage() {
  const { data: session } = useSession()
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [videoData, setVideoData] = useState(null)
  const [error, setError] = useState('')
  const [aiAnalysis, setAiAnalysis] = useState(null)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState('')

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!url.trim()) return

    setLoading(true)
    setError('')
    setVideoData(null)
    setAiAnalysis(null)
    setAiError('')

    try {
      const response = await fetch('/api/youtube', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url.trim() }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Có lỗi xảy ra')
      }

      setVideoData(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleAiAnalysis = async () => {
    if (!videoData || !videoData.comments || videoData.comments.length === 0) {
      setAiError('Không có bình luận để phân tích')
      return
    }

    setAiLoading(true)
    setAiError('')

    try {
      const response = await fetch('/api/ai-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          comments: videoData.comments,
          videoTitle: videoData.video.title,
          analysisType: 'comprehensive'
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Không thể phân tích bằng AI')
      }

      setAiAnalysis(data.analysis)
    } catch (err) {
      setAiError(err.message)
      console.error('AI Analysis Error:', err)
    } finally {
      setAiLoading(false)
    }
  }

  const formatNumber = (num) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
    return num?.toString()
  }

  const formatDuration = (duration) => {
    const match = duration.match(/PT(\d+H)?(\d+M)?(\d+S)?/)
    if (!match) return duration
    
    const hours = match[1] ? parseInt(match[1].slice(0, -1)) : 0
    const minutes = match[2] ? parseInt(match[2].slice(0, -1)) : 0
    const seconds = match[3] ? parseInt(match[3].slice(0, -1)) : 0
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
    }
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  if (!session) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Bạn cần đăng nhập để sử dụng tính năng này
          </h1>
          <Link href="/" className="text-red-600 hover:text-red-700 underline">
            Quay về trang chủ
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <Link href="/" className="flex items-center">
                <div className="h-8 w-8 bg-red-600 rounded-full flex items-center justify-center mr-3">
                  <svg 
                    className="h-5 w-5 text-white" 
                    fill="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                  </svg>
                </div>
                <h1 className="text-xl font-bold text-gray-900">Tube Analytics</h1>
              </Link>
              <div className="text-sm text-gray-500">
                / Phân tích video
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <Image
                  src={session.user.image}
                  alt={session.user.name}
                  width={32}
                  height={32}
                  className="rounded-full"
                />
                <span className="text-sm font-medium text-gray-700">
                  {session.user.name}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Input Form */}
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Phân tích video YouTube
            </h2>
            
            <form onSubmit={handleAnalyze} className="space-y-4">
              <div>
                <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
                  Đường link YouTube
                </label>
                <div className="flex space-x-4">
                  <input
                    type="url"
                    id="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://www.youtube.com/watch?v=..."
                    className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:ring-2 focus:ring-red-500 focus:border-red-500"
                    required
                    disabled={loading}
                  />
                  <button
                    type="submit"
                    disabled={loading || !url.trim()}
                    className="bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200"
                  >
                    {loading ? 'Đang phân tích...' : 'Phân tích'}
                  </button>
                </div>
              </div>
              
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-red-800">{error}</p>
                    </div>
                  </div>
                </div>
              )}
            </form>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="bg-white rounded-lg shadow p-8">
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mr-4"></div>
                <span className="text-lg text-gray-600">Đang lấy thông tin video...</span>
              </div>
            </div>
          )}

          {/* Video Data */}
          {videoData && (
            <div className="space-y-8">
              {/* Reset Button */}
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-gray-900">Kết quả phân tích</h2>
                <div className="flex space-x-3">
                  <button
                    onClick={handleAiAnalysis}
                    disabled={aiLoading || !videoData.comments || videoData.comments.length === 0}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center space-x-2"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a9 9 0 117.072 0l-.548.547A3.374 3.374 0 0014.846 21H9.154a3.374 3.374 0 00-2.846-1.539l-.548-.547z" />
                    </svg>
                    <span>{aiLoading ? 'Đang phân tích AI...' : 'Phân tích AI'}</span>
                  </button>
                  <button
                    onClick={() => {
                      setVideoData(null)
                      setUrl('')
                      setError('')
                      setAiAnalysis(null)
                      setAiError('')
                    }}
                    className="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
                  >
                    Phân tích video khác
                  </button>
                </div>
              </div>

              {/* AI Analysis Error */}
              {aiError && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-red-800">{aiError}</p>
                      {aiError.includes('not running') && (
                        <p className="text-sm text-red-600 mt-1">
                          Hãy khởi chạy FastAPI server bằng cách chạy file <code>start_fastapi.bat</code>
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* AI Loading State */}
              {aiLoading && (
                <div className="bg-white rounded-lg shadow p-8">
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mr-4"></div>
                    <span className="text-lg text-gray-600">Đang phân tích bình luận bằng AI...</span>
                  </div>
                </div>
              )}
              {/* Video Info */}
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="md:flex">
                  <div className="md:w-1/3">
                    <div className="relative aspect-video">
                      <Image
                        src={videoData.video.thumbnail}
                        alt={videoData.video.title}
                        fill
                        className="object-cover"
                      />
                      <div className="absolute bottom-2 right-2 bg-black bg-opacity-75 text-white text-sm px-2 py-1 rounded">
                        {formatDuration(videoData.video.duration)}
                      </div>
                    </div>
                  </div>
                  <div className="md:w-2/3 p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">
                      {videoData.video.title}
                    </h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Kênh: {videoData.video.channelTitle} • Ngày đăng: {formatDate(videoData.video.publishedAt)}
                    </p>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">{formatNumber(videoData.video.viewCount)}</div>
                        <div className="text-sm text-gray-500">Lượt xem</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">{formatNumber(videoData.video.likeCount)}</div>
                        <div className="text-sm text-gray-500">Lượt thích</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">{formatNumber(videoData.video.commentCount)}</div>
                        <div className="text-sm text-gray-500">Bình luận</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">{videoData.comments.length}</div>
                        <div className="text-sm text-gray-500">BL nổi bật</div>
                      </div>
                    </div>

                    {videoData.video.tags && videoData.video.tags.length > 0 && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-900 mb-2">Tags:</h4>
                        <div className="flex flex-wrap gap-2">
                          {videoData.video.tags.slice(0, 10).map((tag, index) => (
                            <span
                              key={index}
                              className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
                            >
                              #{tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Description */}
              {videoData.video.description && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Mô tả video</h3>
                  <div className="text-gray-700 whitespace-pre-line">
                    {videoData.video.description.length > 500 
                      ? videoData.video.description.substring(0, 500) + '...' 
                      : videoData.video.description
                    }
                  </div>
                </div>
              )}

              {/* AI Analysis Results */}
              {aiAnalysis && (
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center gap-2 mb-6">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    <h3 className="text-xl font-bold text-gray-900">Phân tích AI</h3>
                    <span className="text-sm text-gray-500 ml-auto">
                      {new Date(aiAnalysis.analysis_timestamp).toLocaleString('vi-VN')}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Sentiment Analysis */}
                    <div className="bg-gray-50 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-.464 5.535a1 1 0 10-1.415-1.414 3 3 0 01-4.242 0 1 1 0 00-1.415 1.414 5 5 0 007.072 0z" clipRule="evenodd" />
                        </svg>
                        Cảm xúc bình luận
                      </h4>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-green-600 font-medium">Tích cực</span>
                          <div className="flex items-center gap-2">
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-green-500 h-2 rounded-full"
                                style={{ width: `${aiAnalysis.sentiment.positive_percentage}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium">{aiAnalysis.sentiment.positive_percentage}%</span>
                          </div>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-red-600 font-medium">Tiêu cực</span>
                          <div className="flex items-center gap-2">
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-red-500 h-2 rounded-full"
                                style={{ width: `${aiAnalysis.sentiment.negative_percentage}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium">{aiAnalysis.sentiment.negative_percentage}%</span>
                          </div>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 font-medium">Trung tính</span>
                          <div className="flex items-center gap-2">
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-gray-500 h-2 rounded-full"
                                style={{ width: `${aiAnalysis.sentiment.neutral_percentage}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium">{aiAnalysis.sentiment.neutral_percentage}%</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Topics */}
                    <div className="bg-gray-50 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" />
                        </svg>
                        Chủ đề chính
                      </h4>
                      <div className="space-y-2">
                        {aiAnalysis.topics.slice(0, 5).map((topic, index) => (
                          <div key={index} className="flex justify-between items-center">
                            <span className="text-sm font-medium text-gray-700 truncate">
                              {topic.topic}
                            </span>
                            <span className="text-xs text-gray-500 ml-2">
                              {topic.percentage.toFixed(1)}%
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Trends */}
                    <div className="bg-gray-50 rounded-lg p-4 lg:col-span-2">
                      <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
                        </svg>
                        Xu hướng nổi bật
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {aiAnalysis.trends.map((trend, index) => (
                          <div key={index} className="bg-white rounded-lg p-3">
                            <div className="flex justify-between items-center mb-2">
                              <h5 className="font-medium text-gray-900">{trend.trend}</h5>
                              <span className="text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded-full">
                                {trend.score}/10
                              </span>
                            </div>
                            <p className="text-sm text-gray-600">{trend.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Summary */}
                    <div className="bg-blue-50 rounded-lg p-4 lg:col-span-2">
                      <h4 className="font-semibold text-blue-900 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                        </svg>
                        Tổng kết phân tích
                      </h4>
                      <p className="text-sm text-blue-800 leading-relaxed">{aiAnalysis.summary}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Comments */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-6">
                  Bình luận nổi bật ({videoData.comments.length})
                </h3>
                
                <div className="space-y-4">
                  {videoData.comments.map((comment) => (
                    <div key={comment.id} className="flex space-x-3 p-4 bg-gray-50 rounded-lg">
                      <Avatar
                        src={comment.authorImage}
                        alt={comment.author}
                        width={40}
                        height={40}
                      />
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="font-medium text-sm text-gray-900">
                            {comment.author}
                          </span>
                          <span className="text-xs text-gray-500">
                            {formatDate(comment.publishedAt)}
                          </span>
                        </div>
                        <div className="text-gray-700 text-sm mb-2 leading-relaxed">
                          <p className="whitespace-pre-wrap break-words">
                            {truncateText(comment.text, 400)}
                          </p>
                        </div>
                        <div className="flex items-center space-x-4 text-xs text-gray-500">
                          <span className="flex items-center">
                            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                            </svg>
                            {formatNumber(comment.likeCount)}
                          </span>
                          {comment.replyCount > 0 && (
                            <span>{comment.replyCount} phản hồi</span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {videoData.comments.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    Không thể lấy được bình luận cho video này
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}