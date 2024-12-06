import requests


def attach_file_to_ticket(server_url, auth, ticket_id, file_path):
    """
    Attach a file to a Jira ticket.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param ticket_id: ID of the Jira ticket.
    :param file_path: Path to the file to be attached.
    :return: True if the file was attached successfully, False otherwise.
    """
    url = f"{server_url}/rest/api/2/issue/{ticket_id}/attachments"
    headers = {
        "X-Atlassian-Token": "no-check"
    }
    files = {
        "file": open(file_path, "rb")
    }

    response = requests.post(url, headers=headers, auth=auth, files=files)

    if response.status_code == 200:
        print(f"File '{file_path}' attached successfully to ticket '{ticket_id}'.")
        return True
    else:
        print(f"Failed to attach file. Status code: {response.status_code}, Response: {response.text}")
        return False
