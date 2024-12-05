# Hubspot CRM Tools
import os
import aiohttp
from dhisana.utils.assistant_tool_tag import assistant_tool
from typing import Optional, List, Dict, Any


@assistant_tool
async def fetch_hubspot_object_info(
    object_type: str,
    object_id: Optional[str] = None,
    object_ids: Optional[List[str]] = None,
    associations: Optional[List[str]] = None,
    properties: Optional[List[str]] = None
):
    """
    Fetch information for any HubSpot object(s) (contacts, companies, deals, tickets, lists, etc.) using their ID(s) and type.
    Parameters:
    - **object_type** (*str*): Type of the object (e.g., "contacts", "companies", "deals", "tickets", "lists").
    - **object_id** (*str*, optional): Unique HubSpot object ID for fetching a single object.
    - **object_ids** (*List[str]*, optional): List of unique HubSpot object IDs for multiple.
    - **associations** (*List[str]*, optional): List of associated object types to include in the response.
    - **properties** (*List[str]*, optional): List of properties to include in the response.
    # Example below to get company information of contact.
    await fetch_hubspot_object_info(
        object_type="contacts",
        object_id="12345",  # Replace with the contact's ID
        associations=["companies"]
    )
    """

    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        return {'error': "HubSpot API key not found in environment variables"}

    if not object_id and not object_ids:
        return {'error': "HubSpot object ID(s) must be provided"}

    if not object_type:
        return {'error': "HubSpot object type must be provided"}

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    params = {}
    if properties:
        params['properties'] = ','.join(properties)
    if associations:
        params['associations'] = ','.join(associations)

    try:
        async with aiohttp.ClientSession() as session:
            if object_type.lower() == 'lists':
                # Handle lists endpoint
                if object_id:
                    url = f"https://api.hubapi.com/contacts/v1/lists/{object_id}"
                    async with session.get(url, headers=headers, params=params) as response:
                        result = await response.json()
                        if response.status != 200:
                            return {'error': result}
                        return result
                else:
                    return {'error': "For object_type 'lists', object_id must be provided"}
            else:
                if object_ids:
                    # Batch read
                    url = f"https://api.hubapi.com/crm/v3/objects/{object_type}/batch/read"
                    payload = {
                        "inputs": [{"id": oid} for oid in object_ids]
                    }
                    if properties:
                        payload["properties"] = properties
                    if associations:
                        payload["associations"] = associations
                    async with session.post(url, headers=headers, json=payload) as response:
                        result = await response.json()
                        if response.status != 200:
                            return {'error': result}
                        return result
                else:
                    # Single object read
                    url = f"https://api.hubapi.com/crm/v3/objects/{object_type}/{object_id}"
                    async with session.get(url, headers=headers, params=params) as response:
                        result = await response.json()
                        if response.status != 200:
                            return {'error': result}
                        return result
    except Exception as e:
        return {'error': str(e)}


@assistant_tool
async def search_hubspot_objects(
    object_type: str,
    filters: Optional[List[Dict[str, Any]]] = None,
    filter_groups: Optional[List[Dict[str, Any]]] = None,
    sorts: Optional[List[str]] = None,
    query: Optional[str] = None,
    properties: Optional[List[str]] = None,
    limit: Optional[int] = None,
    after: Optional[str] = None
):
    """
    Search for HubSpot objects (contacts, companies, deals, tickets, etc.) using filters and filter groups.
    Parameters:
    - **object_type** (*str*): Type of the object (e.g., "contacts", "companies", "deals", "tickets").
    - **filters** (*List[Dict[str, Any]]*, optional): List of filters.
    - **filter_groups** (*List[Dict[str, Any]]*, optional): List of filter groups.
    - **sorts** (*List[str]*, optional): List of sort criteria.
    - **query** (*str*, optional): Search query string.
    - **properties** (*List[str]*, optional): List of properties to include in the response.
    - **limit** (*int*, optional): Maximum number of results to return.
    - **after** (*str*, optional): Pagination cursor.
    Returns:
    - **dict**: JSON response from the HubSpot API containing the search results.
    Examples:
    await search_hubspot_objects(
        object_type="contacts",
        filters=[
            {"propertyName": "firstname", "operator": "EQ", "value": "John"},
        ],
        properties=["firstname", "lastname", "email"]
    )
    """

    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        return {'error': "HubSpot API key not found in environment variables"}

    if not object_type:
        return {'error': "HubSpot object type must be provided"}

    if not any([filters, filter_groups, query]):
        return {'error': "At least one of filters, filter_groups, or query must be provided"}

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    url = f"https://api.hubapi.com/crm/v3/objects/{object_type}/search"

    payload: Dict[str, Any] = {}
    if filters:
        payload["filterGroups"] = [{"filters": filters}]
    if filter_groups:
        payload["filterGroups"] = filter_groups
    if sorts:
        payload["sorts"] = sorts
    if query:
        payload["query"] = query
    if properties:
        payload["properties"] = properties
    if limit:
        payload["limit"] = limit
    if after:
        payload["after"] = after

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result}
                return result
    except Exception as e:
        return {'error': str(e)}


