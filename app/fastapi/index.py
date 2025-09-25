from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from hume import HumeStreamClient
from hume.models.config import LanguageConfig
from collections import defaultdict
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="YouTube Comment AI Analysis with Hume AI",
    description="Refined API for analyzing YouTube comments using Hume AI emotion detection",
    version="2.0.0"
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
HUME_API_KEY = os.getenv("HUME_API_KEY")
if not HUME_API_KEY:
    raise ValueError("HUME_API_KEY environment variable is required")

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

async def analyze_emotions_with_hume(comments: List[Comment]) -> Dict[str, Any]:
    """Send comments to Hume AI and get emotion analysis"""
    try:
        if not HUME_API_KEY:
            return {"error": "Missing Hume API key", "hume_responses": []}
        
        client = HumeStreamClient(HUME_API_KEY)
        config = LanguageConfig()
        
        print(f"📤 Sending {len(comments)} comments to Hume AI...")
        
        hume_responses = []
        
        async with client.connect([config]) as socket:
            for i, comment in enumerate(comments):
                try:
                    print(f"  📝 Processing comment {i+1}: {comment.text[:50]}...")
                    
                    result = await socket.send_text(comment.text)
                    
                    if result:
                        # Console log raw Hume AI data for debugging
                        print(f"🔍 RAW HUME DATA for comment {i+1}:")
                        print(f"   Structure: {list(result.keys()) if isinstance(result, dict) else type(result)}")
                        
                        if isinstance(result, dict) and "language" in result:
                            predictions = result.get("language", {}).get("predictions", [])
                            print(f"   Predictions count: {len(predictions)}")
                            if predictions:
                                emotions = predictions[0].get("emotions", [])
                                top_3_emotions = sorted(emotions, key=lambda x: x.get("score", 0), reverse=True)[:3]
                                print(f"   Top 3 emotions: {[(e.get('name'), round(e.get('score', 0), 3)) for e in top_3_emotions]}")
                        
                        hume_responses.append({
                            "comment_id": comment.id,
                            "comment_text": comment.text,
                            "author": comment.author,
                            "like_count": comment.likeCount,
                            "hume_result": result
                        })
                        print(f"  ✅ Success for comment {i+1}")
                    else:
                        print(f"  ⚠️ Empty result for comment {i+1}")
                    
                    
                except Exception as e:
                    print(f"  ❌ Error with comment {i+1}: {str(e)}")
                    continue
            
            print(f"✅ Processed {len(hume_responses)} comments successfully")
            
            return {
                "hume_responses": hume_responses,
                "total_comments_sent": len(comments),
                "successful_responses": len(hume_responses),
                "api_status": "success"
            }
        
    except Exception as e:
        print(f"❌ Hume AI error: {str(e)}")
        return {
            "error": str(e),
            "hume_responses": [],
            "total_comments_sent": len(comments),
            "successful_responses": 0,
            "api_status": "failed"
        }

