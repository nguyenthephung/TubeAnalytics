# Tube Analytics

Một ứng dụng phân tích YouTube được xây dựng với Next.js, NextAuth.js và TailwindCSS.

## Tính năng

- ✅ Đăng nhập với Google
- ✅ Giao diện responsive với TailwindCSS
- ✅ Bảo mật session với NextAuth.js
- 🔄 Dashboard phân tích (sắp có)
- 🔄 Phân tích hiệu suất video (sắp có)
- 🔄 Insights về khán giả (sắp có)

## Cài đặt

1. Clone repository:
```bash
git clone <your-repo-url>
cd tube-analytics
```

2. Cài đặt dependencies:
```bash
npm install
```

3. Tạo file `.env.local` và thêm các biến môi trường:
```env
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

4. Chạy ứng dụng:
```bash
npm run dev
```

5. Mở [http://localhost:3000](http://localhost:3000) trong trình duyệt.

## Cấu hình Google OAuth

1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới hoặc chọn project có sẵn
3. Bật Google+ API
4. Tạo OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized JavaScript origins: `http://localhost:3000`
   - Authorized redirect URIs: `http://localhost:3000/api/auth/callback/google`

## Công nghệ sử dụng

- **Next.js 15** - React framework
- **NextAuth.js** - Authentication
- **TailwindCSS 4** - Styling
- **React 19** - UI library

## Cấu trúc dự án

```
tube-analytics/
├── app/
│   ├── api/auth/[...nextauth]/
│   │   └── route.js          # NextAuth API routes
│   ├── auth/signin/
│   │   └── page.js           # Trang đăng nhập tùy chỉnh
│   ├── layout.js             # Root layout với AuthProvider
│   └── page.js               # Trang chủ
├── components/
│   ├── AuthProvider.js       # Session provider wrapper
│   └── Loading.js            # Component loading
├── .env.local                # Biến môi trường (không commit)
└── middleware.js             # Bảo vệ protected routes
```

## Scripts có sẵn

- `npm run dev` - Chạy development server
- `npm run build` - Build ứng dụng cho production
- `npm start` - Chạy production server
- `npm run lint` - Chạy ESLint

## Đóng góp

1. Fork dự án
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## License

Distributed under the MIT License.