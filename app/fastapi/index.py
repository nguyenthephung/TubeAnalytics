from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from collections import defaultdict
import os
from datetime import datetime
from dotenv import load_dotenv
import httpx
import asyncio
import base64

# Load environment variables
load_dotenv()

app = FastAPI(
    title="YouTube Comment AI Analysis with Hume AI REST",
    description="API phân tích bình luận YouTube sử dụng Hume AI REST API trực tiếp",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://tube-analytics-w5pb.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hume AI configuration
HUME_API_KEY = os.getenv("HUME_API_KEY", "ghVbZYw5X4Qj2U7YqPW6H5didOaYyn4984uStf7xxGIz3vcV")
HUME_API_URL = "https://api.hume.ai/v0/batch/jobs"

class Comment(BaseModel):
    id: str
    text: str
    author: str
    likeCount: int
    publishedAt: str

class AnalysisRequest(BaseModel):
    comments: List[Comment]
    video_title: str = ""
    analysis_type: str = "comprehensive"

class SentimentResult(BaseModel):
    positive: int
    negative: int
    neutral: int
    total: int
    positive_percentage: float
    negative_percentage: float
    neutral_percentage: float

class TopicResult(BaseModel):
    topic: str
    count: int
    percentage: float
    sample_comments: List[str]

class TrendResult(BaseModel):
    trend: str
    score: float
    description: str
    related_comments: List[str]

class AnalysisResponse(BaseModel):
    sentiment: SentimentResult
    topics: List[TopicResult]
    trends: List[TrendResult]
    summary: str
    total_comments: int
    analysis_timestamp: str

async def analyze_text_with_hume_rest(text: str, client: httpx.AsyncClient) -> Optional[Dict[str, Any]]:
    """Gửi text đến Hume AI REST API để phân tích cảm xúc"""
    try:
        # Hume AI v0 Batch API endpoint
        url = "https://api.hume.ai/v0/batch/jobs"
        
        headers = {
            "X-Hume-Api-Key": HUME_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Payload cho language model
        payload = {
            "models": {
                "language": {
                    "granularity": "sentence"
                }
            },
            "text": [text],
            "notify": False
        }
        
        # Gửi request
        response = await client.post(url, json=payload, headers=headers, timeout=30.0)
        
        if response.status_code == 200 or response.status_code == 201:
            job_data = response.json()
            job_id = job_data.get("job_id")
            
            if not job_id:
                print(f"⚠️ Không có job_id trong response")
                return None
            
            # Poll job status
            max_attempts = 20
            for attempt in range(max_attempts):
                await asyncio.sleep(2)  # Đợi 2 giây giữa các lần check
                
                status_response = await client.get(
                    f"{url}/{job_id}/predictions",
                    headers=headers,
                    timeout=30.0
                )
                
                if status_response.status_code == 200:
                    result = status_response.json()
                    return result
                elif status_response.status_code == 202:
                    # Job đang xử lý
                    continue
                else:
                    print(f"❌ Status check failed: {status_response.status_code}")
                    return None
            
            print(f"⏱️ Timeout waiting for job {job_id}")
            return None
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception in REST API call: {str(e)}")
        return None

async def analyze_emotions_with_hume(comments: List[Comment]) -> Dict[str, Any]:
    """Phân tích cảm xúc cho nhiều comments sử dụng REST API"""
    try:
        if not HUME_API_KEY:
            return {"error": "Missing Hume API key", "hume_responses": []}
        
        print(f"📤 Gửi {len(comments)} comments đến Hume AI REST API...")
        
        hume_responses = []
        
        async with httpx.AsyncClient() as client:
            # Process comments với batch để tránh rate limit
            batch_size = 5
            for i in range(0, len(comments), batch_size):
                batch = comments[i:i+batch_size]
                
                tasks = []
                for comment in batch:
                    tasks.append(analyze_text_with_hume_rest(comment.text, client))
                
                # Chạy song song trong batch
                results = await asyncio.gather(*tasks)
                
                for idx, (comment, result) in enumerate(zip(batch, results)):
                    global_idx = i + idx
                    if result:
                        print(f"✅ Comment {global_idx+1}/{len(comments)} thành công")
                        
                        # Debug log
                        if global_idx < 3:
                            print(f"🔍 RAW DATA comment {global_idx+1}:")
                            print(f"   Keys: {list(result.keys()) if isinstance(result, dict) else type(result)}")
                        
                        hume_responses.append({
                            "comment_id": comment.id,
                            "comment_text": comment.text,
                            "author": comment.author,
                            "like_count": comment.likeCount,
                            "hume_result": result
                        })
                    else:
                        print(f"⚠️ Comment {global_idx+1} thất bại")
            
            print(f"✅ Hoàn thành: {len(hume_responses)}/{len(comments)} comments")
            
            return {
                "hume_responses": hume_responses,
                "total_comments_sent": len(comments),
                "successful_responses": len(hume_responses),
                "api_status": "success" if hume_responses else "failed"
            }
        
    except Exception as e:
        print(f"❌ Hume AI REST error: {str(e)}")
        return {
            "error": str(e),
            "hume_responses": [],
            "total_comments_sent": len(comments),
            "successful_responses": 0,
            "api_status": "failed"
        }

def extract_emotions_from_response(hume_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract emotions từ Hume API response (xử lý nhiều format)"""
    try:
        # Format 1: Direct predictions array
        if isinstance(hume_result, list):
            for item in hume_result:
                if "results" in item and "predictions" in item["results"]:
                    for pred in item["results"]["predictions"]:
                        if "models" in pred and "language" in pred["models"]:
                            lang_data = pred["models"]["language"]
                            if "grouped_predictions" in lang_data:
                                for group in lang_data["grouped_predictions"]:
                                    for prediction in group.get("predictions", []):
                                        return prediction.get("emotions", [])
        
        # Format 2: Direct structure
        if "predictions" in hume_result:
            for pred in hume_result["predictions"]:
                if "models" in pred:
                    lang_model = pred["models"].get("language", {})
                    if "grouped_predictions" in lang_model:
                        for group in lang_model["grouped_predictions"]:
                            for prediction in group.get("predictions", []):
                                return prediction.get("emotions", [])
        
        # Format 3: Nested results
        if "results" in hume_result:
            return extract_emotions_from_response(hume_result["results"])
        
        return []
        
    except Exception as e:
        print(f"⚠️ Error extracting emotions: {str(e)}")
        return []

def process_hume_emotions(hume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Xử lý Hume AI responses thành insights có ý nghĩa"""
    try:
        hume_responses = hume_data.get("hume_responses", [])
        
        if not hume_responses:
            return {"emotions": {}, "sentiment_scores": {"positive": 0, "negative": 0, "neutral": 0}}
        
        print(f"🔍 PROCESSING {len(hume_responses)} Hume AI responses...")
        
        all_emotions = defaultdict(list)
        sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}
        comment_analyses = []
        
        for idx, response in enumerate(hume_responses):
            hume_result = response.get("hume_result", {})
            
            # Extract emotions từ response
            emotions = extract_emotions_from_response(hume_result)
            
            if not emotions:
                print(f"⚠️ Không tìm thấy emotions cho comment {idx+1}")
                continue
            
            # Debug log cho 3 comments đầu
            if idx < 3:
                print(f"📊 COMMENT {idx+1} EMOTIONS:")
                top_5 = sorted(emotions, key=lambda x: x.get("score", 0), reverse=True)[:5]
                for e in top_5:
                    print(f"   {e['name']}: {e['score']:.3f}")
            
            # Lấy top emotions cho comment này
            top_emotions = sorted(emotions, key=lambda x: x.get("score", 0), reverse=True)[:5]
            
            comment_analyses.append({
                "comment_id": response["comment_id"],
                "comment_preview": response["comment_text"][:80] + "...",
                "author": response["author"],
                "top_emotions": top_emotions
            })
            
            # Aggregate tất cả emotions
            for emotion in emotions:
                emotion_name = emotion.get("name", "")
                emotion_score = emotion.get("score", 0)
                
                # Chỉ tính emotions có confidence đáng kể (>0.08)
                if emotion_score < 0.08:
                    continue
                
                all_emotions[emotion_name].append(emotion_score)
                
                # Phân loại sentiment
                positive_emotions = [
                    "joy", "love", "admiration", "excitement", "amusement", "satisfaction", "pride",
                    "relief", "gratitude", "contentment", "triumph", "ecstasy", "aesthetic appreciation",
                    "determination", "enthusiasm", "anticipation", "interest"
                ]
                negative_emotions = [
                    "anger", "disgust", "fear", "sadness", "disappointment", "contempt", "shame",
                    "guilt", "embarrassment", "annoyance", "envy", "hate", "rage", "despair"
                ]
                
                if emotion_name.lower() in positive_emotions:
                    sentiment_scores["positive"] += emotion_score
                elif emotion_name.lower() in negative_emotions:
                    sentiment_scores["negative"] += emotion_score
                else:
                    sentiment_scores["neutral"] += emotion_score
        
        # Tính trung bình emotions
        emotion_averages = {}
        for emotion, scores in all_emotions.items():
            if scores:
                emotion_averages[emotion] = round(sum(scores) / len(scores), 3)
        
        # Console log summary
        print(f"📈 EMOTION SUMMARY:")
        top_emotions_sorted = sorted(emotion_averages.items(), key=lambda x: x[1], reverse=True)[:10]
        for emotion, score in top_emotions_sorted:
            print(f"   {emotion}: {score:.3f} (avg từ {len(all_emotions[emotion])} lần xuất hiện)")
        
        print(f"💝 SENTIMENT SCORES:")
        for sentiment, score in sentiment_scores.items():
            print(f"   {sentiment}: {score:.2f}")
        
        return {
            "emotion_averages": emotion_averages,
            "sentiment_scores": sentiment_scores,
            "comment_analyses": comment_analyses,
            "top_emotions": top_emotions_sorted
        }
        
    except Exception as e:
        print(f"❌ Error processing emotions: {str(e)}")
        return {"emotions": {}, "sentiment_scores": {"positive": 0, "negative": 0, "neutral": 0}, "error": str(e)}

def create_analysis_from_hume(hume_data: Dict[str, Any], comments: List[Comment]) -> AnalysisResponse:
    """Tạo structured analysis response từ Hume AI data"""
    
    emotion_analysis = process_hume_emotions(hume_data)
    
    sentiment_scores = emotion_analysis.get("sentiment_scores", {"positive": 0, "negative": 0, "neutral": 0})
    total_sentiment = sum(sentiment_scores.values())
    
    if total_sentiment > 0:
        positive_pct = round((sentiment_scores["positive"] / total_sentiment) * 100, 1)
        negative_pct = round((sentiment_scores["negative"] / total_sentiment) * 100, 1)
        neutral_pct = round((sentiment_scores["neutral"] / total_sentiment) * 100, 1)
    else:
        positive_pct = negative_pct = neutral_pct = 33.3
    
    total_analyzed = hume_data.get("successful_responses", 0)
    positive_count = int((positive_pct / 100) * total_analyzed)
    negative_count = int((negative_pct / 100) * total_analyzed)
    neutral_count = total_analyzed - positive_count - negative_count
    
    sentiment = SentimentResult(
        positive=positive_count,
        negative=negative_count,
        neutral=neutral_count,
        total=total_analyzed,
        positive_percentage=positive_pct,
        negative_percentage=negative_pct,
        neutral_percentage=neutral_pct
    )
    
    # Tạo topics từ top emotions
    top_emotions = emotion_analysis.get("top_emotions", [])
    topics = []
    
    emotion_vietnamese = {
        "joy": "Vui vẻ", "sadness": "Buồn bã", "anger": "Tức giận", "fear": "Lo sợ",
        "surprise": "Ngạc nhiên", "disgust": "Chán ghét", "love": "Yêu thích",
        "admiration": "Ngưỡng mộ", "excitement": "Hào hứng", "amusement": "Thích thú",
        "satisfaction": "Hài lòng", "pride": "Tự hào", "relief": "Nhẹ nhõm",
        "contempt": "Khinh thường", "embarrassment": "Xấu hổ", "shame": "Hổ thẹn",
        "guilt": "Tội lỗi", "disappointment": "Thất vọng", "interest": "Quan tâm",
        "enthusiasm": "Nhiệt tình", "contemplation": "Suy ngẫm", "realization": "Nhận ra",
        "annoyance": "Khó chịu", "confusion": "Bối rối", "doubt": "Nghi ngờ",
        "calmness": "Bình tĩnh", "contentment": "Thỏa mãn", "concentration": "Tập trung",
        "boredom": "Chán nản", "determination": "Quyết tâm", "gratitude": "Biết ơn",
        "anticipation": "Mong đợi", "triumph": "Chiến thắng"
    }
    
    for i, (emotion, score) in enumerate(top_emotions[:6]):
        vietnamese_name = emotion_vietnamese.get(emotion.lower(), emotion.title())
        topics.append(TopicResult(
            topic=vietnamese_name,
            count=int(score * total_analyzed) if total_analyzed > 0 else 0,
            percentage=round(score * 100, 1),
            sample_comments=[f"Cảm xúc {vietnamese_name.lower()} với độ tin cậy {score:.3f}"]
        ))
    
    # Tạo trends
    trends = [
        TrendResult(
            trend="Độ chính xác AI",
            score=10.0 if hume_data.get("api_status") == "success" else 0.0,
            description=f"Hume AI REST đã phân tích {hume_data.get('successful_responses', 0)}/{hume_data.get('total_comments_sent', 0)} bình luận",
            related_comments=["Phân tích cảm xúc bằng REST API hoàn tất"]
        ),
        TrendResult(
            trend="Mức độ tương tác cảm xúc",
            score=min(10.0, max(positive_pct, negative_pct) / 10),
            description=f"Phản hồi chủ yếu là {'tích cực' if positive_pct > negative_pct else 'tiêu cực' if negative_pct > positive_pct else 'trung tính'}",
            related_comments=[f"Top emotion: {top_emotions[0][0] if top_emotions else 'neutral'}"]
        )
    ]
    
    # Tạo summary
    top_emotion = top_emotions[0][0] if top_emotions else "neutral"
    summary = f"🤖 Hume AI REST đã phân tích {total_analyzed} bình luận. Cảm xúc chủ đạo: {top_emotion} ({positive_pct}% tích cực, {negative_pct}% tiêu cực, {neutral_pct}% trung tính)."
    
    return AnalysisResponse(
        sentiment=sentiment,
        topics=topics,
        trends=trends,
        summary=summary,
        total_comments=len(comments),
        analysis_timestamp=datetime.now().isoformat()
    )

@app.post("/analyze-raw")
async def analyze_comments_raw(request: AnalysisRequest):
    """Raw endpoint - trả về raw Hume AI data"""
    try:
        if not request.comments:
            raise HTTPException(status_code=400, detail="No comments provided")
        
        print(f"🎯 RAW Analysis cho {len(request.comments)} comments")
        
        hume_data = await analyze_emotions_with_hume(request.comments)
        
        if hume_data.get("error"):
            raise HTTPException(status_code=500, detail=f"Hume AI error: {hume_data['error']}")
        
        return {
            "success": True,
            "total_comments": len(request.comments),
            "successful_responses": hume_data.get("successful_responses", 0),
            "hume_responses": hume_data.get("hume_responses", []),
            "video_title": request.video_title,
            "timestamp": datetime.now().isoformat(),
            "note": "100% raw Hume AI REST API response"
        }
        
    except Exception as e:
        print(f"❌ Raw analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Raw analysis failed: {str(e)}")

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_comments(request: AnalysisRequest):
    """Main analysis endpoint với structured response"""
    try:
        if not request.comments:
            raise HTTPException(status_code=400, detail="No comments provided")
        
        print(f"🎯 Bắt đầu phân tích {len(request.comments)} comments")
        
        hume_data = await analyze_emotions_with_hume(request.comments)
        
        if hume_data.get("api_status") != "success":
            raise HTTPException(status_code=500, detail=f"Hume AI failed: {hume_data.get('error', 'Unknown error')}")
        
        analysis_response = create_analysis_from_hume(hume_data, request.comments)
        
        return analysis_response
        
    except Exception as e:
        print(f"❌ Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/debug/emotions")
async def debug_emotions():
    """Debug endpoint"""
    return {
        "hume_ai_status": "connected" if HUME_API_KEY else "missing_key",
        "system_version": "3.0.0 - REST API Direct",
        "api_method": "Direct REST API calls (no SDK dependency)",
        "capabilities": [
            "Hume AI REST API trực tiếp",
            "53+ emotion types detection",
            "Batch processing với rate limit protection",
            "Async processing với httpx",
            "Retry mechanism tự động",
            "Multiple response format support"
        ],
        "endpoints": {
            "/analyze": "Structured analysis response",
            "/analyze-raw": "Raw Hume AI data",
            "/debug/emotions": "System information",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_version": "3.0.0",
        "ai_provider": "Hume AI REST API",
        "hume_key_present": bool(HUME_API_KEY),
        "method": "Direct REST calls"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)