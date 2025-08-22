"""
Simple test to verify sentiment analysis is working
"""
import sys
import os

# Test sentiment analysis directly 
def test_sentiment():
    try:
        print("Testing sentiment analysis...")
        
        # Import the app
        sys.path.append('.')
        from app import create_app
        
        app = create_app('development')
        
        with app.test_client() as client:
            # Test sentiment page without parameters
            print("1. Testing sentiment page without symbol...")
            response = client.get('/analysis/sentiment')
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Sentiment page loads successfully")
            else:
                print(f"   ❌ Failed with status: {response.status_code}")
                
            # Test sentiment page with symbol
            print("2. Testing sentiment page with EQNR.OL...")
            response = client.get('/analysis/sentiment?symbol=EQNR.OL')
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Sentiment page with symbol loads successfully")
                
                # Check content
                content = response.data.decode('utf-8')
                if 'Markedsstemning' in content:
                    print("   ✅ Page contains expected content")
                if 'EQNR.OL' in content:
                    print("   ✅ Page shows symbol data")
                    
            else:
                print(f"   ❌ Failed with status: {response.status_code}")
                
            # Test with AFG.OL (the one user mentioned)
            print("3. Testing sentiment page with AFG.OL...")
            response = client.get('/analysis/sentiment?symbol=AFG.OL')
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ AFG.OL sentiment loads successfully")
            else:
                print(f"   ❌ AFG.OL failed with status: {response.status_code}")
                
        print("\n✅ All sentiment tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error running sentiment test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_sentiment()
