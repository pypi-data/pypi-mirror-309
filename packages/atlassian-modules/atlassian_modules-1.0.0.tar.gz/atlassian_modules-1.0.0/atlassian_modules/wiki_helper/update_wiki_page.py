import requests


def update_wiki_page(server_url, auth, page_id, new_content):
    """
    Update the content of a Confluence wiki page.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: ID of the Confluence wiki page to be updated.
    :param new_content: New content to replace the existing content of the page.
    :return: True if the update was successful, False otherwise.
    """

    print(f"Fetching current data of page ID: {page_id}...")

    endpoint_url = f"{server_url}/rest/api/content/{page_id}"
    params = {"expand": "version"}

    response = requests.get(
        endpoint_url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        params=params
    )

    if response.status_code != 200:
        print(f"Failed to fetch page data. Status code: {response.status_code}, Response: {response.text}")
        return False

    page_data = response.json()
    new_version = page_data["version"]["number"] + 1
    update_payload = {
        "version": {
            "number": new_version
        },
        "title": page_data["title"],
        "type": "page",
        "body": {
            "storage": {
                "value": new_content,
                "representation": "storage"
            }
        }
    }

    print("Updating page with new content...")
    response = requests.put(
        endpoint_url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        json=update_payload
    )

    if response.status_code == 200:
        print("Page updated successfully.")
        return True
    else:
        print(f"Failed to update page. Status code: {response.status_code}, Response: {response.text}")
        return False