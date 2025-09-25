# 🚀 YouTube Analytics với Hume AI - Hệ thống hoàn thiện

## 📋 Tổng quan hệ thống

YouTube Analytics là một ứng dụng web hiện đại được xây dựng với **Next.js 15** và **Hume AI**, cho phép phân tích video YouTube và cảm xúc bình luận bằng trí tuệ nhân tạo tiên tiến.

## ✨ Tính năng chính

### 🎯 Phân tích Video YouTube
- **Trích xuất metadata**: Tiêu đề, mô tả, thống kê, thumbnail
- **Comment extraction**: Tự động lấy bình luận nổi bật (25-150 comments tùy độ phổ biến)
- **Smart filtering**: Lọc HTML, emoji, làm sạch nội dung
- **Dynamic limits**: Số lượng comment tự động điều chỉnh theo mức độ tương tác

### 🤖 AI Analysis với Hume AI
- **Real-time emotion detection**: Phân tích 53+ loại cảm xúc
- **Sentiment analysis**: Tích cực, tiêu cực, trung tính với độ chính xác cao
- **Topic extraction**: Tự động phát hiện chủ đề từ cảm xúc
- **Trend analysis**: Xu hướng tương tác và mức độ engagement

### 🔐 Bảo mật & Authentication
- **Google OAuth**: Đăng nhập bằng tài khoản Google
- **Session management**: Quản lý phiên làm việc an toàn
- **API key protection**: Bảo vệ khóa API trong environment variables

## 🛠 Công nghệ sử dụng

### Frontend
- **Next.js 15.5.4**: React framework với Turbopack
- **React 19.1.0**: UI library mới nhất
- **TailwindCSS 4**: Styling system hiện đại
- **NextAuth.js**: Authentication solution

### Backend
- **FastAPI**: Python web framework nhanh
- **Hume AI SDK**: Emotion analysis API
- **YouTube Data API v3**: Video & comment data
- **Uvicorn**: ASGI server

### Infrastructure  
- **Python 3.11+**: Backend runtime
- **Node.js**: Frontend runtime
- **Environment Variables**: Cấu hình an toàn

## 📦 Cài đặt và chạy

