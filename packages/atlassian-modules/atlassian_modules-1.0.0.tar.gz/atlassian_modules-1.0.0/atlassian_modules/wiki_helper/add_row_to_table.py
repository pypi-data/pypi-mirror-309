from bs4 import BeautifulSoup
from .get_page_content import get_page_content
from .update_page_content import update_page_content


def add_row_to_table(server_url, auth, page_id, headers, row_data):
    """
    Adds a row to the first table in a Confluence page based on the specified headers.

    :param server_url: The base URL of the Confluence server.
    :param auth: Tuple containing email and API token for authentication.
    :param page_id: The ID of the Confluence page.
    :param headers: A list of headers representing the table columns.
    :param row_data: A list of values corresponding to each header to form the new row.
    :return: A message indicating whether the operation was successful.
    """

    # Fetch the current content of the page
    page_content = get_page_content(server_url, auth, page_id)
    if page_content is None:
        return "Failed to fetch page content."

    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find('table')
    if not table:
        return "No table found on the page."

    # Check if the first row (headers row) matches the passed headers
    table_headers = [th.get_text(strip=True) for th in table.find_all('th')]
    if not all(header in table_headers for header in headers) or not len(headers) == len(table_headers):
        return "Headers do not match the table headers."

    # Check if the row_data length matches the headers length
    if len(headers) != len(row_data):
        return "Row data length does not match headers length."

    # Create a new row
    new_row = soup.new_tag('tr')
    for header in headers:
        new_cell = soup.new_tag('td')
        new_cell.string = row_data[headers.index(header)]
        new_row.append(new_cell)

    table.append(new_row)

    # Update the page with the new content
    update_result = update_page_content(server_url, auth, page_id, str(soup))
    if update_result:
        return "Row added successfully."
    else:
        return "Failed to update the page."