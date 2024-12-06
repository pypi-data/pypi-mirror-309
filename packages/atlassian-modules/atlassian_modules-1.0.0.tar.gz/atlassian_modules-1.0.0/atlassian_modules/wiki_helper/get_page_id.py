import requests


def get_page_id(server_url, auth, title, space_key):
    """
    Retrieve the ID of a Confluence wiki page by its title.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param title: Title of the Confluence wiki page.
    :param space_key: Key of the Confluence space to search in.
    :return: ID of the page if found, otherwise None.
    """
    print(f"Searching for page with title: {title} in space: {space_key}...")

    endpoint_url = f"{server_url}/rest/api/content"
    params = {
        "title": title,  # search by title
        "spaceKey": space_key,  # search in the specific space
        "limit": 1,  # we are only interested in one page with the exact title
    }

    response = requests.get(
        endpoint_url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        params=params
    )

    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return results[0]["id"]
        else:
            print(f"No page found with title: {title} in space: {space_key}.")
            return None
    else:
        print(f"Failed to search for page. Status code: {response.status_code}, Response: {response.text}")
        return None
