import requests


def if_ticket_exist(server_url, auth, ticket_key):
    """
    Check if a ticket with the provided key exists.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param ticket_key: Key of the ticket to be checked.
    :return: True if the ticket exists, or False otherwise.
    """
    # Making a request to check if the ticket exists
    print(f"Checking existence of ticket: {ticket_key}...")
    response = requests.get(
        f"{server_url}/rest/api/2/issue/{ticket_key}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    # Evaluating the response
    if response.status_code == 200:  # HTTP 200 OK, indicates the ticket exists.
        print(f"Ticket {ticket_key} exists!")
        return True
    elif response.status_code == 404:  # HTTP 404 Not Found, indicates the ticket does not exist.
        print(f"Ticket {ticket_key} does not exist!")
        return False
    else:
        print(f"Failed to verify ticket existence. HTTP Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return False