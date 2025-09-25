# 🎯 TubeAnalytics - AI-Powered YouTube Comment Analysis

![Project Screenshot](assets/demo1.png)

[![Demo](https://img.shields.io/badge/🚀-Live_Demo-blue?style=for-the-badge)](https://your-demo-link.vercel.app)
[![Version](https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge)]()
[![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)]()

> Phân tích cảm xúc bình luận YouTube bằng AI - Hiểu rõ phản ứng khán giả

## 📋 Tổng quan

Ứng dụng web phân tích cảm xúc bình luận YouTube sử dụng Hume AI. Trích xuất và phân tích 50+ loại cảm xúc từ bình luận, cung cấp insights về phản ứng khán giả.

![Demo Interface](assets/demo2.png)

## ✨ Tính năng

- 🎭 **Phân tích cảm xúc AI**: 50+ loại cảm xúc với Hume AI
- 📊 **Dashboard trực quan**: Biểu đồ và thống kê realtime  
- 🇻🇳 **Giao diện tiếng Việt**: Hoàn toàn bản địa hóa
- 🎯 **Smart sampling**: Tự động điều chỉnh số lượng comment (50-200)
- 📱 **Responsive**: Tương thích mọi thiết bị

![Features Dashboard](assets/demo3.png)

## 🛠️ Tech Stack

- **Next.js** - React framework & App Router
- **TailwindCSS** - Utility-first CSS styling
- **FastAPI** - Python web framework  
- **Hume AI** - Emotion analysis API
- **Google Cloud API (YouTube API)** - Comment extraction

![Analysis Results](assets/demo4.png)

## 🚀 Demo

🔗 **Live Demo**: [https://your-demo-link.vercel.app](https://your-demo-link.vercel.app)

1. Dán link YouTube video
2. Nhấn "Phân tích bằng AI" 
3. Xem kết quả sau 30-60 giây

## ⚡ Cài đặt

### Yêu cầu
- Node.js 18+
- Python 3.8+

### Setup
```bash
# Clone repo
git clone https://github.com/nguyenthephung/TubeAnalytics.git
cd TubeAnalytics

# Install dependencies
npm install
cd app/fastapi && pip install -r requirements.txt

# Environment variables
cp .env.example .env.local
# Thêm YouTube API key, Hume AI keys
```

### Chạy
```bash
# Terminal 1 - Backend
cd app/fastapi && python index.py

# Terminal 2 - Frontend  
npm run dev
```

Truy cập: `http://localhost:3000`

## 👨‍💻 Tác giả

**Nguyễn Thể Phụng**
- GitHub: [@nguyenthephung](https://github.com/nguyenthephung)
- LinkedIn: [Nguyễn Thể Phụng](https://www.linkedin.com/in/ph%E1%BB%A5ng-nguy%E1%BB%85n-th%E1%BB%83-285107385/)
- Email: your-email@domain.com

## 🙏 Credits

- [Hume AI](https://www.hume.ai/) - Emotion analysis
- [YouTube Data API](https://developers.google.com/youtube/v3) - Comment extraction
- [Next.js](https://nextjs.org/) - React framework
- [FastAPI](https://fastapi.tiangolo.com/) - Python backend



<div align="center">
  <h3>⭐ Nếu project hữu ích, hãy cho chúng tôi một star! ⭐</h3>
  
  **Made with ❤️ by Nguyễn Thể Phụng**
  
  [![GitHub stars](https://img.shields.io/github/stars/nguyenthephung/TubeAnalytics?style=social)](https://github.com/nguyenthephung/TubeAnalytics)
  [![GitHub forks](https://img.shields.io/github/forks/nguyenthephung/TubeAnalytics?style=social)](https://github.com/nguyenthephung/TubeAnalytics/fork)
  [![GitHub watchers](https://img.shields.io/github/watchers/nguyenthephung/TubeAnalytics?style=social)](https://github.com/nguyenthephung/TubeAnalytics)
</div>