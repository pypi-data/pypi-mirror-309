from bs4 import BeautifulSoup
from .get_page_content import get_page_content
from .update_page_content import update_page_content


def update_or_add_table_row(server_url, auth, page_id, headers, new_row_data):
    """
    Update an existing row in a Confluence table or add it if it doesn't exist.

    :param server_url: The base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: The ID of the Confluence page.
    :param headers: A list of headers representing the table columns.
    :param new_row_data: A list of values corresponding to each header for the new or updated row.
    :return: A message indicating the operation result.
    """
    page_content = get_page_content(server_url, auth, page_id)
    if not page_content:
        return "Failed to fetch page content."

    # Attempt to parse the existing table and find if the row exists
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find('table')
    if not table:
        return "No table found on the page."

    table_headers = [th.get_text(strip=True) for th in table.find_all('th')]
    if not all(header in table_headers for header in headers) or not len(headers) == len(table_headers):
        return "Headers do not match the table headers."

    # Check if the row_data length matches the headers length
    if len(headers) != len(new_row_data):
        return "Row data length does not match headers length."

    # Find the row to update or add a new row
    updated = False
    for row in table.find_all('tr')[1:]:  # Skip header row
        cells = row.find_all('td')
        if len(cells) != len(headers):
            continue
        if all(cells[table_headers.index(header)].get_text(strip=True) == new_row_data[headers.index(header)] for header in headers):
            for header in headers:
                cells[table_headers.index(header)].string = new_row_data[headers.index(header)]
            updated = True
            break

    if not updated:
        new_row = soup.new_tag('tr')
        for header in headers:
            new_cell = soup.new_tag('td')
            new_cell.string = new_row_data[headers.index(header)]
            new_row.append(new_cell)
        table.append(new_row)

    update_result = update_page_content(server_url, auth, page_id, str(soup))
    return "Row updated successfully." if update_result else "Failed to update the page."