# Hubspot CRM Tools
import json
import os
import aiohttp
from dhisana.utils.assistant_tool_tag import assistant_tool

@assistant_tool
async def search_google(
    query: str,
    number_of_results: int
):
    """
    Search Google using SERP API and return the results as an array of serialized JSON strings.
    Parameters:
    - **query** (*str*): The search query.
    - **number_of_results** (*int*): The number of results to return.
    """
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
    if not SERPAPI_KEY:
        return {'error': "SERP API key not found in environment variables"}

    params = {
        "q": query,
        "num": number_of_results,
        "api_key": SERPAPI_KEY
    }

    url = "https://serpapi.com/search"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result}
                
                # Serialize each result to JSON string
                serialized_results = [json.dumps(item) for item in result.get('organic_results', [])]
                return serialized_results
    except Exception as e:
        return {'error': str(e)}

@assistant_tool
async def search_google_maps(
    query: str,
    number_of_results: int
):
    """
    Search Google Maps using SERP API and return the results as an array of serialized JSON strings.
    Parameters:
    - **query** (*str*): The search query.
    - **number_of_results** (*int*): The number of results to return.
    """
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
    if not SERPAPI_KEY:
        return {'error': "SERP API key not found in environment variables"}

    params = {
        "q": query,
        "num": number_of_results,
        "api_key": SERPAPI_KEY,
        "engine": "google_maps"
    }

    url = "https://serpapi.com/search"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result}
                
                # Serialize each result to JSON string
                serialized_results = [json.dumps(item) for item in result.get('local_results', [])]
                return serialized_results
    except Exception as e:
        return {'error': str(e)}

@assistant_tool
async def search_google_news(
    query: str,
    number_of_results: int
):
    """
    Search Google News using SERP API and return the results as an array of serialized JSON strings.
    Parameters:
    - **query** (*str*): The search query.
    - **number_of_results** (*int*): The number of results to return.
    """
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
    if not SERPAPI_KEY:
        return {'error': "SERP API key not found in environment variables"}

    params = {
        "q": query,
        "num": number_of_results,
        "api_key": SERPAPI_KEY,
        "engine": "google_news"
    }

    url = "https://serpapi.com/search"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result}
                
                # Serialize each result to JSON string
                serialized_results = [json.dumps(item) for item in result.get('news_results', [])]
                return serialized_results
    except Exception as e:
        return {'error': str(e)}
    

@assistant_tool
async def search_job_postings(
    query: str,
    number_of_results: int
):
    """
    Search for job postings using SERP API and return the results as an array of serialized JSON strings.
    Parameters:
    - **query** (*str*): The search query.
    - **number_of_results** (*int*): The number of results to return.
    """
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
    if not SERPAPI_KEY:
        return {'error': "SERP API key not found in environment variables"}

    params = {
        "q": query,
        "num": number_of_results,
        "api_key": SERPAPI_KEY,
        "engine": "google_jobs"
    }

    url = "https://serpapi.com/search"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result}
                
                # Serialize each result to JSON string
                serialized_results = [json.dumps(item) for item in result.get('jobs_results', [])]
                return serialized_results
    except Exception as e:
        return {'error': str(e)}

@assistant_tool
async def search_google_images(
    query: str,
    number_of_results: int
):
    """
    Search Google Images using SERP API and return the results as an array of serialized JSON strings.
    Parameters:
    - **query** (*str*): The search query.
    - **number_of_results** (*int*): The number of results to return.
    """
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
    if not SERPAPI_KEY:
        return {'error': "SERP API key not found in environment variables"}

    params = {
        "q": query,
        "num": number_of_results,
        "api_key": SERPAPI_KEY,
        "engine": "google_images"
    }

    url = "https://serpapi.com/search"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result}
                
                # Serialize each result to JSON string
                serialized_results = [json.dumps(item) for item in result.get('images_results', [])]
                return serialized_results
    except Exception as e:
        return {'error': str(e)}

@assistant_tool
async def search_google_videos(
    query: str,
    number_of_results: int
):
    """
    Search Google Videos using SERP API and return the results as an array of serialized JSON strings.
    Parameters:
    - **query** (*str*): The search query.
    - **number_of_results** (*int*): The number of results to return.
    """
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
    if not SERPAPI_KEY:
        return {'error': "SERP API key not found in environment variables"}

    params = {
        "q": query,
        "num": number_of_results,
        "api_key": SERPAPI_KEY,
        "engine": "google_videos"
    }

    url = "https://serpapi.com/search"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result}
                
                # Serialize each result to JSON string
                serialized_results = [json.dumps(item) for item in result.get('video_results', [])]
                return serialized_results
    except Exception as e:
        return {'error': str(e)}