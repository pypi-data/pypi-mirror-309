# Importing the function to attach a file to a Jira ticket
from atlassian_modules.jira_helper.attach_file_to_ticket import attach_file_to_ticket

# Importing the function to get the subject of a Jira ticket
from atlassian_modules.jira_helper.get_ticket_subject import get_ticket_subject

# Importing the function to create a custom Jira ticket with additional fields
from atlassian_modules.jira_helper.create_custom_ticket import create_custom_ticket

# Importing the function to update a Jira ticket with specific fields
from atlassian_modules.jira_helper.update_ticket_with_fields import update_ticket_with_fields

# Importing the function to create a standard Jira ticket
from atlassian_modules.jira_helper.create_ticket import create_ticket

# Importing the function to delete a Jira ticket
from atlassian_modules.jira_helper.delete_ticket import delete_ticket

# Importing the function to get the possible transitions for a Jira ticket
from atlassian_modules.jira_helper.get_transitions import get_transitions

# Importing the function to transition a Jira ticket to a different state
from atlassian_modules.jira_helper.transition_ticket import transition_ticket

# Importing the function to check if a Jira ticket exists
from atlassian_modules.jira_helper.if_ticket_exist import if_ticket_exist

# Importing the function to add a comment to a Jira ticket
from atlassian_modules.jira_helper.comment_ticket import comment_ticket

# Importing the function to perform a JQL query on Jira tickets
from atlassian_modules.jira_helper.jql_ticket import jql_ticket

# Importing the function to create a wiki page
from atlassian_modules.wiki_helper.create_wiki_page import create_wiki_page

# Importing the function to duplicate a wiki page
from atlassian_modules.wiki_helper.duplicate_wiki_page import duplicate_wiki_page

# Importing the function to create a page from a template
from atlassian_modules.wiki_helper.create_page_from_template import create_page_from_template

# Importing the function to move a wiki page
from atlassian_modules.wiki_helper.move_wiki_page import move_wiki_page

# Importing the function to check if a wiki page exists
from atlassian_modules.wiki_helper.wiki_page_exists import wiki_page_exists

# Importing the function to get child pages recursively
from atlassian_modules.wiki_helper.get_child_pages_recursive import get_child_pages_recursive

# Importing the function to get the ID of a page
from atlassian_modules.wiki_helper.get_page_id import get_page_id

# Importing the function to replace content in a page
from atlassian_modules.wiki_helper.replace_in_page import replace_in_page

# Importing the function to get tables from a page
from atlassian_modules.wiki_helper.get_tables_from_page import get_tables_from_page

# Importing the function to update a wiki page
from atlassian_modules.wiki_helper.update_wiki_page import update_wiki_page

# Importing the function to get the parent page ID
from atlassian_modules.wiki_helper.get_parent_page_id import get_parent_page_id

# Importing the function to add a table of contents to a page
from atlassian_modules.wiki_helper.add_toc_to_page import add_toc_to_page

# Importing the function to get the content of a page
from atlassian_modules.wiki_helper.get_page_content import get_page_content

# Importing the function to update the content of a page
from atlassian_modules.wiki_helper.update_page_content import update_page_content

# Importing the function to add a row to a table in a page
from atlassian_modules.wiki_helper.add_row_to_table import add_row_to_table

# Importing the function to update or add a row to a table in a page
from atlassian_modules.wiki_helper.update_or_add_table_row import update_or_add_table_row


class JiraHelper:
    def __init__(self, server_url, email, api_token):
        self.server_url = server_url.rstrip('/')
        self.auth = (email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def attach_file_to_ticket(self, ticket_id, file_path):
        return attach_file_to_ticket(self.server_url, self.auth, ticket_id, file_path)

    def get_ticket_subject(self, ticket_id):
        return get_ticket_subject(self.server_url, self.auth, ticket_id)

    def create_custom_ticket(self, project_key, summary, description, issue_type, additional_fields=None):
        return create_custom_ticket(self.server_url, self.auth, project_key, summary, description, issue_type,
                                    additional_fields)

    def update_ticket_with_fields(self, ticket_id, additional_fields):
        return update_ticket_with_fields(self.server_url, self.auth, ticket_id, additional_fields)

    def create_ticket(self, project_key, summary, description, issue_type):
        return create_ticket(self.server_url, self.auth, project_key, summary, description, issue_type)

    def delete_ticket(self, ticket_key):
        return delete_ticket(self.server_url, self.auth, ticket_key)

    def get_transitions(self, ticket_key, transition_to):
        return get_transitions(self.server_url, self.auth, ticket_key, transition_to)

    def transition_ticket(self, ticket_key, transition_input):
        return transition_ticket(self.server_url, self.auth, ticket_key, transition_input)

    def if_ticket_exist(self, ticket_key):
        return if_ticket_exist(self.server_url, self.auth, ticket_key)

    def comment_ticket(self, ticket_key, comment_text):
        return comment_ticket(self.server_url, self.auth, ticket_key, comment_text)

    def jql_ticket(self, jql_query, max_results=None):
        return jql_ticket(self.server_url, self.auth, jql_query, max_results)


class WikiHelper:
    def __init__(self, server_url, email, api_token):
        self.server_url = server_url.rstrip('/') + "/wiki"
        self.auth = (email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def create_wiki_page(self, space_key, title, content, parent_page_id=None):
        return create_wiki_page(self.server_url, self.auth, space_key, title, content, parent_page_id)

    def duplicate_wiki_page(self, source_page_id, target_space_key, target_title, target_parent_page_id=None):
        return duplicate_wiki_page(self.server_url, self.auth, source_page_id, target_space_key, target_title,
                                   target_parent_page_id)

    def create_page_from_template(self, template_id, space_key, title, parent_page_id=None):
        return create_page_from_template(self.server_url, self.auth, template_id, space_key, title, parent_page_id)

    def move_wiki_page(self, page_id, target_space_key, target_position='append', target_parent_page_id=None):
        return move_wiki_page(self.server_url, self.auth, page_id, target_space_key, target_position,
                              target_parent_page_id)

    def wiki_page_exists(self, title, space_key):
        return wiki_page_exists(self.server_url, self.auth, title, space_key)

    def get_child_pages_recursive(self, parent_id):
        return get_child_pages_recursive(self.server_url, self.auth, parent_id)

    def get_page_id(self, title, space_key):
        return get_page_id(self.server_url, self.auth, title, space_key)

    def replace_in_page(self, page_id, from_string, to_string):
        return replace_in_page(self.server_url, self.auth, page_id, from_string, to_string)

    def get_tables_from_page(self, page_id):
        return get_tables_from_page(self.server_url, self.auth, page_id)

    def update_wiki_page(self, page_id, new_content):
        return update_wiki_page(self.server_url, self.auth, page_id, new_content)

    def get_parent_page_id(self, page_id):
        return get_parent_page_id(self.server_url, self.auth, page_id)

    def add_toc_to_page(self, page_id):
        return add_toc_to_page(self.server_url, self.auth, page_id)

    def get_page_content(self, page_id):
        return get_page_content(self.server_url, self.auth, page_id)

    def update_page_content(self, page_id, new_content):
        return update_page_content(self.server_url, self.auth, page_id, new_content)

    def add_row_to_table(self, page_id, headers, row_data):
        return add_row_to_table(self.server_url, self.auth, page_id, headers, row_data)

    def update_or_add_table_row(self, page_id, headers, new_row_data):
        return update_or_add_table_row(self.server_url, self.auth, page_id, headers, new_row_data)