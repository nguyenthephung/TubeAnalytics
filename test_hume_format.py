"""
Test script để hiểu format response của Hume AI SDK
"""
import asyncio
import os
from hume import HumeStreamClient
from hume.models.config import LanguageConfig
from dotenv import load_dotenv

load_dotenv()

async def test_hume_format():
    """Test raw Hume AI response format"""
    api_key = os.getenv("HUME_API_KEY", "ghVbZYw5X4Qj2U7YqPW6H5didOaYyn4984uStf7xxGIz3vcV")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"🔑 Using API key: {api_key[:10]}...")
    
    try:
        client = HumeStreamClient(api_key)
        config = LanguageConfig()
        
        # Test với một comment đơn giản
        test_comment = "This video is amazing! I love it so much!"
        
        print(f"📤 Sending test comment: {test_comment}")
        
        async with client.connect([config]) as socket:
            result = await socket.send_text(test_comment)
            
            print("✅ Raw Hume AI Response:")
            print("=" * 50)
            print(f"Type: {type(result)}")
            print(f"Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            print("=" * 50)
            print("Full response:")
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_hume_format())