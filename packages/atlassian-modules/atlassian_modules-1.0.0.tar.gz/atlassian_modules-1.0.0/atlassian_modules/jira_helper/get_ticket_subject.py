import requests


def get_ticket_subject(server_url, auth, ticket_id):
    """
    Retrieve the subject line (summary) of a Jira ticket.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param ticket_id: ID of the Jira ticket.
    :return: Subject line of the ticket or None if the request fails.
    """
    endpoint_url = f"{server_url}/rest/api/2/issue/{ticket_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.get(endpoint_url, headers=headers, auth=auth)

    if response.status_code == 200:
        ticket_data = response.json()
        return ticket_data.get("fields", {}).get("summary", None)
    else:
        print(f"Failed to fetch ticket subject. Status code: {response.status_code}, Response: {response.text}")
        return None
