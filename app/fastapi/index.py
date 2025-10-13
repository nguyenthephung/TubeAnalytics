from fastapi import FastAPI, HTTPExceptionfrom fastapi import FastAPI, HTTPExceptionfrom fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModelfrom fastapi.middleware.cors import CORSMiddlewarefrom fastapi.middleware.cors import CORSMiddleware

from typing import List, Dict, Any

from collections import defaultdictfrom pydantic import BaseModelfrom pydantic import BaseModel

import os

from datetime import datetimefrom typing import List, Dict, Anyfrom typing import List, Dict, Any

from dotenv import load_dotenv

import httpxfrom collections import defaultdictfrom collections import defaultdict



load_dotenv()import osimport os



app = FastAPI(from datetime import datetimefrom datetime import datetime

    title="YouTube Comment AI Analysis",

    version="3.0.0"from dotenv import load_dotenvfrom dotenv import load_dotenv

)

import httpximport httpx

app.add_middleware(

    CORSMiddleware,import asyncioimport asyncio

    allow_origins=["http://localhost:3000", "https://tube-analytics-w5pb.vercel.app"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],# Load environment variables# Load environment variables

)

load_dotenv()load_dotenv()

HUME_API_KEY = os.getenv("HUME_API_KEY")



class Comment(BaseModel):

    id: strapp = FastAPI(app = FastAPI(

    text: str

    author: str    title="YouTube Comment AI Analysis with Hume AI",    title="YouTube Comment AI Analysis with Hume AI",

    likeCount: int

    publishedAt: str    description="API for analyzing YouTube comments using Hume AI emotion detection via REST API",    description="API for analyzing YouTube comments using Hume AI emotion detection via REST API",



class AnalysisRequest(BaseModel):    version="3.0.0"    version="3.0.0"

    comments: List[Comment]

    video_title: str = ""))

    analysis_type: str = "comprehensive"



class SentimentResult(BaseModel):

    positive: int# CORS middleware# CORS middleware

    negative: int

    neutral: intapp.add_middleware(app.add_middleware(

    total: int

    positive_percentage: float    CORSMiddleware,    CORSMiddleware,

    negative_percentage: float

    neutral_percentage: float    allow_origins=[    allow_origins=[



class TopicResult(BaseModel):        "http://localhost:3000",        "http://localhost:3000",

    topic: str

    count: int        "https://tube-analytics-w5pb.vercel.app"        "https://tube-analytics-w5pb.vercel.app"

    percentage: float

    sample_comments: List[str]    ],    ],



class TrendResult(BaseModel):    allow_credentials=True,    allow_credentials=True,

    trend: str

    score: float    allow_methods=["*"],    allow_methods=["*"],

    description: str

    related_comments: List[str]    allow_headers=["*"],    allow_headers=["*"],



class AnalysisResponse(BaseModel):))

    sentiment: SentimentResult

    topics: List[TopicResult]

    trends: List[TrendResult]

    summary: str# Hume AI configuration# Hume AI configuration

    total_comments: int

    analysis_timestamp: strHUME_API_KEY = os.getenv("HUME_API_KEY")HUME_API_KEY = os.getenv("HUME_API_KEY")



async def rule_based_analysis(comments: List[Comment]) -> Dict[str, Any]:HUME_API_URL = "https://api.hume.ai/v0/batch/jobs"HUME_API_URL = "https://api.hume.ai/v0/batch/jobs"

    """Rule-based sentiment analysis"""

    print(f"🤖 Analyzing {len(comments)} comments with rule-based method")

    

    positive_keywords = ["good", "great", "love", "awesome", "amazing", "excellent", "best", "perfect", "nice", "beautiful", "thank", "thanks", "tuyệt", "hay", "đẹp", "thích", "tốt", "cảm ơn"]class Comment(BaseModel):class Comment(BaseModel):

    negative_keywords = ["bad", "hate", "worst", "terrible", "awful", "disappointing", "poor", "boring", "sucks", "stupid", "tệ", "dở", "chán", "ghét", "tồi", "kém"]

        id: str    id: str

    results = []

    sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}    text: str    text: str

    

    for comment in comments:    author: str    author: str

        text_lower = comment.text.lower()

        pos_count = sum(1 for word in positive_keywords if word in text_lower)    likeCount: int    likeCount: int

        neg_count = sum(1 for word in negative_keywords if word in text_lower)

            publishedAt: str    publishedAt: str

        if pos_count > neg_count:

            sentiment = "positive"

            sentiment_scores["positive"] += 1

            top_emotion = "joy"class AnalysisRequest(BaseModel):class AnalysisRequest(BaseModel):

        elif neg_count > pos_count:

            sentiment = "negative"    comments: List[Comment]    comments: List[Comment]

            sentiment_scores["negative"] += 1

            top_emotion = "sadness"    video_title: str = ""    video_title: str = ""

        else:

            sentiment = "neutral"    analysis_type: str = "comprehensive"    analysis_type: str = "comprehensive"

            sentiment_scores["neutral"] += 1

            top_emotion = "neutral"

        

        results.append({class SentimentResult(BaseModel):class SentimentResult(BaseModel):

            "comment_id": comment.id,

            "sentiment": sentiment,    positive: int    positive: int

            "top_emotion": top_emotion

        })    negative: int    negative: int

    

    return {    neutral: int    neutral: int

        "analysis_results": results,

        "sentiment_scores": sentiment_scores,    total: int    total: int

        "total_analyzed": len(comments),

        "method": "rule_based"    positive_percentage: float    positive_percentage: float

    }

    negative_percentage: float    negative_percentage: float

