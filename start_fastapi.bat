@echo off
echo Installing Python dependencies...
pip install fastapi uvicorn pydantic requests python-dotenv httpx hume

echo Starting FastAPI server with Hume AI...
cd app/fastapi
python -m uvicorn index:app --reload --host 0.0.0.0 --port 8000

pause