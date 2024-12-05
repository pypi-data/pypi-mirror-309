import requests

# Base URL for the API
BASE_URL = "https://api.opmentis.xyz/api/v1"
FOODBOT_URL = "https://labfoodbot.opmentis.xyz/api/v1"


def get_active_lab():
    """
    Fetch the active lab details from the central API endpoint.
    Returns the active lab information including the requirements.
    """
    endpoint = f"{BASE_URL}/labs/labs/active"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        
        lab_info = response.json()
        print("Active Lab Information:", lab_info)
        return lab_info
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch active lab details. Error: {e}")
        return {"error": "Failed to fetch active lab details."}


def authenticate(wallet_address: str):
    """
    Authenticate or register a user based on the wallet address.
    Returns an authentication token if the user is authenticated or registered.
    """
    endpoint = f"{BASE_URL}/authenticate"
    params = {"wallet_address": wallet_address}

    try:
        response = requests.post(endpoint, params=params)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        
        data = response.json()
        token = data.get("access_token")
        
        if token:
            print("User authenticated successfully. Token:", token)
            return token
        else:
            print("Authentication failed or user not registered.")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to authenticate user. Error: {e}")
        return None

def register_user(wallet_address: str, labid: str, role_type: str):
    """
    Register a user as a miner or validator based on the role type.
    Requires an authenticated wallet address and a valid lab ID.
    If registration is successful, add a stake for the user based on the role type.
    """
    register_endpoint = f"{BASE_URL}/labs/labs/{labid}/{role_type}/register"
    add_stake_endpoint = f"{BASE_URL}/stakes/add"
    
    # Step 1: Authenticate the user to obtain the token
    token = authenticate(wallet_address)
    if not token:
        return {"error": "Authentication failed. Could not obtain access token."}

    # Set headers for authenticated requests
    headers = {"Authorization": f"Bearer {token}"}

    # Payload for the registration request
    register_payload = {"wallet_address": wallet_address}

    try:
        # Step 2: Add a stake based on the role type
        add_stake_payload = {
            "labid": labid,
            "minerstake": 0 if role_type == "miner" else 0,
            "validatorstake": 20 if role_type == "validator" else 0
        }
        stake_response = requests.post(add_stake_endpoint, json=add_stake_payload, headers=headers)
        stake_response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx

        stake_response_data = stake_response.json()
        print("Stake added successfully. Response:", stake_response_data)

        # Step 3: Register the user after stake is successfully added
        response = requests.post(register_endpoint, json=register_payload, headers=headers)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        registration_response = response.json()

        print(f"User registered successfully as {role_type}. Response:", registration_response)

        # Combine both responses and return
        return {
            "registration_response": registration_response,
            "stake_response": stake_response_data
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to register user as {role_type} or add stake. Error: {e}")
        return {"error": f"Failed to register as {role_type} or add stake."}


def userdata(wallet_address: str):
    """
    Fetch user data from the central API endpoint and return as a formatted table.
    Requires an authentication token for secure access.
    """
    endpoint = f"{FOODBOT_URL}/user_data/table"
    payload = {"wallet_address": wallet_address}
    token = authenticate(wallet_address)

    # Ensure auth_token is available
    if not token:
        print("Authentication token is missing. Please authenticate first.")
        return {"error": "Authentication required to fetch user data."}

    try:
        # Send request with authorization headers
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()

        # Parse and print user data table
        user_table = response.json().get("user_table", "")
        # print("User Data Table:", user_table)
        return user_table

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch user data. Error: {e}")
        return {"error": "Failed to fetch user data."}


def endchat():
    """
    End chat session by sending a request to the central API endpoint.
    """
    endpoint = f"{FOODBOT_URL}/end_chat"

    try:
        response = requests.post(endpoint)
        response.raise_for_status()
        
        end_chat_response = response.json().get("message", "Chat ended and evaluation triggered.")
        print("Chat ended successfully:", end_chat_response)
        return end_chat_response
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to end chat. Error: {e}")
        return {"error": "Failed to end chat."}
