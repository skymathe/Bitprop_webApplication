# Bitprop Web Application

This is a Real Estate Management System implemented in Python using Flask. It allows users to manage properties, handle leasing and selling inquiries, and interact with agents and tenants.

## Features

- **User Authentication**: Supports authentication for Admins, Agents, and Tenants.
- **Property Management**: Admins and Agents can add, update, and manage property listings.
- **Leasing and Selling Inquiries**: Users can inquire about leasing or selling properties through dedicated forms.
- **Email Notifications**: Notifications are sent to agents when users express interest in properties or inquire about leasing/selling.

## Technologies Used

- **Flask**: Python web framework used for backend development.
- **Flask-SQLAlchemy**: Flask extension for SQL database integration.
- **Flask-Login**: Flask extension for user authentication.
- **Flask-Mail**: Flask extension for sending emails.
- **Flask-WTF**: Flask extension for handling web forms.
- **SQLite**: Lightweight relational database management system.

## Setup and Installation

1. Clone the repository: `git clone https://github.com/skymathe/Bitprop_webApplication.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Access the website at (http://127.0.0.1:5000)

## Usage

- Visit the homepage to browse available properties and learn more about the system.
- Sign up as a tenant or log in as an existing user (Admin, Agent, or Tenant).
- Admins and Agents can manage properties and view inquiries from tenants.
- Tenants can view properties, express interest in listings, and contact agents for leasing inquiries.

## Email Confirmation

To verify that the email functionality works, you can use the provided Mailtrap credentials:

- **Mailtrap Credentials**:
  - **Email:** makenzie@xsellsy.com
  - **Password:** testing_1

Follow these steps to verify email functionality:

1. Go to [Mailtrap](https://mailtrap.io/).
2. Log in using the provided credentials.
3. Once logged in, you should see the Mailtrap inbox.
4. Trigger actions in the application that are expected to send emails, such as signing up, submitting inquiries, or adding properties.
5. Check the Mailtrap inbox for any emails sent by the application.

By following these steps, you can verify that the email functionality is working as expected, and you can see the content and format of the emails being sent from the application.

## Users

The application includes the following user roles:

### Admin
- **Email:** your-email@gmail.com
- **Password:** admin-password
- **Description:** Admins have overall control over the system. They can upload properties, view all registered users, and handle emails. 

### Agents
- **Agent1**
  - **Email:** agent1@example.com
  - **Password:** agent-password
  - **Description:** Agents act as intermediaries between admins and tenants. They receive communication from tenants regarding issues such as repairs. They can also be property owners that the application manages.

### Tenants
- **Tenant1**
  - **Email:** tenant1@example.com
  - **Password:** tenant-password
  - **Description:** Tenants have access to the application for better management of the property.

These user roles have specific functionalities and access levels within the application, contributing to its overall functionality and management capabilities.

## Errors

The following errors have been identified in the application:

1. **Login Flash Messages**: 
   - Flash messages are not displayed when logging in. For example, it does not display a message when the password is incorrect.

2. **Adding Property Manually**:
   - Adding property manually does not work as expected. Hard coding was necessary to force property into the database.

3. **Agents List Display**:
   - The agents list does not display the number of bedrooms and bathrooms for each property.

4. **Tenant Database Display**:
   - When tenants are logged in, the database does not display any information.

5. **Old Database**:
    - The old database is still present in the application, which may cause confusion and lead to errors.
    -I do not know how to remove it yet.

6. **Home Page Search Bar**:
    -The search bar on the home page is not linked to anything.

___

for futher assistance contact me at fezilenmathe@gmail.com, 0760426672
