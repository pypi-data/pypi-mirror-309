import os
import aiohttp
from dhisana.utils.assistant_tool_tag import assistant_tool
from typing import List, Optional, Union
import backoff

@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=2,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def enrich_person_info_from_apollo(
    linkedin_url: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
):
    """
    Fetch a person's details from Apollo using LinkedIn URL, email, or phone number.
    
    Parameters:
    - **linkedin_url** (*str*, optional): LinkedIn profile URL of the person.
    - **email** (*str*, optional): Email address of the person.
    - **phone** (*str*, optional): Phone number of the person.

    Returns:
    - **dict**: JSON response containing person information.
    """
    APOLLO_API_KEY = os.environ.get('APOLLO_API_KEY')
    if not APOLLO_API_KEY:
        return {'error': "Apollo API key not found in environment variables"}

    if not linkedin_url and not email and not phone:
        return {'error': "At least one of linkedin_url, email, or phone must be provided"}

    headers = {
        "X-Api-Key": f"{APOLLO_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {}
    if linkedin_url:
        data['linkedin_url'] = linkedin_url
    if email:
        data['email'] = email
    if phone:
        data['phone_numbers'] = [phone]  # Apollo expects a list for phone numbers

    url = 'https://api.apollo.io/v1/people/match'  # Correct API endpoint

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 429:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Rate limit exceeded",
                    headers=response.headers
                )
            else:
                result = await response.json()
                return {'error': result}



@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=2,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def enrich_company_info_from_apollo(
    company_domain: Optional[str] = None,
):
    """
    Fetch a company's details from Apollo using the company domain.
    
    Parameters:
    - **company_domain** (*str*, optional): Domain of the company.

    Returns:
    - **dict**: JSON response containing company information.
    """
    APOLLO_API_KEY = os.environ.get('APOLLO_API_KEY')
    if not APOLLO_API_KEY:
        return {'error': "Apollo API key not found in environment variables"}

    if not company_domain:
        return {'error': "Company domain must be provided"}

    headers = {
        "X-Api-Key": f"{APOLLO_API_KEY}",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "accept": "application/json"
    }

    url = f'https://api.apollo.io/api/v1/organizations/enrich?domain={company_domain}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 429:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Rate limit exceeded",
                    headers=response.headers
                )
            else:
                result = await response.json()
                return {'error': result}