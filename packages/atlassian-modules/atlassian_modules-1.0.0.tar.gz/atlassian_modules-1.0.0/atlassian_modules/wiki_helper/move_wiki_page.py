import requests


def move_wiki_page(server_url, auth, page_id, target_space_key, target_position='append', target_parent_page_id=None):
    """
    Move a Confluence wiki page to a new space and position within another page without changing its title.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: ID of the Confluence page to be moved.
    :param target_space_key: Key of the Confluence space where the moved page will reside.
    :param target_position: Position to place the moved page relative to the parent page
                            (e.g., 'append', 'above', 'below'). Default is 'append'.
    :param target_parent_page_id: Optional ID of the parent page in which the page will be moved under.
    :return: Moved Confluence page object for the page or None if move operation failed.
    """

    print(f"Initiating move of page with ID '{page_id}'...")

    # 1. Retrieve current title of the page
    response = requests.get(
        f"{server_url}/rest/api/content/{page_id}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    if response.status_code != 200:
        print(f"Failed to retrieve page details. Status code: {response.status_code}, Response: {response.text}")
        return None

    current_title = response.json()["title"]
    current_version = response.json()["version"]["number"]

    # 2. Construct the payload for the move operation
    print(f"Preparing to move page '{current_title}' to space '{target_space_key}'.")
    move_payload = {
        "version": {
            "number": current_version + 1
        },
        "space": {
            "key": target_space_key
        },
        "title": current_title
    }

    if target_parent_page_id:
        move_payload["ancestors"] = [{"id": target_parent_page_id}]

    # 3. Make the request to move the page
    print(f"Executing move operation for page '{current_title}'...")
    response = requests.put(
        f"{server_url}/rest/api/content/{page_id}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        json=move_payload
    )

    if response.status_code == 200:
        print(f"Page moved successfully to space '{target_space_key}'.")
        return response.json()
    else:
        print(f"Failed to move page. Status code: {response.status_code}, Response: {response.text}")
        return None