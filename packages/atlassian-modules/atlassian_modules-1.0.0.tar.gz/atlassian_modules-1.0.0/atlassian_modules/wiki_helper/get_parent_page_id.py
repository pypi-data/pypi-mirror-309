import requests


def get_parent_page_id(server_url, auth, page_id):
    """
    Retrieve the parent ID of a Confluence wiki page.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: ID of the Confluence wiki page.
    :return: ID of the parent page if it exists, otherwise None.
    """

    print(f"Fetching parent page ID for page ID: {page_id}...")

    endpoint_url = f"{server_url}/rest/api/content/{page_id}?expand=ancestors"

    response = requests.get(
        endpoint_url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    if response.status_code == 200:
        page_data = response.json()
        ancestors = page_data.get("ancestors", [])

        if ancestors:
            return ancestors[-1]["id"]
        else:
            print("No parent page found.")
            return None
    else:
        print(f"Failed to fetch parent page ID. Status code: {response.status_code}, Response: {response.text}")
        return None