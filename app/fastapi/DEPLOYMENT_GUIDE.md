# YouTube Comment Analysis API - Version 3.0.0

## Thay đổi chính:

### 1. **Requirements.txt mới** - Tối giản, không lỗi dependency:
```
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic==2.10.5
requests==2.32.3
python-dotenv==1.0.1
httpx==0.27.2
```
- ❌ Loại bỏ: `hume` SDK (gây lỗi pyaudioop, dependencies phức tạp)
- ✅ Chỉ dùng: core packages có prebuilt wheels

### 2. **index.py mới** - Dùng Hume REST API trực tiếp:
- Thay `HumeStreamClient` → gọi Hume Batch API qua `httpx`
- Có fallback: nếu Hume API fail → dùng rule-based sentiment analysis
- Đơn giản hơn, không phụ thuộc SDK phức tạp

### 3. **Cách hoạt động**:
1. Nhận comments từ frontend
2. Gửi tới **Hume AI Batch API** (REST)
3. Poll kết quả (hoặc dùng webhook trong production)
4. Nếu Hume fail → fallback sang **rule-based analysis** (keywords)
5. Trả về kết quả phân tích sentiment + emotions

### 4. **Build Command cho Render**:
```bash
cd app/fastapi && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
```

### 5. **Start Command**:
```bash
cd app/fastapi && uvicorn index:app --host 0.0.0.0 --port $PORT
```

### 6. **Environment Variables cần thiết**:
```
HUME_API_KEY=your-hume-api-key-here
```

## Test local:
```powershell
cd app\fastapi
pip install -r requirements.txt
uvicorn index:app --reload
```

Truy cập: http://localhost:8000/health

## Deploy Render:
1. Push code lên GitHub
2. Render tự động build
3. Thêm `HUME_API_KEY` trong Render Dashboard
4. Deploy thành công ✅

## API Endpoints:
- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /analyze` - Analyze comments (main endpoint)

## Ưu điểm version 3.0.0:
- ✅ Không có lỗi dependency (Rust, pyaudioop, etc.)
- ✅ Vẫn dùng Hume AI (qua REST API)
- ✅ Có fallback nếu API fail
- ✅ Deploy nhanh trên Render
- ✅ Tất cả packages có prebuilt wheels