@assistant_tool
async def fetch_hubspot_lead_info(first_name: str = None, last_name: str = None, email: str = None, linkedin_url: str = None, phone_number: str = None, hubspot_id: str = None):
    """
    Fetch lead information from HubSpot based on provided parameters.

    This function sends an asynchronous GET request to the HubSpot Contacts API to retrieve the lead's information based on the available non-empty parameters.
    
    Parameters:
    first_name (str): Lead's first name.
    last_name (str): Lead's last name.
    email (str): Lead's email address.
    linkedin_url (str): Lead's LinkedIn URL.
    phone_number (str): Lead's phone number.
    hubspot_id (str): Lead's HubSpot contact ID.

    Returns:
    dict: JSON response from the HubSpot API containing lead information.

    Raises:
    ValueError: If the HubSpot API key is not found in the environment variables or if no search parameter is provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    # Construct the search parameters based on non-empty inputs
    search_params = {}
    if first_name:
        search_params["properties.firstname"] = first_name
    if last_name:
        search_params["properties.lastname"] = last_name
    if email:
        search_params["properties.email"] = email
    if linkedin_url:
        search_params["properties.linkedinurl"] = linkedin_url
    if phone_number:
        search_params["properties.phone"] = phone_number
    if hubspot_id:
        search_params["id"] = hubspot_id
    
    if not search_params:
        raise ValueError("At least one search parameter must be provided")
    
    url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Building filters for search based on the available parameters
    filters = [{"propertyName": key, "operator": "EQ", "value": value} for key, value in search_params.items()]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json={"filters": filters}) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            search_result = await response.json()
            if not search_result.get('results'):
                raise Exception("No lead found with the provided parameters")
            lead_info = search_result['results'][0]

        # Fetch additional properties
        lead_id = lead_info['id']
        additional_properties = {}

        # Fetch company information
        company_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{lead_id}/associations/companies"
        async with session.get(company_url, headers=headers) as response:
            if response.status == 200:
                additional_properties['companies'] = await response.json()

        # Fetch notes
        notes_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{lead_id}/associations/notes"
        async with session.get(notes_url, headers=headers) as response:
            if response.status == 200:
                additional_properties['notes'] = await response.json()

        # Fetch recent activity
        activity_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{lead_id}/associations/activities"
        async with session.get(activity_url, headers=headers) as response:
            if response.status == 200:
                additional_properties['activities'] = await response.json()

        # Merge additional properties into lead_info
        lead_info.update(additional_properties)

        return lead_info

@assistant_tool
async def fetch_hubspot_contact_info(hubspot_id: str = None, email: str = None):
    """
    Fetch contact information from HubSpot including associated companies, notes, activities, tasks, calls, meetings, and email engagement data.

    Parameters:
    - hubspot_id (str): Unique HubSpot contact ID.
    - email (str): Contact's email address.

    Returns:
    - dict: JSON response containing contact information and associated data.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not hubspot_id and not email:
        raise ValueError("Either HubSpot contact ID or email must be provided")

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        if hubspot_id:
            # Lookup by HubSpot ID
            url = f"https://api.hubapi.com/crm/v3/objects/contacts/{hubspot_id}"
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                contact_info = await response.json()
        else:
            # Lookup by email using search endpoint
            url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
            payload = {
                "filterGroups": [
                    {
                        "filters": [
                            {
                                "propertyName": "email",
                                "operator": "EQ",
                                "value": email
                            }
                        ]
                    }
                ],
                "properties": ["email", "firstname", "lastname"]  # Add other properties as needed
            }
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                search_result = await response.json()
                if not search_result.get('results'):
                    raise Exception("No contact found with the provided email")
                contact_info = search_result['results'][0]

        contact_id = contact_info['id']
        additional_properties = {}

        # Fetch associated companies
        company_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/companies"
        async with session.get(company_url, headers=headers) as response:
            if response.status == 200:
                companies_data = await response.json()
                company_ids = [item['id'] for item in companies_data.get('results', [])]
                
                # Fetch company details for each company ID
                companies = []
                for company_id in company_ids:
                    company_detail_url = f"https://api.hubapi.com/crm/v3/objects/companies/{company_id}"
                    async with session.get(company_detail_url, headers=headers) as company_response:
                        if company_response.status == 200:
                            company_info = await company_response.json()
                            companies.append(company_info)
                additional_properties['companies'] = companies

        # Fetch notes
        notes_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/notes"
        async with session.get(notes_url, headers=headers) as response:
            if response.status == 200:
                notes_data = await response.json()
                additional_properties['notes'] = notes_data

        # Fetch activities (engagements)
        activities_url = f"https://api.hubapi.com/engagements/v1/engagements/associated/CONTACT/{contact_id}/paged"
        async with session.get(activities_url, headers=headers) as response:
            if response.status == 200:
                activities_data = await response.json()
                additional_properties['activities'] = activities_data

        # Fetch tasks
        tasks_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/tasks"
        async with session.get(tasks_url, headers=headers) as response:
            if response.status == 200:
                tasks_data = await response.json()
                additional_properties['tasks'] = tasks_data

        # Fetch calls
        calls_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/calls"
        async with session.get(calls_url, headers=headers) as response:
            if response.status == 200:
                calls_data = await response.json()
                additional_properties['calls'] = calls_data

        # Fetch meetings
        meetings_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/meetings"
        async with session.get(meetings_url, headers=headers) as response:
            if response.status == 200:
                meetings_data = await response.json()
                additional_properties['meetings'] = meetings_data

        # Fetch email engagement data
        email_events_url = f"https://api.hubapi.com/email/public/v1/events"
        params = {
            "recipient": contact_info['properties']['email'],
            "eventType": "OPEN"  # You can add multiple types like OPEN, CLICK
        }
        async with session.get(email_events_url, headers=headers, params=params) as response:
            if response.status == 200:
                email_events_data = await response.json()
                additional_properties['email_events'] = email_events_data

        # Merge additional properties into contact_info
        contact_info.update(additional_properties)

        return contact_info

