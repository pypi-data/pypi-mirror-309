import requests
from .create_wiki_page import create_wiki_page


def duplicate_wiki_page(server_url, auth, source_page_id, target_space_key, target_title, target_parent_page_id=None):
    """
    Duplicate a Confluence wiki page from a source page to a target space with a new title.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param source_page_id: ID of the source Confluence page to be duplicated.
    :param target_space_key: Key of the Confluence space where the duplicated page will reside.
    :param target_title: Title of the duplicated page.
    :param target_parent_page_id: Optional parent page ID if the duplicated page is to be a child.
    :return: URL of the duplicated Confluence page or None if duplication failed.
    """
    print(f"Retrieving content from source page with ID '{source_page_id}'...")

    # 1. Retrieve content from the source page
    response = requests.get(
        f"{server_url}/rest/api/content/{source_page_id}?expand=body.storage",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    if response.status_code != 200:
        print(
            f"Failed to retrieve content from source page. Status code: {response.status_code}, Response: {response.text}")
        return None

    source_content = response.json()["body"]["storage"]["value"]
    print(f"Successfully retrieved content from source page with ID '{source_page_id}'.")

    # 2. Create the new page using the content from the source page
    return create_wiki_page(server_url, auth, target_space_key, target_title, source_content, target_parent_page_id)
