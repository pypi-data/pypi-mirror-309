import requests
from .get_page_content import get_page_content


def update_page_content(server_url, auth, page_id, new_content):
    """
    Update the content of a Confluence page.

    :param server_url: The base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: The ID of the Confluence page to be updated.
    :param new_content: The new content in storage format.
    :return: True if the update was successful, False otherwise.
    """
    # Fetch current page version
    current_content = get_page_content(server_url, auth, page_id)
    if current_content is None:
        return False

    version_endpoint = f"{server_url}/rest/api/content/{page_id}"
    version_response = requests.get(version_endpoint,
                                    headers={"Accept": "application/json", "Content-Type": "application/json"},
                                    auth=auth)
    if version_response.status_code != 200:
        print("Failed to fetch current page version.")
        return False

    current_version = version_response.json()['version']['number']

    # Prepare the update payload
    update_payload = {
        "version": {
            "number": current_version + 1
        },
        "title": version_response.json()['title'],
        "type": "page",
        "body": {
            "storage": {
                "value": new_content,
                "representation": "storage"
            }
        }
    }

    update_response = requests.put(version_endpoint,
                                   headers={"Accept": "application/json", "Content-Type": "application/json"},
                                   auth=auth, json=update_payload)

    if update_response.status_code == 200:
        print("Page updated successfully.")
        return True
    else:
        print(f"Failed to update page. Status code: {update_response.status_code}, Response: {update_response.text}")
        return False
