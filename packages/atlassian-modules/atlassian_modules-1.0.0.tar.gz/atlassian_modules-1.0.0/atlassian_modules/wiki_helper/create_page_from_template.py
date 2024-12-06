import requests


def create_page_from_template(server_url, auth, template_id, space_key, title, parent_page_id=None):
    """
    Create a Confluence wiki page using a specified template.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param template_id: ID of the Confluence template to use.
    :param space_key: Key of the Confluence space where the new page will reside.
    :param title: Title of the new page.
    :param parent_page_id: Optional parent page ID if the new page is to be a child.
    :return: Created Confluence page object for the new page or None if failed.
    """

    print(f"Initiating creation of page '{title}' in space '{space_key}' using template ID '{template_id}'...")

    # Check if a page with the same title already exists
    duplicate_check_response = requests.get(
        f"{server_url}/rest/api/content?spaceKey={space_key}&title={title}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    if duplicate_check_response.status_code == 200:
        if duplicate_check_response.json()["size"] > 0:
            print(f"A page with the title '{title}' already exists in space '{space_key}'.")
            return None

    # Retrieve content from the template
    response = requests.get(
        f"{server_url}/rest/api/template/{template_id}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    if response.status_code != 200:
        print(f"Failed to retrieve content from template. Status code: {response.status_code}, Response: {response.text}")
        return None

    print(f"Successfully retrieved content from template with ID '{template_id}'.")

    template_content = response.json()["body"]["storage"]["value"]

    # Create the new page using the content from the template
    print(f"Creating the new page '{title}' using the retrieved template content...")

    payload = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": template_content,
                "representation": "storage"
            }
        }
    }

    if parent_page_id:
        payload["ancestors"] = [{"id": parent_page_id}]

    response = requests.post(
        f"{server_url}/rest/api/content",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        json=payload
    )

    if response.status_code == 200 or response.status_code == 201:
        page_url = f"{server_url}/pages/viewpage.action?pageId={response.json()['id']}"
        print(f"Page created successfully. URL: {page_url}")
        return response.json()
    else:
        print(f"Failed to create page. Status code: {response.status_code}, Response: {response.text}")
        return None