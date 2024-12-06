import requests
from .if_ticket_exist import if_ticket_exist


def comment_ticket(server_url, auth, ticket_key, comment_text):
    """
    Add a comment to a ticket with the provided key.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param ticket_key: Key of the ticket where the comment will be added.
    :param comment_text: Text of the comment to be added.
    :return: URL of the created comment if successful, or False otherwise.
    """
    # Checking if the ticket exists
    if not if_ticket_exist(server_url, auth, ticket_key):
        return False

    # Preparing the payload to add the comment
    print(f"Adding comment to ticket: {ticket_key}...")
    payload = {
        "body": comment_text
    }

    response = requests.post(
        f"{server_url}/rest/api/2/issue/{ticket_key}/comment",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        json=payload
    )

    # Evaluating the response
    if response.status_code == 201:  # HTTP 201 Created, indicates success.
        comment_id = response.json().get("id")
        comment_url = f"{server_url}/browse/{ticket_key}?focusedCommentId={comment_id}#comment-{comment_id}"
        print(f"Successfully added comment to ticket {ticket_key}. Comment URL: {comment_url}")
        return comment_url
    else:
        print(f"Failed to add comment. Status code: {response.status_code}, Response: {response.text}")
        return False
