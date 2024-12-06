import requests


def get_page_content(server_url, auth, page_id):
    """
    Fetch the storage format content of a Confluence page by ID.

    :param server_url: The base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: The ID of the Confluence page.
    :return: The storage format content of the page if successful, None otherwise.
    """
    endpoint_url = f"{server_url}/rest/api/content/{page_id}?expand=body.storage"
    response = requests.get(endpoint_url, headers={"Accept": "application/json", "Content-Type": "application/json"}, auth=auth)

    if response.status_code == 200:
        return response.json()['body']['storage']['value']
    else:
        print(f"Failed to fetch page content. Status code: {response.status_code}, Response: {response.text}")
        return None