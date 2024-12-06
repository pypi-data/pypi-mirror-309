import requests


def replace_in_page(server_url, auth, page_id, from_string, to_string):
    """
    Replace all occurrences of a string in a Confluence wiki page.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: ID of the Confluence wiki page.
    :param from_string: String to be replaced.
    :param to_string: String to replace with.
    :return: True if replacement was successful, False otherwise.
    """

    print(f"Fetching content of page ID: {page_id}...")

    endpoint_url = f"{server_url}/rest/api/content/{page_id}"
    params = {"expand": "version,body.storage"}

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
        print(f"Failed to fetch page content. Status code: {response.status_code}, Response: {response.text}")
        return False

    page_data = response.json()
    content = page_data["body"]["storage"]["value"]

    print("Performing replacements...")
    updated_content = content.replace(from_string, to_string)

    if updated_content == content:
        print("No replacements made.")
        return True

    new_version = page_data["version"]["number"] + 1
    update_payload = {
        "version": {
            "number": new_version
        },
        "title": page_data["title"],
        "type": "page",
        "body": {
            "storage": {
                "value": updated_content,
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