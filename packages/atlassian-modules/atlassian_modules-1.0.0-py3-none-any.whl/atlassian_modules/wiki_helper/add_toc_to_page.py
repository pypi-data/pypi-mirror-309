import requests


def add_toc_to_page(server_url, auth, page_id):
    """
    Add a Table of Contents (TOC) to a Confluence wiki page if it doesn't already have one.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: ID of the Confluence wiki page.
    :return: Message indicating the result of the operation.
    """

    def toc_exists(content):
        return '<ac:structured-macro ac:name="toc"' in content

    print(f"Checking and updating page ID: {page_id} for TOC...")

    # Fetch the current content of the page
    endpoint_url = f"{server_url}/rest/api/content/{page_id}"
    params = {"expand": "body.storage,version"}

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
        return "Failed to fetch page content."

    data = response.json()
    current_content = data['body']['storage']['value']
    version_number = data.get('version', {}).get('number', 0)

    # Add TOC if not exists
    if not toc_exists(current_content):
        new_content = f'<ac:structured-macro ac:name="toc"></ac:structured-macro>{current_content}'
        update_payload = {
            "version": {
                "number": version_number + 1
            },
            "title": data["title"],
            "type": "page",
            "body": {
                "storage": {
                    "value": new_content,
                    "representation": "storage"
                }
            }
        }

        print("Updating page with TOC...")
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
            print("Page updated successfully with TOC.")
            return "Page updated successfully with TOC."
        else:
            print(f"Failed to update page. Status code: {response.status_code}, Response: {response.text}")
            return "Failed to update page."
    else:
        print("TOC already exists on the page.")
        return "TOC already exists on the page."