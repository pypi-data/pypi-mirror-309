import requests


def get_transitions(server_url, auth, ticket_key, transition_to):
    """
    Retrieve the transition ID for a given ticket based on the desired transition name.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param ticket_key: Key of the ticket for which transitions are being fetched.
    :param transition_to: Desired transition name to look for.
    :return: Transition ID if found, or False if not found or if request failed.
    """
    # Making a request to get transitions
    response = requests.get(
        f"{server_url}/rest/api/2/issue/{ticket_key}/transitions",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    # Checking response
    if response.status_code == 200:  # HTTP 200 OK
        print("Successfully fetched transitions!")
        transitions = response.json().get("transitions", [])
        for transition in transitions:
            if str(transition["name"]).lower() == transition_to.lower():
                print(f"Found transition '{transition_to}' with ID: {transition['id']}")
                return transition["id"]
        print(f"Transition '{transition_to}' not found for ticket: {ticket_key}")
        return False
    else:
        print(f"Failed to fetch transitions. HTTP Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return False