@assistant_tool
async def fetch_companies_in_crm(num: int = 250, list_name: str = None):
    """
    Fetch companies in HubSpot CRM, handling pagination and returning the company entries as a list of dictionaries.
    If a list name is provided, fetch companies from that list; otherwise, fetch all companies.

    Parameters:
    - num (int, optional): Number of companies to fetch. Defaults to 250.
    - list_name (str, optional): Name of the list in HubSpot to fetch companies from. If not provided, fetch all companies.

    Returns:
    - list: List of dictionaries containing company information.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    companies = []
    after = None

    async with aiohttp.ClientSession() as session:
        if list_name:
            # Lookup list ID by list name
            list_info = await fetch_hubspot_list_by_name(list_name, 'companies')
            if list_info:
                list_id = list_info.get('list', {}).get('listId')
            else:
                raise Exception(f"List '{list_name}' not found.")
            if not list_id:
                return []
            # Fetch company record IDs from the list memberships
            while len(companies) < num:
                url = f"https://api.hubapi.com/crm/v3/lists/{list_id}/memberships"
                params = {
                    "limit": min(num - len(companies), 100),  # HubSpot API limit per request
                }
                if after:
                    params["after"] = after
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status != 200:
                        error_details = await response.text()
                        raise Exception(f"Error: Received status code {response.status} with details: {error_details}")
                    result = await response.json()
                    memberships = result.get('results', [])
                    record_ids = [member['recordId'] for member in memberships]

                    if record_ids:
                        # Fetch company details for these record IDs using batch read
                        company_url = "https://api.hubapi.com/crm/v3/objects/companies/batch/read"
                        batch_data = {
                            "properties": ["name", "domain", "annualrevenue", "numberofemployees", "description", "linkedin_company_page", "city", "state", "zip"],
                            "inputs": [{"id": rid} for rid in record_ids]
                        }
                        async with session.post(company_url, headers=headers, json=batch_data) as company_response:
                            if company_response.status != 200:
                                error_details = await company_response.text()
                                raise Exception(f"Error fetching company details: {company_response.status} with details: {error_details}")
                            company_result = await company_response.json()
                            companies.extend(company_result.get('results', []))

                    after = result.get('paging', {}).get('next', {}).get('after')
                    if not after:
                        break
        else:
            # Fetch all companies
            while len(companies) < num:
                url = "https://api.hubapi.com/crm/v3/objects/companies"
                params = {
                    "limit": min(num - len(companies), 100),  # HubSpot API limit per request
                    "properties": ["name", "domain", "annualrevenue", "numberofemployees", "description", "linkedin_company_page", "city", "state", "zip"],
                }
                if after:
                    params["after"] = after
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status != 200:
                        error_details = await response.text()
                        raise Exception(f"Error: Received status code {response.status} with details: {error_details}")
                    result = await response.json()
                    companies.extend(result.get('results', []))
                    after = result.get('paging', {}).get('next', {}).get('after')
                    if not after:
                        break

    return companies[:num]


@assistant_tool
async def fetch_last_n_activities(email: str, num_events: int):
    """
    Fetch the last n activities logged on a HubSpot contact including email, call, and LinkedIn message logs.

    Parameters:
    - email (str): Contact's email address.
    - num_events (int): Number of recent activities to fetch.

    Returns:
    - dict: JSON response containing the last n activities.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")

    if not email:
        raise ValueError("Email must be provided")

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        # Lookup by email using search endpoint
        url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
        payload = {
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": "email",
                            "operator": "EQ",
                            "value": email
                        }
                    ]
                }
            ],
            "properties": ["email", "firstname", "lastname"]  # Add other properties as needed
        }
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            search_result = await response.json()
            if not search_result.get('results'):
                raise Exception("No contact found with the provided email")
            contact_info = search_result['results'][0]

        contact_id = contact_info['id']

        # Fetch activities (engagements)
        activities_url = f"https://api.hubapi.com/engagements/v1/engagements/associated/CONTACT/{contact_id}/paged"
        params = {
            "limit": num_events,
            "offset": 0
        }
        async with session.get(activities_url, headers=headers, params=params) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            activities_data = await response.json()

        return activities_data
    