def create_analysis_response(analysis_data: Dict[str, Any], comments: List[Comment]) -> AnalysisResponse:

    """Create response"""    neutral_percentage: float    neutral_percentage: float

    sentiment_scores = analysis_data.get("sentiment_scores", {"positive": 0, "negative": 0, "neutral": 0})

    total = sum(sentiment_scores.values())

    

    if total > 0:class TopicResult(BaseModel):class TopicResult(BaseModel):

        positive_pct = round((sentiment_scores["positive"] / total) * 100, 1)

        negative_pct = round((sentiment_scores["negative"] / total) * 100, 1)    topic: str    topic: str

        neutral_pct = round((sentiment_scores["neutral"] / total) * 100, 1)

    else:    count: int    count: int

        positive_pct = negative_pct = neutral_pct = 33.3

        percentage: float    percentage: float

    sentiment = SentimentResult(

        positive=sentiment_scores["positive"],    sample_comments: List[str]    sample_comments: List[str]

        negative=sentiment_scores["negative"],

        neutral=sentiment_scores["neutral"],

        total=total,

        positive_percentage=positive_pct,class TrendResult(BaseModel):class TrendResult(BaseModel):

        negative_percentage=negative_pct,

        neutral_percentage=neutral_pct    trend: str    trend: str

    )

        score: float    score: float

    emotion_vietnamese = {

        "joy": "Vui vẻ", "sadness": "Buồn bã", "neutral": "Trung tính",    description: str    description: str

        "anger": "Tức giận", "love": "Yêu thích", "excitement": "Hào hứng"

    }    related_comments: List[str]    related_comments: List[str]

    

    emotion_counts = defaultdict(int)

    for result in analysis_data.get("analysis_results", []):

        emotion = result.get("top_emotion", "neutral")class AnalysisResponse(BaseModel):class AnalysisResponse(BaseModel):

        emotion_counts[emotion] += 1

        sentiment: SentimentResult    sentiment: SentimentResult

    topics = []

    for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:6]:    topics: List[TopicResult]    topics: List[TopicResult]

        vietnamese_name = emotion_vietnamese.get(emotion, emotion.title())

        percentage = round((count / total * 100), 1) if total > 0 else 0    trends: List[TrendResult]    trends: List[TrendResult]

        topics.append(TopicResult(

            topic=vietnamese_name,    summary: str    summary: str

            count=count,

            percentage=percentage,    total_comments: int    total_comments: int

            sample_comments=[f"Phát hiện cảm xúc {vietnamese_name.lower()}"]

        ))    analysis_timestamp: str    analysis_timestamp: str

    

    method = analysis_data.get("method", "unknown")

    trends = [

        TrendResult(async def analyze_with_hume_batch(comments: List[Comment]) -> Dict[str, Any]:async def analyze_emotions_with_hume(comments: List[Comment]) -> Dict[str, Any]:

            trend="Phương pháp phân tích",

            score=7.0,    """    """Send comments to Hume AI and get emotion analysis"""

            description=f"Sử dụng phân tích dựa trên quy tắc",

            related_comments=[f"Đã phân tích {total} bình luận"]    Analyze comments using Hume AI Batch API    try:

        )

    ]    Fallback to rule-based analysis if API fails        if not HUME_API_KEY:

    

    top_emotion = list(emotion_counts.keys())[0] if emotion_counts else "neutral"    """            return {"error": "Missing Hume API key", "hume_responses": []}

    summary = f"📊 Đã phân tích {total} bình luận. ({positive_pct}% tích cực, {negative_pct}% tiêu cực, {neutral_pct}% trung tính)."

        if not HUME_API_KEY:        

    return AnalysisResponse(

        sentiment=sentiment,        print("⚠️ Hume API key not found, using rule-based analysis")        client = HumeStreamClient(HUME_API_KEY)

        topics=topics,

        trends=trends,        return await rule_based_analysis(comments)        config = LanguageConfig()

        summary=summary,

        total_comments=len(comments),            

        analysis_timestamp=datetime.now().isoformat()

    )    try:        print(f"📤 Sending {len(comments)} comments to Hume AI...")



@app.post("/analyze", response_model=AnalysisResponse)        async with httpx.AsyncClient(timeout=30.0) as client:        

async def analyze_comments(request: AnalysisRequest):

    """Main analysis endpoint"""            # Prepare texts for batch analysis        hume_responses = []

    try:

        if not request.comments:            texts = [{"text": comment.text} for comment in comments[:50]]  # Limit to 50 comments        

            raise HTTPException(status_code=400, detail="No comments provided")

                            async with client.connect([config]) as socket:

        print(f"🎯 Analyzing {len(request.comments)} comments")

        analysis_data = await rule_based_analysis(request.comments)            headers = {            for i, comment in enumerate(comments):

        response = create_analysis_response(analysis_data, request.comments)

        return response                "X-Hume-Api-Key": HUME_API_KEY,                try:

        

    except Exception as e:                "Content-Type": "application/json"                    print(f"  📝 Processing comment {i+1}: {comment.text[:50]}...")

        print(f"❌ Analysis error: {str(e)}")

        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")            }                    



@app.get("/health")                                result = await socket.send_text(comment.text)

async def health_check():

    return {            payload = {                    

        "status": "healthy",

        "timestamp": datetime.now().isoformat(),                "models": {                    if result:

        "api_version": "3.0.0",

        "ai_provider": "Rule-based (Hume AI integration ready)",                    "language": {                        # Console log raw Hume AI data for debugging

        "hume_key_present": bool(HUME_API_KEY)

    }                        "granularity": "sentence"                        print(f"🔍 RAW HUME DATA for comment {i+1}:")



@app.get("/")                    }                        print(f"   Structure: {list(result.keys()) if isinstance(result, dict) else type(result)}")

async def root():

    return {                },                        

        "message": "YouTube Comment Analysis API",

        "version": "3.0.0",                "text": texts                        if isinstance(result, dict) and "language" in result:

        "status": "operational"

    }            }                            predictions = result.get("language", {}).get("predictions", [])



if __name__ == "__main__":                                        print(f"   Predictions count: {len(predictions)}")

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)            print(f"📤 Sending {len(texts)} comments to Hume AI Batch API...")                            if predictions:


                                            emotions = predictions[0].get("emotions", [])

            # Submit batch job                                top_3_emotions = sorted(emotions, key=lambda x: x.get("score", 0), reverse=True)[:3]

            response = await client.post(                                print(f"   Top 3 emotions: {[(e.get('name'), round(e.get('score', 0), 3)) for e in top_3_emotions]}")

                HUME_API_URL,                        

                json=payload,                        hume_responses.append({

                headers=headers                            "comment_id": comment.id,

            )                            "comment_text": comment.text,

                                        "author": comment.author,

            if response.status_code != 200:                            "like_count": comment.likeCount,

                print(f"⚠️ Hume API error {response.status_code}, falling back to rule-based")                            "hume_result": result

                return await rule_based_analysis(comments)                        })

                                    print(f"  ✅ Success for comment {i+1}")

            job_data = response.json()                    else:

            job_id = job_data.get("job_id")                        print(f"  ⚠️ Empty result for comment {i+1}")

                                

            if not job_id:                    

                print("⚠️ No job_id returned, falling back to rule-based")                except Exception as e:

                return await rule_based_analysis(comments)                    print(f"  ❌ Error with comment {i+1}: {str(e)}")

                                continue

            print(f"✅ Job submitted: {job_id}")            

                        print(f"✅ Processed {len(hume_responses)} comments successfully")

            # Poll for results (simplified - in production use webhooks)            

            max_attempts = 10            return {

            for attempt in range(max_attempts):                "hume_responses": hume_responses,

                await asyncio.sleep(2)  # Wait 2 seconds between polls                "total_comments_sent": len(comments),

                                "successful_responses": len(hume_responses),

                status_response = await client.get(                "api_status": "success"

                    f"{HUME_API_URL}/{job_id}",            }

                    headers=headers        

                )    except Exception as e:

                        print(f"❌ Hume AI error: {str(e)}")

                if status_response.status_code == 200:        return {

                    job_status = status_response.json()            "error": str(e),

                    state = job_status.get("state", {}).get("status")            "hume_responses": [],

                                "total_comments_sent": len(comments),

                    if state == "COMPLETED":            "successful_responses": 0,

                        # Get predictions            "api_status": "failed"

                        predictions_url = job_status.get("state", {}).get("predictions_url")        }

                        if predictions_url:

                            pred_response = await client.get(predictions_url, headers=headers)def process_hume_emotions(hume_data: Dict[str, Any]) -> Dict[str, Any]:

                            if pred_response.status_code == 200:    """Process Hume AI responses into meaningful insights"""

                                predictions = pred_response.json()    try:

                                return process_hume_results(predictions, comments)        hume_responses = hume_data.get("hume_responses", [])

                    elif state == "FAILED":        

                        print("⚠️ Hume job failed, falling back")        if not hume_responses:

                        break            return {"emotions": {}, "sentiment_scores": {"positive": 0, "negative": 0, "neutral": 0}}

                    

            # If we get here, timeout or failure        print(f"🔍 PROCESSING {len(hume_responses)} Hume AI responses...")

            print("⚠️ Hume API timeout, falling back to rule-based")        

            return await rule_based_analysis(comments)        # Process each Hume AI response

                    all_emotions = defaultdict(list)

    except Exception as e:        sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}

        print(f"❌ Hume AI error: {str(e)}, falling back to rule-based")        comment_analyses = []

        return await rule_based_analysis(comments)        

        for idx, response in enumerate(hume_responses):

async def rule_based_analysis(comments: List[Comment]) -> Dict[str, Any]:            hume_result = response.get("hume_result", {})

    """            

    Simple rule-based sentiment analysis as fallback            if "language" in hume_result:

    """                predictions = hume_result["language"].get("predictions", [])

    print(f"🤖 Using rule-based analysis for {len(comments)} comments")                

                    for prediction in predictions:

    # Keywords for sentiment detection                    emotions = prediction.get("emotions", [])

    positive_keywords = [                    

        "good", "great", "love", "awesome", "amazing", "excellent", "fantastic", "wonderful",                    # Console log detailed emotion data for first few responses

        "best", "perfect", "nice", "beautiful", "thank", "thanks", "appreciate", "helpful",                    if idx < 3:  # Debug first 3 responses

        "tuyệt", "hay", "đẹp", "thích", "tốt", "cảm ơn", "xuất sắc", "tuyệt vời"                        print(f"📊 COMMENT {idx+1} EMOTIONS:")

    ]                        top_5 = sorted(emotions, key=lambda x: x["score"], reverse=True)[:5]

                            for e in top_5:

    negative_keywords = [                            print(f"   {e['name']}: {e['score']:.3f}")

        "bad", "hate", "worst", "terrible", "awful", "horrible", "disappointing", "poor",                    

        "useless", "waste", "boring", "sucks", "dumb", "stupid", "trash", "garbage",                    # Get top emotions for this comment

        "tệ", "dở", "chán", "ghét", "tồi", "kém", "thất vọng"                    top_emotions = sorted(emotions, key=lambda x: x["score"], reverse=True)[:5]

    ]                    

                        comment_analyses.append({

    results = []                        "comment_id": response["comment_id"],

    sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}                        "comment_preview": response["comment_text"][:80] + "...",

                            "author": response["author"],

    for comment in comments:                        "top_emotions": top_emotions

        text_lower = comment.text.lower()                    })

                            

        pos_count = sum(1 for word in positive_keywords if word in text_lower)                    # Aggregate all emotions

        neg_count = sum(1 for word in negative_keywords if word in text_lower)                    for emotion in emotions:

                                emotion_name = emotion["name"]

        if pos_count > neg_count:                        emotion_score = emotion["score"]

            sentiment = "positive"                        

            sentiment_scores["positive"] += 1                        # Only count emotions with significant confidence (>0.08)

            top_emotion = "joy"                        if emotion_score < 0.08:

            score = min(0.9, 0.5 + pos_count * 0.1)                            continue

        elif neg_count > pos_count:                            

            sentiment = "negative"                        all_emotions[emotion_name].append(emotion_score)

            sentiment_scores["negative"] += 1                        

            top_emotion = "anger" if "hate" in text_lower or "worst" in text_lower else "sadness"                        # Strict sentiment categorization - only truly negative emotions count as negative

            score = min(0.9, 0.5 + neg_count * 0.1)                        positive_emotions = [

        else:                            "joy", "love", "admiration", "excitement", "amusement", "satisfaction", "pride", 

            sentiment = "neutral"                            "relief", "gratitude", "contentment", "triumph", "ecstasy", "aesthetic appreciation",

            sentiment_scores["neutral"] += 1                            "determination", "surprise (positive)", "enthusiasm", "anticipation", "interest"

            top_emotion = "calmness"                        ]

            score = 0.6                        # Only strong negative emotions

                                negative_emotions = [

        results.append({                            "anger", "disgust", "fear", "sadness", "disappointment", "contempt", "shame",

            "comment_id": comment.id,                            "guilt", "embarrassment", "annoyance", "envy", "hate", "rage", "despair"

            "comment_text": comment.text,                        ]

            "author": comment.author,                        # Most emotions are neutral in YouTube comment context

            "sentiment": sentiment,                        neutral_emotions = [

            "top_emotion": top_emotion,                            "confusion", "doubt", "contemplation", "realization", "calmness", "boredom",

            "confidence": score                            "concentration", "sarcasm", "nostalgia", "desire", "craving", "romance",

        })                            "awkwardness", "surprise (negative)", "tiredness", "empathic pain"

                            ]

    return {                        

        "analysis_results": results,                        if emotion_name.lower() in positive_emotions:

        "sentiment_scores": sentiment_scores,                            sentiment_scores["positive"] += emotion_score

        "total_analyzed": len(comments),                        elif emotion_name.lower() in negative_emotions:

        "method": "rule_based"                            sentiment_scores["negative"] += emotion_score

    }                        else:

                            sentiment_scores["neutral"] += emotion_score

