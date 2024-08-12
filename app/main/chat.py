import requests

from main import settings


def create_session():

    api_endpoint = f"{settings.CHATWEB_API_URL}/create-session"

    response = requests.get(api_endpoint)

    response.raise_for_status()

    session_id = response.json()

    return session_id


def index(url):

    api_endpoint = f"{settings.CHATWEB_API_URL}/index"

    data = {'url': url}

    response = requests.post(api_endpoint, data=data)

    response.raise_for_status()


def ask(url, query, session_id=None):

    api_endpoint = f"{settings.CHATWEB_API_URL}/ask"

    data = {'url': url, 'query': query, 'session_id': session_id}

    response = requests.post(api_endpoint, data=data)

    response.raise_for_status()

    answer = response.json()

    return answer