@assistant_tool
async def fetch_hubspot_list_records(list_id: str = None, list_name: str = None, max_entries_to_read: int = 2500) -> List[dict]:
    """
    Fetch records from a specific HubSpot list using the list's ID or name.

    This function sends asynchronous GET requests to the HubSpot Lists API to retrieve contact records associated with a given list, handling pagination as required.

    Parameters:
    - list_id (str, optional): Unique HubSpot list ID.
    - list_name (str, optional): Name of the HubSpot list.
    - max_entries_to_read (int, optional): Maximum number of entries to read. Defaults to 2500.

    Returns:
    - List[dict]: List of contacts from the HubSpot list.

    Raises:
    - ValueError: If the HubSpot API key, list ID, list name, or max_entries_to_read is invalid.
    - Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")

    if not list_id and not list_name:
        raise ValueError("Either HubSpot list ID or list name must be provided")

    if not max_entries_to_read or max_entries_to_read <= 0:
        raise ValueError("max_entries_to_read must be a positive integer")

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        if list_name:
            # Fetch list ID based on list name
            lists_url = "https://api.hubapi.com/contacts/v1/lists"
            async with session.get(lists_url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                lists_data = await response.json()
                lists = lists_data.get('lists', [])
                matching_list = next((lst for lst in lists if lst.get('name') == list_name), None)
                if not matching_list:
                    raise ValueError(f"No list found with the name {list_name}")
                list_id = matching_list.get('listId')

        # URL to fetch contacts within the specified list
        url = f"https://api.hubapi.com/contacts/v1/lists/{list_id}/contacts/all"

        contacts = []
        has_more = True
        vid_offset = None

        while len(contacts) < max_entries_to_read and has_more:
            params = {
                'count': min(100, max_entries_to_read - len(contacts))
            }
            if vid_offset:
                params['vidOffset'] = vid_offset

            async with session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                result = await response.json()

                for contact in result.get('contacts', []):
                    email = None
                    identity_profiles = contact.get('identity-profiles', [])
                    for profile in identity_profiles:
                        for identity in profile.get('identities', []):
                            if identity.get('type') == 'EMAIL' and identity.get('is-primary'):
                                email = identity.get('value')
                                break
                        if email:
                            break

                    contact_info = {
                        'id': contact.get('vid'),
                        'first_name': contact.get('properties', {}).get('firstname', {}).get('value'),
                        'last_name': contact.get('properties', {}).get('lastname', {}).get('value'),
                        'email': email,
                        'company': contact.get('properties', {}).get('company', {}).get('value')
                    }
                    contacts.append(contact_info)

                has_more = result.get('has-more', False)
                vid_offset = result.get('vid-offset', None)

    return contacts


@assistant_tool
async def update_hubspot_contact_properties(contact_id: str, properties: dict):
    """
    Update contact properties in HubSpot for a given contact ID.

    This function sends an asynchronous PATCH request to the HubSpot Contacts API to update specified contact properties.
    
    Parameters:
    contact_id (str): Unique HubSpot contact ID.
    properties (dict): Dictionary of properties to update, with property names as keys and new values as values.

    Returns:
    dict: JSON response from the HubSpot API containing the updated contact information.

    Raises:
    ValueError: If the HubSpot API key, contact ID, or properties are not provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not contact_id:
        raise ValueError("HubSpot contact ID must be provided")

    if not properties:
        raise ValueError("Properties dictionary must be provided")

    # URL to update contact properties for the specified contact ID
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Payload with properties to update
    payload = {
        "properties": properties
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=payload) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            result = await response.json()
            return result

