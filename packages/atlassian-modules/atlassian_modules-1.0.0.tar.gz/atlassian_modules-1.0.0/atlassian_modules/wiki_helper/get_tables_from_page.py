import requests
from bs4 import BeautifulSoup
import json


def get_tables_from_page(server_url, auth, page_id):
    """
    Fetch all tables from a Confluence wiki page based on the provided page ID and convert them into a structured JSON,
    preserving all text, including bullets and list items in table cells.

    :param server_url: Base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: ID of the Confluence wiki page.
    :return: A JSON structure containing all tables from the page.
    """

    print(f"Fetching content of page ID: {page_id}...")

    endpoint_url = f"{server_url}/rest/api/content/{page_id}"
    params = {"expand": "body.storage"}

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
        return None

    page_content = response.json()['body']['storage']['value']
    soup = BeautifulSoup(page_content, 'html.parser')

    tables = soup.find_all('table')

    result = {}
    for idx, table in enumerate(tables, start=1):
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            cells = [cell.get_text(strip=True) for cell in row.find_all('td')]
            row_dict = dict(zip(headers, cells))
            rows.append(row_dict)
        result[f"table{idx}"] = rows

    return json.dumps(result, indent=4)