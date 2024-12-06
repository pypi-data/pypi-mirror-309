import requests


def get_child_pages_recursive(server_url, auth, parent_id):
    """
    Recursively retrieve all descendant pages of a given parent page ID.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param parent_id: ID of the parent Confluence wiki page.
    :return: List of child pages with their titles and IDs.
    """

    def fetch_children(page_id):
        endpoint_url = f"{server_url}/rest/api/content/{page_id}/child/page"
        response = requests.get(
            endpoint_url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            auth=auth
        )

        if response.status_code == 200:
            return response.json()["results"]
        else:
            print(f"Failed to fetch children for page ID {page_id}. Status code: {response.status_code}, Response: {response.text}")
            return []

    children = fetch_children(parent_id)
    all_pages = children.copy()

    for child in children:
        all_pages.extend(get_child_pages_recursive(server_url, auth, child["id"]))

    return all_pages