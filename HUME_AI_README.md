# YouTube Analytics với Hume AI

## Tính năng mới: Phân tích AI Comment với Hume AI

### 1. Cài đặt và chạy FastAPI Server

1. **Cài đặt Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Khởi chạy FastAPI server:**
   - Chạy file `start_fastapi.bat`
   - Hoặc manual: 
     ```bash
     cd app/fastapi
     python -m uvicorn index:app --reload --host 0.0.0.0 --port 8000
     ```

3. **Kiểm tra server:**
   - Truy cập: http://localhost:8000
   - Health check: http://localhost:8000/health

### 2. Sử dụng chức năng AI Analysis

1. **Phân tích video YouTube:**
   - Nhập URL YouTube và click "Phân tích"
   - Chờ lấy thông tin video và comments

2. **Phân tích AI:**
   - Click nút "Phân tích AI" sau khi có kết quả video
   - Hệ thống sẽ gửi comments tới Hume AI để phân tích cảm xúc

3. **Kết quả AI bao gồm:**
   - **Emotion Analysis**: Phân tích cảm xúc chi tiết (joy, sadness, anger, etc.)
   - **Sentiment Analysis**: Chuyển đổi cảm xúc thành sentiment (tích cực, tiêu cực, trung tính)
   - **Topic Analysis**: Trích xuất chủ đề chính trong comments
   - **Trend Analysis**: Phát hiện xu hướng dựa trên patterns cảm xúc
   - **Summary**: Tổng kết phân tích của AI

### 3. Cấu hình

**Environment Variables (.env.local):**
```
NEXTAUTH_SECRET=your_secret_here
NEXTAUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
YOUTUBE_API_KEY=your_youtube_api_key
FASTAPI_URL=http://localhost:8000
```

**FastAPI Configuration (.env in app/fastapi/):**
```
HUME_API_KEY=ghVbZYw5X4Qj2U7YqPW6H5didOaYyn4984uStf7xxGIz3vcV
```

### 4. Hume AI Features

**Emotion Detection:**
- Phân tích 53 loại cảm xúc khác nhau
- Điểm số tin cậy cho mỗi cảm xúc  
- Real-time streaming analysis
- Hỗ trợ tiếng Việt và đa ngôn ngữ

**Advanced Analytics:**
- Aggregated emotion scores
- Top emotions per comment
- Emotional trend analysis
- Sentiment conversion from emotions

### 5. Kiến trúc hệ thống

```
Next.js App (Port 3000)
├── YouTube Data API (/api/youtube)
├── AI Analysis API (/api/ai-analysis)
└── FastAPI Server (Port 8000)
    ├── Hume AI Integration
    ├── Emotion Analysis
    ├── Sentiment Conversion
    └── Trend Analysis
```

### 6. Troubleshooting

**Lỗi thường gặp:**
1. **"AI analysis service is not running"**
   - Khởi chạy FastAPI server bằng `start_fastapi.bat`

2. **"Hume AI connection failed"**
   - Kiểm tra kết nối internet
   - Kiểm tra HUME_API_KEY trong .env

3. **FastAPI import errors**
   - Cài đặt dependencies: `pip install -r requirements.txt`
   - Đặc biệt chú ý cài đặt: `pip install hume`