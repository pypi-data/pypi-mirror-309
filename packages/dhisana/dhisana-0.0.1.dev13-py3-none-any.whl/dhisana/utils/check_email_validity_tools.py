# Check validity of email

import os
import os
import aiohttp
from dhisana.utils.assistant_tool_tag import assistant_tool    

@assistant_tool
async def check_email_validity_with_zero_bounce(email_id: str):
    """
    Validate a single email address using the ZeroBounce API.

    This function sends an asynchronous GET request to the ZeroBounce API to validate the provided email address.
    
    Parameters:
    email_id (str): The email address to be validated.

    Returns:
    dict: The JSON response from the ZeroBounce API containing the validation results.

    Raises:
    ValueError: If the ZeroBounce API key is not found in the environment variables.
    Exception: If the response status code from the ZeroBounce API is not 200.
    """
    ZERO_BOUNCE_API_KEY = os.environ.get('ZERO_BOUNCE_API_KEY')
    if not ZERO_BOUNCE_API_KEY:
        raise ValueError("ZeroBounce API key not found in environment variables")

    url = f"https://api.zerobounce.net/v2/validate?api_key={ZERO_BOUNCE_API_KEY}&email={email_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            result = await response.json()
            return result