def process_hume_emotions(hume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process Hume AI responses into meaningful insights"""
    try:
        hume_responses = hume_data.get("hume_responses", [])
        
        if not hume_responses:
            return {"emotions": {}, "sentiment_scores": {"positive": 0, "negative": 0, "neutral": 0}}
        
        print(f"🔍 PROCESSING {len(hume_responses)} Hume AI responses...")
        
        # Process each Hume AI response
        all_emotions = defaultdict(list)
        sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}
        comment_analyses = []
        
        for idx, response in enumerate(hume_responses):
            hume_result = response.get("hume_result", {})
            
            if "language" in hume_result:
                predictions = hume_result["language"].get("predictions", [])
                
                for prediction in predictions:
                    emotions = prediction.get("emotions", [])
                    
                    # Console log detailed emotion data for first few responses
                    if idx < 3:  # Debug first 3 responses
                        print(f"📊 COMMENT {idx+1} EMOTIONS:")
                        top_5 = sorted(emotions, key=lambda x: x["score"], reverse=True)[:5]
                        for e in top_5:
                            print(f"   {e['name']}: {e['score']:.3f}")
                    
                    # Get top emotions for this comment
                    top_emotions = sorted(emotions, key=lambda x: x["score"], reverse=True)[:5]
                    
                    comment_analyses.append({
                        "comment_id": response["comment_id"],
                        "comment_preview": response["comment_text"][:80] + "...",
                        "author": response["author"],
                        "top_emotions": top_emotions
                    })
                    
                    # Aggregate all emotions
                    for emotion in emotions:
                        emotion_name = emotion["name"]
                        emotion_score = emotion["score"]
                        
                        # Only count emotions with significant confidence (>0.08)
                        if emotion_score < 0.08:
                            continue
                            
                        all_emotions[emotion_name].append(emotion_score)
                        
                        # Strict sentiment categorization - only truly negative emotions count as negative
                        positive_emotions = [
                            "joy", "love", "admiration", "excitement", "amusement", "satisfaction", "pride", 
                            "relief", "gratitude", "contentment", "triumph", "ecstasy", "aesthetic appreciation",
                            "determination", "surprise (positive)", "enthusiasm", "anticipation", "interest"
                        ]
                        # Only strong negative emotions
                        negative_emotions = [
                            "anger", "disgust", "fear", "sadness", "disappointment", "contempt", "shame",
                            "guilt", "embarrassment", "annoyance", "envy", "hate", "rage", "despair"
                        ]
                        # Most emotions are neutral in YouTube comment context
                        neutral_emotions = [
                            "confusion", "doubt", "contemplation", "realization", "calmness", "boredom",
                            "concentration", "sarcasm", "nostalgia", "desire", "craving", "romance",
                            "awkwardness", "surprise (negative)", "tiredness", "empathic pain"
                        ]
                        
                        if emotion_name.lower() in positive_emotions:
                            sentiment_scores["positive"] += emotion_score
                        elif emotion_name.lower() in negative_emotions:
                            sentiment_scores["negative"] += emotion_score
                        else:
                            sentiment_scores["neutral"] += emotion_score
        
        # Calculate emotion averages
        emotion_averages = {}
        for emotion, scores in all_emotions.items():
            if scores:
                emotion_averages[emotion] = round(sum(scores) / len(scores), 3)
        
        # Console log emotion summary
        print(f"📈 EMOTION SUMMARY:")
        top_emotions_sorted = sorted(emotion_averages.items(), key=lambda x: x[1], reverse=True)[:10]
        for emotion, score in top_emotions_sorted:
            print(f"   {emotion}: {score:.3f} (avg from {len(all_emotions[emotion])} occurrences)")
        
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
    """Create structured analysis response from Hume AI data"""
    
    # Process Hume emotions
    emotion_analysis = process_hume_emotions(hume_data)
    
    # Create sentiment result
    sentiment_scores = emotion_analysis.get("sentiment_scores", {"positive": 0, "negative": 0, "neutral": 0})
    total_sentiment = sum(sentiment_scores.values())
    
    if total_sentiment > 0:
        positive_pct = round((sentiment_scores["positive"] / total_sentiment) * 100, 1)
        negative_pct = round((sentiment_scores["negative"] / total_sentiment) * 100, 1)
        neutral_pct = round((sentiment_scores["neutral"] / total_sentiment) * 100, 1)
    else:
        positive_pct = negative_pct = neutral_pct = 33.3
    
    # Estimate counts based on percentages
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
    
    # Create topics based on top emotions with better formatting
    top_emotions = emotion_analysis.get("top_emotions", [])
    topics = []
    
    # Mapping tiếng Việt cho emotions (expanded với Hume AI emotions)
    emotion_vietnamese = {
        # Basic emotions
        "joy": "Vui vẻ", "sadness": "Buồn bã", "anger": "Tức giận", "fear": "Lo sợ",
        "surprise": "Ngạc nhiên", "disgust": "Chán ghét", "love": "Yêu thích", 
        "admiration": "Ngưỡng mộ", "excitement": "Hào hứng", "amusement": "Thích thú",
        "satisfaction": "Hài lòng", "pride": "Tự hào", "relief": "Nhẹ nhõm",
        "contempt": "Khinh thường", "embarrassment": "Xấu hổ", "shame": "Hổ thẹn",
        "guilt": "Tội lỗi", "disappointment": "Thất vọng", "interest": "Quan tâm",
        "enthusiasm": "Nhiệt tình", "contemplation": "Suy ngẫm", "realization": "Nhận ra",
        "annoyance": "Khó chịu", "confusion": "Bối rối", "doubt": "Nghi ngờ",
        
        # Advanced Hume AI emotions
        "calmness": "Bình tĩnh", "contentment": "Thỏa mãn", "concentration": "Tập trung",
        "boredom": "Chán nản", "sarcasm": "Châm biếm", "awkwardness": "Ngượng ngùng",
        "surprise (negative)": "Ngạc nhiên tiêu cực", "surprise (positive)": "Ngạc nhiên tích cực",
        "determination": "Quyết tâm", "aesthetic appreciation": "Thẩm mỹ",
        "nostalgia": "Hoài niệm", "gratitude": "Biết ơn", "envy": "Ghen tị",
        "anticipation": "Mong đợi", "desire": "Khao khát", "tiredness": "Mệt mỏi",
        "romance": "Lãng mạn", "craving": "Thèm muốn", "empathic pain": "Đau lòng",
        "triumph": "Chiến thắng", "ecstasy": "Hân hoan"
    }
    
    for i, (emotion, score) in enumerate(top_emotions[:6]):
        vietnamese_name = emotion_vietnamese.get(emotion.lower(), emotion.title())
        topics.append(TopicResult(
            topic=vietnamese_name,
            count=int(score * total_analyzed) if total_analyzed > 0 else 0,
            percentage=round(score * 100, 1),
            sample_comments=[f"Cảm xúc {vietnamese_name.lower()} với độ tin cậy {score:.3f}"]
        ))
    
    # Create trends
    trends = [
        TrendResult(
            trend="Độ chính xác AI",
            score=10.0 if hume_data.get("api_status") == "success" else 0.0,
            description=f"Hume AI đã phân tích thành công {hume_data.get('successful_responses', 0)}/{hume_data.get('total_comments_sent', 0)} bình luận",
            related_comments=["Phân tích cảm xúc bằng AI hoàn tất"]
        ),
        TrendResult(
            trend="Mức độ tương tác cảm xúc",
            score=min(10.0, max(positive_pct, negative_pct) / 10),
            description=f"Phản hồi chủ yếu là {'tích cực' if positive_pct > negative_pct else 'tiêu cực' if negative_pct > positive_pct else 'trung tính'}",
            related_comments=[f"Top emotion: {top_emotions[0][0] if top_emotions else 'neutral'}"]
        )
    ]
    
    # Create summary
    top_emotion = top_emotions[0][0] if top_emotions else "neutral"
    summary = f"🤖 Hume AI đã phân tích {total_analyzed} bình luận thành công. Cảm xúc chủ đạo: {top_emotion} ({positive_pct}% tích cực, {negative_pct}% tiêu cực, {neutral_pct}% trung tính)."
    
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
    """Raw endpoint - returns actual Hume AI data without model constraints"""
    try:
        if not request.comments:
            raise HTTPException(status_code=400, detail="No comments provided")
        
        print(f"🎯 RAW Analysis for {len(request.comments)} comments")
        
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
            "note": "100% raw Hume AI response data"
        }
        
    except Exception as e:
        print(f"❌ Raw analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Raw analysis failed: {str(e)}")

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_comments(request: AnalysisRequest):
    """Main analysis endpoint with structured response"""
    try:
        if not request.comments:
            raise HTTPException(status_code=400, detail="No comments provided")
        
        print(f"🎯 Starting structured analysis for {len(request.comments)} comments")
        
        # Get Hume AI analysis
        hume_data = await analyze_emotions_with_hume(request.comments)
        
        if hume_data.get("api_status") != "success":
            raise HTTPException(status_code=500, detail=f"Hume AI failed: {hume_data.get('error', 'Unknown error')}")
        
        # Create structured analysis response
        analysis_response = create_analysis_from_hume(hume_data, request.comments)
        
        return analysis_response
        
    except Exception as e:
        print(f"❌ Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/debug/emotions")
async def debug_emotions():
    """Debug endpoint showing system capabilities"""
    return {
        "hume_ai_status": "connected" if HUME_API_KEY else "missing_key",
        "system_version": "2.0.0 - Production Ready",
        "capabilities": [
            "Real-time Hume AI emotion analysis",
            "53+ emotion types detection",
            "Dynamic comment limit (25-150 based on popularity)",
            "Sentiment analysis with weighted scoring",
            "Topic detection with emotional context",
            "Trend analysis based on engagement patterns"
        ],
        "endpoints": {
            "/analyze": "Structured analysis response",
            "/analyze-raw": "Raw Hume AI data",
            "/debug/emotions": "System information"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_version": "2.0.0",
        "ai_provider": "Hume AI",
        "hume_key_present": bool(HUME_API_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)