def process_hume_results(predictions: Dict[str, Any], comments: List[Comment]) -> Dict[str, Any]:        

    """Process Hume API predictions into our format"""        # Calculate emotion averages

    try:        emotion_averages = {}

        results = []        for emotion, scores in all_emotions.items():

        sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}            if scores:

                        emotion_averages[emotion] = round(sum(scores) / len(scores), 3)

        # Hume returns predictions in format: [{"results": {"predictions": [...]}}]        

        for idx, prediction_block in enumerate(predictions):        # Console log emotion summary

            if idx >= len(comments):        print(f"📈 EMOTION SUMMARY:")

                break        top_emotions_sorted = sorted(emotion_averages.items(), key=lambda x: x[1], reverse=True)[:10]

                        for emotion, score in top_emotions_sorted:

            comment = comments[idx]            print(f"   {emotion}: {score:.3f} (avg from {len(all_emotions[emotion])} occurrences)")

            pred_results = prediction_block.get("results", {}).get("predictions", [])        

                    print(f"💝 SENTIMENT SCORES:")

            if pred_results:        for sentiment, score in sentiment_scores.items():

                # Get language model predictions            print(f"   {sentiment}: {score:.2f}")

                lang_pred = pred_results[0].get("models", {}).get("language", {}).get("grouped_predictions", [])        

                        return {

                if lang_pred:            "emotion_averages": emotion_averages,

                    emotions = lang_pred[0].get("predictions", [{}])[0].get("emotions", [])            "sentiment_scores": sentiment_scores,

                                "comment_analyses": comment_analyses,

                    # Get top emotion            "top_emotions": top_emotions_sorted

                    top_emotions = sorted(emotions, key=lambda x: x.get("score", 0), reverse=True)[:3]        }

                    top_emotion = top_emotions[0] if top_emotions else {"name": "neutral", "score": 0.5}        

                        except Exception as e:

                    # Determine sentiment        print(f"❌ Error processing emotions: {str(e)}")

                    positive_emotions = ["joy", "love", "admiration", "excitement", "satisfaction", "amusement"]        return {"emotions": {}, "sentiment_scores": {"positive": 0, "negative": 0, "neutral": 0}, "error": str(e)}

                    negative_emotions = ["anger", "fear", "sadness", "disgust", "disappointment"]

                    def create_analysis_from_hume(hume_data: Dict[str, Any], comments: List[Comment]) -> AnalysisResponse:

                    top_name = top_emotion.get("name", "neutral").lower()    """Create structured analysis response from Hume AI data"""

                    if any(pos in top_name for pos in positive_emotions):    

                        sentiment = "positive"    # Process Hume emotions

                        sentiment_scores["positive"] += 1    emotion_analysis = process_hume_emotions(hume_data)

                    elif any(neg in top_name for neg in negative_emotions):    

                        sentiment = "negative"    # Create sentiment result

                        sentiment_scores["negative"] += 1    sentiment_scores = emotion_analysis.get("sentiment_scores", {"positive": 0, "negative": 0, "neutral": 0})

                    else:    total_sentiment = sum(sentiment_scores.values())

                        sentiment = "neutral"    

                        sentiment_scores["neutral"] += 1    if total_sentiment > 0:

                            positive_pct = round((sentiment_scores["positive"] / total_sentiment) * 100, 1)

                    results.append({        negative_pct = round((sentiment_scores["negative"] / total_sentiment) * 100, 1)

                        "comment_id": comment.id,        neutral_pct = round((sentiment_scores["neutral"] / total_sentiment) * 100, 1)

                        "comment_text": comment.text,    else:

                        "author": comment.author,        positive_pct = negative_pct = neutral_pct = 33.3

                        "sentiment": sentiment,    

                        "top_emotion": top_emotion.get("name"),    # Estimate counts based on percentages

                        "confidence": top_emotion.get("score", 0)    total_analyzed = hume_data.get("successful_responses", 0)

                    })    positive_count = int((positive_pct / 100) * total_analyzed)

            negative_count = int((negative_pct / 100) * total_analyzed)

        return {    neutral_count = total_analyzed - positive_count - negative_count

            "analysis_results": results,    

            "sentiment_scores": sentiment_scores,    sentiment = SentimentResult(

            "total_analyzed": len(results),        positive=positive_count,

            "method": "hume_ai"        negative=negative_count,

        }        neutral=neutral_count,

                total=total_analyzed,

    except Exception as e:        positive_percentage=positive_pct,

        print(f"❌ Error processing Hume results: {str(e)}")        negative_percentage=negative_pct,

        # Fallback to empty results        neutral_percentage=neutral_pct

        return {    )

            "analysis_results": [],    

            "sentiment_scores": {"positive": 0, "negative": 0, "neutral": 0},    # Create topics based on top emotions with better formatting

            "total_analyzed": 0,    top_emotions = emotion_analysis.get("top_emotions", [])

            "method": "error"    topics = []

        }    

    # Mapping tiếng Việt cho emotions (expanded với Hume AI emotions)