### 1. Clone repository
\`\`\`bash
git clone <repository-url>
cd tube-analytics
\`\`\`

### 2. Cài đặt dependencies

**Frontend:**
\`\`\`bash
npm install
\`\`\`

**Backend:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Cấu hình Environment Variables

Tạo file \`.env.local\`:
\`\`\`env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret

# YouTube API
YOUTUBE_API_KEY=your_youtube_api_key

# Hume AI
HUME_API_KEY=your_hume_ai_api_key

# FastAPI URL
FASTAPI_URL=http://localhost:8000
\`\`\`

### 4. Chạy ứng dụng

**Terminal 1 - Frontend:**
\`\`\`bash
npm run dev
\`\`\`

**Terminal 2 - Backend:**
\`\`\`bash
npm run fastapi-dev
\`\`\`

**Truy cập:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🎮 Hướng dẫn sử dụng

### 1. Đăng nhập
- Truy cập http://localhost:3000
- Nhấn "Đăng nhập bằng Google"
- Cho phép quyền truy cập

### 2. Phân tích video
- Paste URL YouTube vào ô input
- Nhấn "Phân tích video"
- Chờ hệ thống trích xuất dữ liệu

### 3. AI Analysis
- Sau khi có dữ liệu video, nhấn "Phân tích AI"
- **Test Raw AI**: Xem raw data từ Hume AI (5 comments đầu)
- **Phân tích AI**: Phân tích toàn bộ với kết quả có cấu trúc

### 4. Xem kết quả
- **Sentiment**: Biểu đồ cảm xúc tích cực/tiêu cực/trung tính
- **Topics**: Chủ đề cảm xúc được phát hiện
- **Trends**: Xu hướng tương tác và mức độ engagement

## 🔧 API Endpoints

### FastAPI Backend

#### \`POST /analyze\`
Phân tích bình luận với response có cấu trúc
\`\`\`json
{
  "comments": [...],
  "video_title": "Video title",
  "analysis_type": "comprehensive"
}
\`\`\`

#### \`POST /analyze-raw\`  
Phân tích raw trả về dữ liệu thô từ Hume AI
\`\`\`json
{
  "success": true,
  "hume_responses": [...],
  "total_comments": 25
}
\`\`\`

#### \`GET /debug/emotions\`
Thông tin debug và capabilities của hệ thống

#### \`GET /health\`
Health check endpoint

### Next.js API Routes

#### \`POST /api/youtube\`
Trích xuất dữ liệu từ YouTube

#### \`POST /api/ai-analysis\`
Proxy tới FastAPI analysis

#### \`POST /api/ai-raw\`
Proxy tới FastAPI raw analysis

## 📊 Kiến trúc hệ thống

\`\`\`
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend        │    │   External APIs │
│   Next.js 15    │◄──►│   FastAPI        │◄──►│   Hume AI       │
│   Port 3000     │    │   Port 8000      │    │   YouTube API   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Authentication│    │   AI Processing  │    │   Data Sources  │
│   NextAuth.js   │    │   Emotion Analysis│    │   Comments      │
│   Google OAuth  │    │   Sentiment      │    │   Video Meta    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
\`\`\`

## 🚀 Tính năng nâng cao

### Smart Comment Extraction
- **Dynamic limits**: 25-150 comments dựa trên popularity
- **Relevance ordering**: Ưu tiên comments có tương tác cao
- **HTML cleaning**: Loại bỏ tags, entities, emoji
- **Error handling**: Xử lý graceful khi API giới hạn

### Advanced AI Analysis
- **Weighted emotion scoring**: Trọng số khác nhau cho emotions
- **Multi-emotion detection**: Phát hiện đồng thời nhiều cảm xúc
- **Context-aware topics**: Chủ đề dựa trên cảm xúc
- **Engagement scoring**: Tính điểm tương tác thông minh

### Performance Optimization
- **Parallel processing**: Xử lý đồng thời multiple requests
- **Caching**: Cache kết quả để tăng tốc
- **Streaming**: Real-time data processing với Hume AI
- **Error recovery**: Tự động retry và fallback

## 🔐 Bảo mật

### API Key Management
- Environment variables cho tất cả sensitive data
- Không hardcode keys trong source code
- Separate development/production environments

### Authentication
- Secure Google OAuth flow
- Session-based authentication
- Protected API routes
- CORS configuration

### Data Protection
- Không lưu trữ personal data
- Temporary processing chỉ trong memory
- Secure API communication

## 📈 Monitoring & Debug

### Debug Endpoints
- \`/debug/emotions\`: System capabilities
- \`/health\`: Service health check
- \`/analyze-raw\`: Raw AI data inspection

### Logging
- Detailed console logging cho development
- Error tracking và reporting
- Performance metrics

### Testing
- \`Test Raw AI\` button cho debug
- Sample data validation
- API endpoint testing

## 🛠 Troubleshooting

### Common Issues

**1. "AI analysis service unavailable"**
- Kiểm tra FastAPI server đang chạy (port 8000)
- Verify HUME_API_KEY trong .env
- Check console logs cho detailed errors

**2. "Invalid video URL"**  
- URL phải là YouTube video (youtube.com/watch?v= hoặc youtu.be/)
- Video phải public và có comments enabled

**3. "Authentication failed"**
- Kiểm tra Google OAuth credentials
- Verify NEXTAUTH_URL và NEXTAUTH_SECRET
- Clear browser cache và cookies

### Performance Issues
- Reduce comment limit nếu video có quá nhiều comments
- Sử dụng \`Test Raw AI\` với ít comments để debug
- Monitor Hume AI quota usage

## 🔄 Updates & Maintenance

### Version History
- **v1.0**: Basic YouTube analysis
- **v1.5**: Hume AI integration  
- **v2.0**: Production-ready với advanced features

### Future Enhancements
- [ ] Video trend analysis over time
- [ ] Batch processing multiple videos
- [ ] Advanced visualization với charts
- [ ] Export results to PDF/Excel
- [ ] Custom emotion categories
- [ ] Real-time comment monitoring

## 💡 Tips & Best Practices

### Optimal Usage
- Test với videos có 100-1000 comments để có kết quả tốt nhất
- Sử dụng \`Test Raw AI\` trước khi chạy full analysis
- Monitor Hume AI usage để avoid quota limits

### Development
- Sử dụng \`fastapi-old\` script nếu cần fallback
- Check \`/debug/emotions\` endpoint để verify system status
- Use browser developer tools để inspect raw responses

### Production Deployment
- Set production environment variables
- Configure proper CORS settings
- Monitor API usage và performance
- Implement rate limiting

---

## 📞 Support

Nếu gặp vấn đề, hãy check:
1. Console logs (browser & terminal)
2. API endpoints health (/health)
3. Environment variables configuration
4. Network connectivity to external APIs

**Hệ thống đã hoàn thiện và sẵn sàng sử dụng! 🚀**