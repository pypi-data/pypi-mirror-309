import requests


def jql_ticket(server_url, auth, jql_query, max_results=None):
    """
    Retrieve tickets based on a provided JQL query, up to a specified maximum number of results.

    :param server_url: Base URL of the Jira server.
    :param auth: Tuple containing email and API token for authentication.
    :param jql_query: The Jira Query Language query string to retrieve tickets.
    :param max_results: The maximum number of tickets to retrieve. If not specified, fetches all tickets.
    :return: List of ticket keys if successful, or False otherwise.
    """
    all_ticket_keys = []
    start_at = 0
    batch_size = 50  # This number can be adjusted based on your preference

    print(f"Executing JQL query: '{jql_query}'...")

    while True:
        payload = {
            "jql": jql_query,
            "fields": ["key"],  # We only need the ticket key
            "maxResults": batch_size,
            "startAt": start_at
        }

        response = requests.post(
            f"{server_url}/rest/api/2/search",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            auth=auth,
            json=payload
        )

        if response.status_code == 200:  # HTTP 200 OK, indicates success.
            issues = response.json().get("issues", [])
            ticket_keys = [issue["key"] for issue in issues]
            all_ticket_keys.extend(ticket_keys)

            print(f"Fetched {len(ticket_keys)} tickets in this batch.")

            # Check if we need to fetch more results or if we've reached the limit if one was set
            if not max_results:
                if len(ticket_keys) < batch_size:
                    break
            else:
                if len(all_ticket_keys) >= max_results:
                    all_ticket_keys = all_ticket_keys[:max_results]
                    break

            start_at += batch_size
        else:
            print(f"Failed to fetch tickets. HTTP Status Code: {response.status_code}, Response: {response.text}")
            return False

    print(f"Total tickets fetched: {len(all_ticket_keys)}")
    return all_ticket_keys