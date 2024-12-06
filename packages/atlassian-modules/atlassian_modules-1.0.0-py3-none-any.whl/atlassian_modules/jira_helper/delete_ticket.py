import requests


def delete_ticket(server_url, auth, ticket_key):
    """
    Delete a JIRA ticket with the provided key.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param ticket_key: Key of the ticket to be deleted.
    :return: True if the deletion was successful, False otherwise.
    """
    response = requests.delete(
        f"{server_url}/rest/api/2/issue/{ticket_key}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    return response.status_code == 204  # HTTP 204 No Content indicates success.