@assistant_tool
async def update_hubspot_lead_properties(lead_id: str, properties: dict):
    """
    Update lead properties in HubSpot for a given lead ID.

    This function sends an asynchronous PATCH request to the HubSpot CRM API to update specified lead properties.
    
    Parameters:
    lead_id (str): Unique HubSpot lead ID.
    properties (dict): Dictionary of properties to update, with property names as keys and new values as values.

    Returns:
    dict: JSON response from the HubSpot API containing the updated lead information.

    Raises:
    ValueError: If the HubSpot API key, lead ID, or properties are not provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not lead_id:
        raise ValueError("HubSpot lead ID must be provided")

    if not properties:
        raise ValueError("Properties dictionary must be provided")

    # URL to update lead properties for the specified lead ID
    url = f"https://api.hubapi.com/crm/v3/objects/leads/{lead_id}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Payload with properties to update
    payload = {
        "properties": properties
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=payload) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            result = await response.json()
            return result

@assistant_tool
async def fetch_hubspot_company_info(company_id: str = None, name: str = None, domain: str = None):
    """
    Fetch company information from HubSpot using the company's HubSpot ID, name, or domain.

    This function sends an asynchronous request to the HubSpot Companies API to retrieve detailed company information.
    
    Parameters:
    company_id (str): Unique HubSpot company ID.
    name (str): Name of the company.
    domain (str): Domain of the company.

    Returns:
    dict: JSON response from the HubSpot API containing company information.

    Raises:
    ValueError: If the HubSpot API key is not provided or if none of the parameters are provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not (company_id or name or domain):
        raise ValueError("At least one of company_id, name, or domain must be provided")

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        if company_id:
            # Direct lookup by company ID
            url = f"https://api.hubapi.com/crm/v3/objects/companies/{company_id}"
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                company_info = await response.json()
        else:
            # Search lookup by name or domain
            url = "https://api.hubapi.com/crm/v3/objects/companies/search"
            filters = []
            if name:
                filters.append({"propertyName": "name", "operator": "EQ", "value": name})
            if domain:
                filters.append({"propertyName": "domain", "operator": "EQ", "value": domain})
            
            payload = {
                "filters": filters
            }
            
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                search_result = await response.json()
                if not search_result.get('results'):
                    raise Exception("No company found with the provided parameters")
                company_info = search_result['results'][0]

        # Fetch additional properties
        company_id = company_info['id']
        additional_properties = {}

        # Fetch associated contacts
        contacts_url = f"https://api.hubapi.com/crm/v3/objects/companies/{company_id}/associations/contacts"
        async with session.get(contacts_url, headers=headers) as response:
            if response.status == 200:
                additional_properties['contacts'] = await response.json()

        # Fetch associated deals
        deals_url = f"https://api.hubapi.com/crm/v3/objects/companies/{company_id}/associations/deals"
        async with session.get(deals_url, headers=headers) as response:
            if response.status == 200:
                additional_properties['deals'] = await response.json()

        # Merge additional properties into company_info
        company_info.update(additional_properties)

        return company_info

