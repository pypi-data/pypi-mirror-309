import requests


def wiki_page_exists(server_url, auth, title, space_key):
    """
    Check if a Confluence wiki page already exists based on its title and space key.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param title: Title of the Confluence wiki page.
    :param space_key: Key of the Confluence space.
    :return: True if the page exists, False otherwise.
    """

    print(f"Checking if wiki page '{title}' exists in space '{space_key}'...")

    jql_query = f'space="{space_key}" AND title="{title}"'
    endpoint_url = f"{server_url}/rest/api/content/search?cql={jql_query}"

    response = requests.get(
        endpoint_url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    if response.status_code == 200:
        results = response.json()["results"]
        return len(results) > 0
    else:
        print(f"Failed to check page existence. Status code: {response.status_code}, Response: {response.text}")
        return False
