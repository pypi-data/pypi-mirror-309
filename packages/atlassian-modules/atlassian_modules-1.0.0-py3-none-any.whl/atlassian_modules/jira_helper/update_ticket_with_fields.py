import requests


def update_ticket_with_fields(server_url, auth, ticket_id, additional_fields):
    """
    Update a JIRA ticket with additional fields.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param ticket_id: ID (key) of the ticket to be updated.
    :param additional_fields: Dictionary of fields to update the ticket with.
    :return: True if the update was successful, False otherwise.
    """
    print(f"Updating ticket {ticket_id} with additional fields...")

    # Preparing the update data
    update_data = {
        "fields": additional_fields
    }

    # Making a request to update the ticket
    print(f"Sending request to update ticket {ticket_id}...")
    response = requests.put(
        f"{server_url}/rest/api/2/issue/{ticket_id}",
        json=update_data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    # Checking response
    if response.status_code in [200, 204]:  # HTTP 200 OK or 204 No Content indicate success
        print("Ticket updated successfully!")
        return True
    else:
        print(f"Failed to update ticket. HTTP Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return False
