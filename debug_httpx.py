#!/usr/bin/env python3
import httpx
import sys
import asyncio

async def test_httpx():
    url = "https://elvwrlwvgolsbtfguppm.supabase.co/rest/v1/"
    
    headers = {
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVsdndybHd2Z29sc2J0Zmd1cHBtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1ODc4NzIsImV4cCI6MjA4MTE2Mzg3Mn0.dHsgJoK5REiiV3d6bLqu3mSVWGRpwJSxEiAKA9lNd0o",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVsdndybHd2Z29sc2J0Zmd1cHBtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1ODc4NzIsImV4cCI6MjA4MTE2Mzg3Mn0.dHsgJoK5REiiV3d6bLqu3mSVWGRpwJSxEiAKA9lNd0o"
    }
    
    try:
        print(f"Testing HTTPX connection to: {url}")
        

        # Test with a timeout
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return True
            
    except httpx.ConnectError as e:
        print(f"Httpx ConnectError: {e}")
        return False
    except Exception as e:
        print(f"Other error: {e}")
        return False

if __name__ == "__main__":
    print("Testing httpx connection...")
    result = asyncio.run(test_httpx())
    sys.exit(0 if result else 1)
