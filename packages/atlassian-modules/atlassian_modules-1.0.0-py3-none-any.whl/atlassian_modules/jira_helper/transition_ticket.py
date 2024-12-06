import requests
from .get_transitions import get_transitions


def transition_ticket(server_url, auth, ticket_key, transition_input):
    """
    Transition a ticket based on the provided input which can be a transition name or ID.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param ticket_key: Key of the ticket to be transitioned.
    :param transition_input: Desired transition name or ID to perform on the ticket.
    :return: True if the transition was successful, or False otherwise.
    """
    # Check if the transition input is an ID or a name
    print(f"Attempting to transition ticket: {ticket_key}...")
    if str(transition_input).isdigit():
        print("Using provided transition ID.")
        transition_id = transition_input
    else:
        print(f"Fetching transition ID for '{transition_input}'...")
        transition_id = get_transitions(server_url, auth, ticket_key, str(transition_input).lower())
        if not transition_id:
            print(f"Failed to find a transition ID for '{transition_input}'!")
            return False

    # Prepare the payload and make a request to transition the ticket
    payload = {
        "transition": {
            "id": transition_id
        }
    }

    response = requests.post(
        f"{server_url}/rest/api/2/issue/{ticket_key}/transitions",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        json=payload
    )

    # Checking response
    if response.status_code == 204:  # HTTP 204 No Content, indicates success.
        print(f"Successfully transitioned ticket: {ticket_key}")
        return True
    else:
        print(f"Failed to transition ticket. HTTP Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return False