@assistant_tool
async def update_hubspot_company_info(company_id: str = None, domain: str = None, city: str = None, state: str = None, number_of_employees: int = None, description: str = None, linkedin_company_page: str = None, annual_revenue: float = None, industry: str = None):
    """
    Update company information in HubSpot using the company's HubSpot ID or domain.

    This function sends an asynchronous request to the HubSpot Companies API to update company information.
    
    Parameters:
    company_id (str): Unique HubSpot company ID.
    domain (str): Domain of the company.
    city (str): City of the company.
    state (str): State of the company.
    number_of_employees (int): Number of employees in the company.
    description (str): Description of the company.
    linkedin_company_page (str): LinkedIn company page URL.
    annual_revenue (float): Annual revenue of the company.
    industry (str): Industry of the company.

    Returns:
    dict: JSON response from the HubSpot API containing updated company information.

    Raises:
    ValueError: If the HubSpot API key is not provided or if neither company_id nor domain is provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not (company_id or domain):
        raise ValueError("Either company_id or domain must be provided")

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        if not company_id:
            # Lookup company ID by domain
            url = "https://api.hubapi.com/crm/v3/objects/companies/search"
            payload = {
                "filters": [{"propertyName": "domain", "operator": "EQ", "value": domain}]
            }
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                search_result = await response.json()
                if not search_result.get('results'):
                    raise Exception("No company found with the provided domain")
                company_id = search_result['results'][0]['id']

        # Prepare the update payload
        update_payload = {
            "properties": {}
        }
        if city:
            update_payload["properties"]["city"] = city
        if state:
            update_payload["properties"]["state"] = state
        if number_of_employees:
            update_payload["properties"]["numberofemployees"] = number_of_employees
        if description:
            update_payload["properties"]["description"] = description
        if linkedin_company_page:
            update_payload["properties"]["linkedin_company_page"] = linkedin_company_page
        if annual_revenue:
            update_payload["properties"]["annualrevenue"] = annual_revenue
        # if industry:
        #     update_payload["properties"]["industry"] = industry

        # Update company information
        url = f"https://api.hubapi.com/crm/v3/objects/companies/{company_id}"
        async with session.patch(url, headers=headers, json=update_payload) as response:
            if response.status != 200:
                error_details = await response.text()
                print(error_details)
                raise Exception(f"Error: Received status code {response.status}")
            updated_company_info = await response.json()

        return updated_company_info

@assistant_tool
async def create_hubspot_note_for_customer(customer_id: str = None, email: str = None, note: str = None):
    """
    Create and attach a note to a customer in HubSpot using the customer's HubSpot ID or email.

    This function sends an asynchronous request to the HubSpot Engagements API to create a note and associate it with the customer.
    
    Parameters:
    customer_id (str): Unique HubSpot customer ID.
    email (str): Email of the customer.
    note (str): The note content to be added.

    Returns:
    dict: JSON response from the HubSpot API containing the created note information.

    Raises:
    ValueError: If the HubSpot API key is not provided or if neither customer_id nor email is provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not (customer_id or email):
        raise ValueError("Either customer_id or email must be provided")
    
    if not note:
        raise ValueError("Note content must be provided")

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        if not customer_id:
            # Lookup customer ID by email
            url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
            payload = {
                "filters": [{"propertyName": "email", "operator": "EQ", "value": email}]
            }
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                search_result = await response.json()
                if not search_result.get('results'):
                    raise Exception("No customer found with the provided email")
                customer_id = search_result['results'][0]['id']

        # Prepare the note payload
        note_payload = {
            "engagement": {
                "active": True,
                "type": "NOTE"
            },
            "associations": {
                "contactIds": [customer_id]
            },
            "metadata": {
                "body": note
            }
        }

        # Create the note
        url = "https://api.hubapi.com/engagements/v1/engagements"
        async with session.post(url, headers=headers, json=note_payload) as response:
            if response.status != 200:
                error_details = await response.text()
                print(error_details)
                raise Exception(f"Error: Received status code {response.status}")
            created_note_info = await response.json()

        return created_note_info