def create_analysis_response(analysis_data: Dict[str, Any], comments: List[Comment]) -> AnalysisResponse:    emotion_vietnamese = {

    """Create structured response from analysis data"""        # Basic emotions

            "joy": "Vui vẻ", "sadness": "Buồn bã", "anger": "Tức giận", "fear": "Lo sợ",

    sentiment_scores = analysis_data.get("sentiment_scores", {"positive": 0, "negative": 0, "neutral": 0})        "surprise": "Ngạc nhiên", "disgust": "Chán ghét", "love": "Yêu thích", 

    total = sum(sentiment_scores.values())        "admiration": "Ngưỡng mộ", "excitement": "Hào hứng", "amusement": "Thích thú",

            "satisfaction": "Hài lòng", "pride": "Tự hào", "relief": "Nhẹ nhõm",

    if total > 0:        "contempt": "Khinh thường", "embarrassment": "Xấu hổ", "shame": "Hổ thẹn",

        positive_pct = round((sentiment_scores["positive"] / total) * 100, 1)        "guilt": "Tội lỗi", "disappointment": "Thất vọng", "interest": "Quan tâm",

        negative_pct = round((sentiment_scores["negative"] / total) * 100, 1)        "enthusiasm": "Nhiệt tình", "contemplation": "Suy ngẫm", "realization": "Nhận ra",

        neutral_pct = round((sentiment_scores["neutral"] / total) * 100, 1)        "annoyance": "Khó chịu", "confusion": "Bối rối", "doubt": "Nghi ngờ",

    else:        

        positive_pct = negative_pct = neutral_pct = 33.3        # Advanced Hume AI emotions

            "calmness": "Bình tĩnh", "contentment": "Thỏa mãn", "concentration": "Tập trung",

    sentiment = SentimentResult(        "boredom": "Chán nản", "sarcasm": "Châm biếm", "awkwardness": "Ngượng ngùng",

        positive=sentiment_scores["positive"],        "surprise (negative)": "Ngạc nhiên tiêu cực", "surprise (positive)": "Ngạc nhiên tích cực",

        negative=sentiment_scores["negative"],        "determination": "Quyết tâm", "aesthetic appreciation": "Thẩm mỹ",

        neutral=sentiment_scores["neutral"],        "nostalgia": "Hoài niệm", "gratitude": "Biết ơn", "envy": "Ghen tị",

        total=total,        "anticipation": "Mong đợi", "desire": "Khao khát", "tiredness": "Mệt mỏi",

        positive_percentage=positive_pct,        "romance": "Lãng mạn", "craving": "Thèm muốn", "empathic pain": "Đau lòng",

        negative_percentage=negative_pct,        "triumph": "Chiến thắng", "ecstasy": "Hân hoan"

        neutral_percentage=neutral_pct    }

    )    

        for i, (emotion, score) in enumerate(top_emotions[:6]):

    # Create topics from emotions        vietnamese_name = emotion_vietnamese.get(emotion.lower(), emotion.title())

    emotion_counts = defaultdict(int)        topics.append(TopicResult(

    for result in analysis_data.get("analysis_results", []):            topic=vietnamese_name,

        emotion = result.get("top_emotion", "neutral")            count=int(score * total_analyzed) if total_analyzed > 0 else 0,

        emotion_counts[emotion] += 1            percentage=round(score * 100, 1),

                sample_comments=[f"Cảm xúc {vietnamese_name.lower()} với độ tin cậy {score:.3f}"]

    # Vietnamese emotion mapping        ))

    emotion_vietnamese = {    

        "joy": "Vui vẻ", "sadness": "Buồn bã", "anger": "Tức giận", "fear": "Lo sợ",    # Create trends

        "surprise": "Ngạc nhiên", "disgust": "Chán ghét", "love": "Yêu thích",    trends = [

        "admiration": "Ngưỡng mộ", "excitement": "Hào hứng", "amusement": "Thích thú",        TrendResult(

        "satisfaction": "Hài lòng", "calmness": "Bình tĩnh", "neutral": "Trung tính"            trend="Độ chính xác AI",

    }            score=10.0 if hume_data.get("api_status") == "success" else 0.0,

                description=f"Hume AI đã phân tích thành công {hume_data.get('successful_responses', 0)}/{hume_data.get('total_comments_sent', 0)} bình luận",

    topics = []            related_comments=["Phân tích cảm xúc bằng AI hoàn tất"]

    for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:6]:        ),

        vietnamese_name = emotion_vietnamese.get(emotion, emotion.title())        TrendResult(

        percentage = round((count / total * 100), 1) if total > 0 else 0            trend="Mức độ tương tác cảm xúc",

        topics.append(TopicResult(            score=min(10.0, max(positive_pct, negative_pct) / 10),

            topic=vietnamese_name,            description=f"Phản hồi chủ yếu là {'tích cực' if positive_pct > negative_pct else 'tiêu cực' if negative_pct > positive_pct else 'trung tính'}",

            count=count,            related_comments=[f"Top emotion: {top_emotions[0][0] if top_emotions else 'neutral'}"]

            percentage=percentage,        )

            sample_comments=[f"Phát hiện cảm xúc {vietnamese_name.lower()}"]    ]

        ))    

        # Create summary

    # Create trends    top_emotion = top_emotions[0][0] if top_emotions else "neutral"

    method = analysis_data.get("method", "unknown")    summary = f"🤖 Hume AI đã phân tích {total_analyzed} bình luận thành công. Cảm xúc chủ đạo: {top_emotion} ({positive_pct}% tích cực, {negative_pct}% tiêu cực, {neutral_pct}% trung tính)."

    trends = [    

        TrendResult(    return AnalysisResponse(

            trend="Phương pháp phân tích",        sentiment=sentiment,

            score=10.0 if method == "hume_ai" else 7.0,        topics=topics,

            description=f"Sử dụng {'Hume AI' if method == 'hume_ai' else 'phân tích dựa trên quy tắc'}",        trends=trends,

            related_comments=[f"Đã phân tích {total} bình luận"]        summary=summary,

        ),        total_comments=len(comments),

        TrendResult(        analysis_timestamp=datetime.now().isoformat()

            trend="Xu hướng chung",    )

            score=max(positive_pct, negative_pct, neutral_pct) / 10,

            description=f"Phản hồi chủ yếu {'tích cực' if positive_pct > max(negative_pct, neutral_pct) else 'tiêu cực' if negative_pct > neutral_pct else 'trung tính'}",@app.post("/analyze-raw")

            related_comments=[f"{positive_pct}% tích cực, {negative_pct}% tiêu cực"]async def analyze_comments_raw(request: AnalysisRequest):

        )    """Raw endpoint - returns actual Hume AI data without model constraints"""

    ]    try:

            if not request.comments:

    # Summary            raise HTTPException(status_code=400, detail="No comments provided")

    top_emotion = list(emotion_counts.keys())[0] if emotion_counts else "neutral"        

    summary = f"📊 Đã phân tích {total} bình luận. Cảm xúc chủ đạo: {emotion_vietnamese.get(top_emotion, top_emotion)} ({positive_pct}% tích cực, {negative_pct}% tiêu cực, {neutral_pct}% trung tính)."        print(f"🎯 RAW Analysis for {len(request.comments)} comments")

            

    return AnalysisResponse(        hume_data = await analyze_emotions_with_hume(request.comments)

        sentiment=sentiment,        

        topics=topics,        if hume_data.get("error"):

        trends=trends,            raise HTTPException(status_code=500, detail=f"Hume AI error: {hume_data['error']}")

        summary=summary,        

        total_comments=len(comments),        return {

        analysis_timestamp=datetime.now().isoformat()            "success": True,

    )            "total_comments": len(request.comments),

            "successful_responses": hume_data.get("successful_responses", 0),

@app.post("/analyze", response_model=AnalysisResponse)            "hume_responses": hume_data.get("hume_responses", []),

async def analyze_comments(request: AnalysisRequest):            "video_title": request.video_title,

    """Main analysis endpoint"""            "timestamp": datetime.now().isoformat(),

    try:            "note": "100% raw Hume AI response data"

        if not request.comments:        }

            raise HTTPException(status_code=400, detail="No comments provided")        

            except Exception as e:

        print(f"🎯 Analyzing {len(request.comments)} comments")        print(f"❌ Raw analysis error: {str(e)}")

                raise HTTPException(status_code=500, detail=f"Raw analysis failed: {str(e)}")

        # Analyze with Hume AI (or fallback to rule-based)

        analysis_data = await analyze_with_hume_batch(request.comments)@app.post("/analyze", response_model=AnalysisResponse)

        async def analyze_comments(request: AnalysisRequest):

        # Create structured response    """Main analysis endpoint with structured response"""

        response = create_analysis_response(analysis_data, request.comments)    try:

                if not request.comments:

        return response            raise HTTPException(status_code=400, detail="No comments provided")

                

    except Exception as e:        print(f"🎯 Starting structured analysis for {len(request.comments)} comments")

        print(f"❌ Analysis error: {str(e)}")        

        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")        # Get Hume AI analysis

        hume_data = await analyze_emotions_with_hume(request.comments)

@app.get("/health")        

async def health_check():        if hume_data.get("api_status") != "success":

    return {            raise HTTPException(status_code=500, detail=f"Hume AI failed: {hume_data.get('error', 'Unknown error')}")

        "status": "healthy",        

        "timestamp": datetime.now().isoformat(),        # Create structured analysis response

        "api_version": "3.0.0",        analysis_response = create_analysis_from_hume(hume_data, request.comments)

        "ai_provider": "Hume AI REST API + Rule-based fallback",        

        "hume_key_present": bool(HUME_API_KEY)        return analysis_response

    }        

    except Exception as e:

@app.get("/")        print(f"❌ Analysis error: {str(e)}")

async def root():        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    return {

        "message": "YouTube Comment Analysis API",@app.get("/debug/emotions")

        "version": "3.0.0",async def debug_emotions():

        "endpoints": {    """Debug endpoint showing system capabilities"""

            "POST /analyze": "Analyze comments with sentiment and emotion detection",    return {

            "GET /health": "Health check"        "hume_ai_status": "connected" if HUME_API_KEY else "missing_key",

        }        "system_version": "2.0.0 - Production Ready",

    }        "capabilities": [

            "Real-time Hume AI emotion analysis",

if __name__ == "__main__":            "53+ emotion types detection",

    import uvicorn            "Dynamic comment limit (25-150 based on popularity)",

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)            "Sentiment analysis with weighted scoring",

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