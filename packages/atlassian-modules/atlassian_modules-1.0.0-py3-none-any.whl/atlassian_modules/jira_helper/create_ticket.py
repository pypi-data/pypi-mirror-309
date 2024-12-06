import requests


def create_ticket(server_url, auth, project_key, summary, description, issue_type):
    """
    Create a ticket in a specified project using the provided details.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param project_key: Key of the project where the new ticket will be created.
    :param summary: Summary of the new ticket.
    :param description: Detailed description of the new ticket.
    :param issue_type: Type of the issue (e.g., Bug, Task, Story).
    :return: URL of the created ticket or False if the creation failed.
    """
    # Preparing issue data
    print("Preparing issue data...")
    issue_data = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
    }

    # Making a request to create a ticket
    print(f"Sending request to create a ticket in project {project_key}...")
    response = requests.post(
        f"{server_url}/rest/api/2/issue",
        json=issue_data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth
    )

    # Checking response
    if response.status_code == 201:  # HTTP 201 Created
        print("Ticket created successfully!")
        ticket_data = response.json()
        ticket_key = ticket_data["key"]
        ticket_url = f"{server_url}/browse/{ticket_key}"
        print(f"Ticket URL: {ticket_url}")
        return ticket_url
    else:
        print(f"Failed to create ticket. HTTP Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return False
