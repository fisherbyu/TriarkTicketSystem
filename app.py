import streamlit as st
import requests

class EmployeeForm:
    # Define Constants and Keys
    NOTION_API_KEY = st.secrets["NOTION_API_KEY"]
    DATABASE_ID = st.secrets["DATABASE_ID"]
    URL = f'https://api.notion.com/v1/pages'

    # Define Options
    applications = ["", "Text/Email", "JobNimbus Document Templates", "JobNimbus Automations"]
    ticket_types = ["", "Suggestion", "Question", "Bug/Issue"]
    severity_options = ["", "Low", "Medium", "High", "Extreme"]


    def __init__(self):
        self.name = ""
        self.problem_application = ""
        self.ticket_type = ""
        self.severity = ""
        self.description = ""


    def render(self):
        st.header("Triark IT Ticket Form")
        st.text("To report an issue, fill out the IT ticket form below. Only submit once per request. \nTo submit multiple requests, refresh page.")

        with st.form("employee_info_form"):
            self.name = st.text_input("Name:", value=self.name)
            col1, col2, col3 = st.columns(3)
            self.problem_application = col1.selectbox("Problem Application:", options=self.applications, index=self.applications.index(self.problem_application))
            self.ticket_type = col2.selectbox("Ticket Type", options=self.ticket_types, index=self.ticket_types.index(self.ticket_type))
            self.severity = col3.selectbox("Severity", options=self.severity_options, index=self.severity_options.index(self.severity))
            self.description = st.text_area("Description:", placeholder="Please describe the issue in detail.  If applicable, include a job title for me to reference.", value=self.description)
            submit_button = st.form_submit_button("Submit")

        if submit_button:
            if self.validate_input():
                self.update_db()
                st.success("Ticket information submitted successfully.")
                self.reset_form()

    def validate_input(self):
        if not self.name or not self.problem_application or not self.ticket_type or not self.severity or not self.description:
            st.error("Please fill in all fields.")
            return False
        return True

    def update_db(self):
        # Send Ticket to Notion DB
        headers = {
            'Authorization': f'Bearer {self.NOTION_API_KEY}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
        }
        # Assemble Notion Object
        data = {
            "parent": {
                "database_id": self.DATABASE_ID
            },
            "properties": {
                "Employee Name": {
                    "title": [
                        {
                            "text": {
                                "content": self.name
                            }
                        }
                    ]
                },
                "Problem Application": {
                    "select": {
                        "name": self.problem_application
                    }
                },
                "Ticket Type": {
                    "select": {
                        "name": self.ticket_type
                    }
                },
                "Severity": {
                    "select": {
                        "name": self.severity
                    }
                },
                "Description": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": self.description
                            }
                        }
                    ]
                }
            }
        }
        # Send the POST request
        response = requests.post(self.URL, headers=headers, json=data)

        # Check the response status code
        if response.status_code == 200:
            # The request was successful, and the data is in response.json()
            data = response.json()
            print(data)
        else:
            # There was an error in the request
            print(f"Request failed with status code {response.status_code}: {response.text}")


    def reset_form(self):
        self.name = ""
        self.problem_application = ""
        self.ticket_type = ""
        self.severity = ""
        self.description = ""


if __name__ == "__main__":
    st.session_state.employee_form = EmployeeForm()
    st.session_state.employee_form.render()
