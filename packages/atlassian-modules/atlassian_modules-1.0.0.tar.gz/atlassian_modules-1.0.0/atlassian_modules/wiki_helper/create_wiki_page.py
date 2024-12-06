import requests


def create_wiki_page(server_url, auth, space_key, title, content, parent_page_id=None):
    """
    Create a Confluence wiki page in the specified space.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param space_key: Key of the Confluence space where the new page will reside.
    :param title: Title of the new page.
    :param content: Content of the new page.
    :param parent_page_id: Optional parent page ID if the new page is to be a child.
    :return: URL of the created Confluence page or None if creation failed.
    """
    page_data = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }

    if parent_page_id:
        page_data["ancestors"] = [{"id": parent_page_id}]

    print(f"Creating Confluence page with title '{title}' in space '{space_key}', please wait...")

    response = requests.post(
        f"{server_url}/rest/api/content",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        json=page_data
    )

    if response.status_code == 200:  # HTTP 200 OK indicates success for Confluence.
        page_url = f"{server_url}/pages/viewpage.action?pageId={response.json()['id']}"
        print(f"Page created successfully. URL: {page_url}")
        return page_url
    else:
        print(f"Failed to create page. Status code: {response.status_code}, Response: {response.text}")
        return None