@assistant_tool
async def get_last_n_notes_for_customer(customer_id: str = None, email: str = None, n: int = 5):
    """
    Retrieve the last n notes attached to a customer in HubSpot using the customer's HubSpot ID or email.

    This function sends an asynchronous request to the HubSpot Engagements API to retrieve the last n notes associated with the customer.
    
    Parameters:
    customer_id (str): Unique HubSpot customer ID.
    email (str): Email of the customer.
    n (int): Number of notes to retrieve.

    Returns:
    list: List of JSON responses from the HubSpot API containing the notes information.

    Raises:
    ValueError: If the HubSpot API key is not provided or if neither customer_id nor email is provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not (customer_id or email):
        raise ValueError("Either customer_id or email must be provided")

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        if not customer_id:
            # Lookup customer ID by email
            url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
            payload = {
                "filters": [{"propertyName": "email", "operator": "EQ", "value": email}]
            }
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                search_result = await response.json()
                if not search_result.get('results'):
                    raise Exception("No customer found with the provided email")
                customer_id = search_result['results'][0]['id']

        # Retrieve the notes
        url = f"https://api.hubapi.com/engagements/v1/engagements/associated/contact/{customer_id}/paged"
        params = {
            "limit": n,
            "engagementType": "NOTE"
        }
        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            notes_info = await response.json()

        return notes_info.get('results', [])
       
@assistant_tool
async def fetch_hubspot_contact_associations(contact_id: str, to_object_type: str):
    """
    Fetch associations from a contact to other objects in HubSpot.

    This function sends an asynchronous GET request to the HubSpot Associations API to retrieve 
    associated records of a specified type for a contact.
    
    Parameters:
    contact_id (str): Unique HubSpot contact ID.
    to_object_type (str): The object type to retrieve associations for (e.g., 'companies', 'deals', 'tickets').
    
    Returns:
    dict: JSON response from the HubSpot API containing association information.

    Raises:
    ValueError: If the HubSpot API key or contact ID is not provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not contact_id:
        raise ValueError("HubSpot contact ID must be provided")
    
    if not to_object_type:
        raise ValueError("Target object type must be provided")
    
    # URL to fetch associations from the contact to the specified object type
    url = f"https://api.hubapi.com/crm/v4/objects/contacts/{contact_id}/associations/{to_object_type}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            result = await response.json()
            return result



async def fetch_hubspot_list_by_name(list_name: str, list_type: str = 'contacts'):
    """
    Fetch information for a specific HubSpot list using the list's name.

    This function sends an asynchronous GET request to the HubSpot V3 Lists API to retrieve the list
    that matches the specified name and object type.
    
    Parameters:
    list_name (str): Name of the HubSpot list to find.
    list_type (str): Type of the HubSpot list to find ('contacts', 'companies', 'deals', etc.).

    Returns:
    dict: JSON response from the HubSpot API containing the list information if found.

    Raises:
    ValueError: If the HubSpot API key or list name is not provided.
    Exception: If the response status code from the HubSpot API is not 200 or if the list is not found.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not list_name:
        raise ValueError("HubSpot list name must be provided")

    # Map list types to objectTypeIds
    object_type_ids = {
        'contacts': '0-1',
        'companies': '0-2',
        'deals': '0-3',
        'tickets': '0-5',
        # Add other object types if needed
    }
    
    object_type_id = object_type_ids.get(list_type.lower())
    if not object_type_id:
        raise ValueError(f"Invalid list type '{list_type}'. Valid types are: {list(object_type_ids.keys())}")
    
    # URL to fetch the list by name and object type
    url = f"https://api.hubapi.com/crm/v3/lists/object-type-id/{object_type_id}/name/{list_name}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                list_info = await response.json()
                return list_info
            elif response.status == 404:
                raise Exception(f"List with name '{list_name}' not found for object type '{list_type}'")
            else:
                error_details = await response.text()
                raise Exception(f"Error: Received status code {response.status} with details: {error_details}")
