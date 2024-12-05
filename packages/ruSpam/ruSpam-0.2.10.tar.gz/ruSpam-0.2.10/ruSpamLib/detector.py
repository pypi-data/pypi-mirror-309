import requests
from tqdm import tqdm

def is_spam(message, model_name='spamNS_v6', user_token=None): 
    api_url = "https://neurospacex-ruspamlib-serverandsite.hf.space/api/check_spam"
    
    if not user_token:
        print("API token is required for authentication.")
        return False, 0

    headers = {
        "Authorization": user_token
    }

    payload = {"message": message, "model_name": model_name}

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        is_spam_result = result.get('is_spam', 0) == 1
        confidence = result.get('confidence', 0)
        
        return is_spam_result, confidence
    else:
        print("Error with API request:", response.status_code)
        if response.status_code == 400:
            result = response.json()
            if 'error' in result:
                print("Error:", result['error'])
        return False, 0
