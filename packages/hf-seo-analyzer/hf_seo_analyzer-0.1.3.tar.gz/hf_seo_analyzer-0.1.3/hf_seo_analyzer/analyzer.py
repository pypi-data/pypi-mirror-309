import requests
import time

def analyze_markdown(content, api_key="", api_url="", retries=3, backoff_factor=2):
    """
    Sends Markdown content to the Huggingface API for analysis.

    :param content: Markdown content as a string.
    :param api_key: API key for authentication (optional).
    :param api_url: API URL for the analysis API.
    :param retries: Number of retry attempts if the request fails.
    :param backoff_factor: Multiplier for exponential backoff between retries.
    :return: Parsed JSON response from the API.
    """
    if not api_url:
        raise ValueError("API URL is required for analysis.")

    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["api-key"] = api_key

    payload = {"content": content}

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                wait_time = backoff_factor ** attempt
                print(f"Request failed (attempt {attempt}/{retries}). Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise RuntimeError(
                    f"API Request failed after {retries} attempts: {e}"
                )
