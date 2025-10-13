# Hướng dẫn Deploy lên Render

## Tổng quan cấu hình

Dự án này deploy FastAPI backend lên Render sử dụng `render.yaml`.

### Cấu trúc thư mục quan trọng:
```
tube-analytics/
├── render.yaml              # Cấu hình Render (root của repo)
└── app/
    └── fastapi/
        ├── index.py         # FastAPI app chính
        ├── requirements.txt # Python dependencies
        └── runtime.txt      # Python version (3.12.5)
```

## ✅ Checklist trước khi deploy

### 1. File cấu hình đã đúng:
- ✅ `render.yaml` - nằm ở root repo
- ✅ `app/fastapi/runtime.txt` - chứa `python-3.12.5`
- ✅ `app/fastapi/requirements.txt` - chứa tất cả dependencies
- ✅ `rootDir: app/fastapi` - trỏ đúng thư mục

### 2. Environment Variables cần thiết:

Bạn cần thêm các biến môi trường sau vào Render Dashboard (không commit vào git):

#### Bắt buộc:
```bash
HUME_API_KEY=your-hume-api-key-here
```

#### Tùy chọn (nếu cần):
```bash
YOUTUBE_API_KEY=your-youtube-key  # nếu FastAPI cần
NEXTAUTH_URL=https://your-frontend-url.com  # nếu có auth
```

**Cách thêm env vars trên Render:**
1. Vào Dashboard → Service → Environment
2. Click "Add Environment Variable"
3. Nhập key/value
4. Save Changes

### 3. Cấu hình đặc biệt cho package `hume`

Package `hume==0.4.0` yêu cầu biên dịch Rust, nên `render.yaml` đã được cấu hình:
- Cài `rustup` (Rust toolchain) trong quá trình build
- Đặt `CARGO_HOME` và `RUSTUP_HOME` vào `$HOME/.cargo`
- Cài `maturin` (công cụ build Python-Rust packages)

## 🚀 Các bước deploy

### ⭐ Option 1: Deploy qua Render Blueprint - từ `render.yaml` (KHUYẾN NGHỊ)

**Đây là cách tốt nhất vì bạn đã có `render.yaml`!**

1. **Push `render.yaml` lên repo GitHub:**
   ```powershell
   git add render.yaml
   git commit -m "Add Render config"
   git push origin main
   ```

2. **Đăng nhập Render:** https://dashboard.render.com

3. **New → Blueprint**

4. **Connect Repository:** chọn repo GitHub `TubeAnalytics`

5. **Render sẽ tự động phát hiện và đọc `render.yaml` từ root repo**
   - Service Name: `fastapi-server` (từ render.yaml)
   - Root Directory: `app/fastapi` (từ render.yaml)
   - Build/Start Commands: (đã có trong render.yaml)

6. **Review và Apply**

7. **Thêm Environment Variables** trong Dashboard:
   - Dashboard → Service → Environment
   - Add: `HUME_API_KEY` = `your-key-here`

### Option 2: Deploy thủ công qua Dashboard (nếu KHÔNG dùng render.yaml)

**Chỉ dùng option này nếu bạn KHÔNG muốn dùng `render.yaml`.**

1. **Đăng nhập Render:** https://dashboard.render.com

2. **New → Web Service**

3. **Connect Repository:** chọn repo GitHub `TubeAnalytics`

4. **Cấu hình thủ công:**
   - Name: `fastapi-server`
   - Environment: `Python 3`
   - **Root Directory: KHÔNG điền gì** (để trống hoặc `.`)
   - Branch: `main`
   
5. **Build Command** (copy/paste toàn bộ):
   ```bash
   export CARGO_HOME="$HOME/.cargo" && export RUSTUP_HOME="$HOME/.rustup" && export PATH="$CARGO_HOME/bin:$PATH" && mkdir -p "$CARGO_HOME" "$RUSTUP_HOME" && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable && source "$CARGO_HOME/env" && pip install --upgrade pip setuptools wheel && pip install maturin && pip install -r app/fastapi/requirements.txt
   ```

