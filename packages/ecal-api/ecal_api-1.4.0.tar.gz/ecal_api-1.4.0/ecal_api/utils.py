import hashlib, json
from urllib.parse import quote, unquote


def m5_signature(api_key, api_secret, params):
    """
    Calculates the MD5 signature for the given parameters.

    Args:
        api_key (str): The API key provided by ECAL.
        api_secret (str): The secret key for signing requests.
        params (dict): The parameters to be signed.

    Returns:
        str: The MD5 signature.
    """
    if params is None:
        params = {}
    if 'apiKey' not in params:
        params['apiKey'] = str(api_key)

        params.keys()

    concatenated_string = ''.join([f"{key}{value}" for key, value in sorted(params.items()) if key!="json_data"])
    
    final_string = f"{api_secret}{concatenated_string}"

    if 'json_data' in params:
        final_string += params['json_data']

    md5_hash = hashlib.md5(final_string.encode('utf-8')).hexdigest()
    return md5_hash

def status_code(code):
    if code == 200:
        return {"status": "Request successful", "result":True}
    elif code == 204:
        return {"status": "No content", "result":False}
    elif code == 400:
        return {"status": "Invalid input sent in either request body or params", "result":False}
    elif code == 403:
        return {"status": "API signature does not match; or API key status is inactive/expired/non-existent; or Delete private calendar is forbidden", "result":False}
    elif code == 404:
        return {"status": "Calendar/Event not found for given id or reference", "result":False}
    elif code == 409:
        return {"status": "Calendar/Event already exists", "result":False}
    elif code == 429:
        return {"status": "Too many requests! Try again after sometime", "result":False}
    else:
        return {"status": "Server or Gateway error. Please try again later", "result":False}

    