6. **Start Command:**
   ```bash
   cd app/fastapi && uvicorn index:app --host 0.0.0.0 --port $PORT
   ```

7. **Thêm Environment Variables** (xem mục 2 phía trên)

8. **Create Web Service**

---

### 🤔 Nên chọn Option nào?

| Tiêu chí | Option 1 (Blueprint) | Option 2 (Thủ công) |
|----------|---------------------|---------------------|
| Có `render.yaml` | ✅ Tự động đọc config | ❌ Phải nhập tay |
| Dễ cập nhật | ✅ Chỉ cần push code | ❌ Phải vào Dashboard sửa |
| Reproduce | ✅ Config trong git | ❌ Config chỉ trên Render |
| **Khuyến nghị** | ⭐ **DÙNG CÁI NÀY** | Chỉ khi không có render.yaml |

## 🔍 Kiểm tra sau khi deploy

### 1. Health check:
```bash
curl https://your-service-name.onrender.com/health
```
Kết quả mong đợi:
```json
{
  "status": "healthy",
  "service": "YouTube Comment AI Analysis"
}
```

### 2. Test API endpoint:
```bash
curl -X POST https://your-service-name.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "comments": [
      {"id": "1", "text": "Great video!", "author": "User1", "likeCount": 5, "publishedAt": "2025-01-01"}
    ],
    "video_title": "Test Video"
  }'
```

### 3. Xem logs:
- Render Dashboard → Service → Logs
- Kiểm tra lỗi build hoặc runtime

## ⚠️ Lỗi thường gặp và cách sửa

### Lỗi 1: "Read-only file system" khi build
**Nguyên nhân:** Rust toolchain cố ghi vào thư mục không có quyền.
**Giải pháp:** Đã fix trong `render.yaml` - dùng `$HOME/.cargo` thay vì `/tmp/cargo`

### Lỗi 2: "Module not found: hume"
**Nguyên nhân:** Build thất bại do thiếu Rust.
**Giải pháp:** Kiểm tra Build Logs, đảm bảo `rustup` cài thành công.

### Lỗi 3: Port binding error
**Nguyên nhân:** Dùng port cố định thay vì `$PORT`.
**Giải pháp:** Đã fix - dùng `--port $PORT` trong startCommand.

### Lỗi 4: CORS errors từ frontend
**Nguyên nhân:** FastAPI CORS middleware chưa có domain production.
**Giải pháp:** Cập nhật `app/fastapi/index.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://tube-analytics-w5pb.vercel.app",
        "https://your-production-domain.com"  # Thêm domain của bạn
    ],
    ...
)
```

## 📝 Cập nhật Frontend để trỏ tới Render backend

Sau khi deploy, cập nhật biến môi trường frontend:

**Vercel / Production:**
```bash
NEXT_PUBLIC_FASTAPI_URL=https://your-service-name.onrender.com
```

**Local development (.env.local):**
```bash
FASTAPI_URL=http://localhost:8000
```

## 🔄 Tự động deploy khi push code

Render tự động build lại khi bạn push commits lên branch `main`.

Để tắt auto-deploy:
- Dashboard → Service → Settings → Build & Deploy
- Uncheck "Auto-Deploy"

## 💡 Tips tối ưu

1. **Build time:** Build lần đầu mất ~5-10 phút (cài Rust). Các lần sau nhanh hơn nhờ cache.
2. **Free tier:** Render free tier sleep sau 15 phút không dùng. Request đầu tiên sẽ chậm (cold start).
3. **Logs:** Luôn xem logs để debug nhanh khi có lỗi.
4. **Health checks:** Render tự động ping `/health` để kiểm tra service sống.

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra Render logs
2. Xem lại env vars đã đặt đủ chưa
3. Test local trước: `cd app/fastapi && uvicorn index:app --reload`
