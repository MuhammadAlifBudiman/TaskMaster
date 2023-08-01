# Task Master

Task Master is a feature-rich web application that empowers users to efficiently manage their daily, weekly, and monthly tasks. The application offers a seamless user experience with real-time task management capabilities, allowing users to effortlessly add, edit, delete, and mark tasks as complete without the need to refresh the page.

#### Video Demo:[Demo](https://youtu.be/TTgARJFSDxc)
#### Website: [TaskMaster](https://alif.pythonanywhere.com)

## Features

- **Task Types:** Task Master provides support for daily, weekly, and monthly tasks, enabling users to organize and prioritize their tasks effectively.

- **API for Task Management:** The application offers a robust API to handle Create, Read, Update, and Delete (CRUD) operations for tasks, complete with input validation for enhanced data integrity.

- **Interactive Data Tables:** Task lists are displayed using dynamic data tables with built-in functionalities such as pagination, sorting, and searching, making it easy for users to find and access their tasks efficiently.

- **Smart Task Sorting:** Tasks are intelligently sorted based on completion status and execution time, ensuring that users can effortlessly focus on their pending tasks.

- **Task Completion Tracking:** A badge prominently displays the number of incomplete tasks, providing users with a quick overview of their pending responsibilities.

- **Automatic Task Reset:** The application automatically resets daily tasks at 00:00, weekly tasks every Monday at 00:00, and monthly tasks on the 1st day of the month at 00:00, all based on the user's specified timezone.

- **Secure Registration Form:** The registration form is equipped with validations, including checks for alphanumeric full names, username availability, strong password requirements, and matching passwords.

- **User-Friendly Login and Registration:** Users can seamlessly register an account and log in using Django views, ensuring a smooth onboarding experience.

- **Real-Time Notifications:** Task Master utilizes SweetAlert2 for elegant and non-intrusive notifications, enhancing user engagement and feedback.

- **Task History:** Completed tasks are automatically saved to the task history, providing users with a comprehensive record of their accomplishments.

- **Task Export to Excel:** Users can export their tasks to Excel, facilitating easy data sharing and analysis.

## Tech Stack

Front-end:
- HTML: Markup language for creating the structure of web pages.
- CSS: Styling language for designing the appearance of web pages.
- JavaScript: Programming language for adding interactivity to web pages.
- Unicons: Icon library for adding icons to the user interface.
- Bootstrap 5.2.3: Front-end framework for creating responsive and mobile-first web pages.
- DataTables: JavaScript library for adding advanced features to HTML tables.

Back-end:
- Django 4.2: Python web framework for building the backend of the application.
- Python libraries:
  - psycopg2-binary: PostgreSQL database adapter for Python.
  - python-decouple: Configuration file management for Python projects.
  - parameterized: Decorator for parameterized testing in Python.
  - djangorestframework: Django toolkit for building Web APIs.
  - djangorestframework-simplejwt: Django REST framework support for JSON Web Tokens.
  - pytz: Python library for working with time zones.
  - openpyxl: Python library for working with Excel files.
  - drf-yasg: Yet Another Swagger Generator for Django REST framework.

Front-end Libraries and Plugins (Used in HTML File):
- Font Awesome: Icon library for adding scalable vector icons.
- jQuery (v3.7.0): JavaScript library for simplifying DOM manipulation and event handling.
- jQuery Validation (v1.19.5): jQuery plugin for form validation.
- Select2 (v4.1.0-rc.0): jQuery-based replacement for select boxes with search support.
- SweetAlert2 (v10): JavaScript library for beautiful and customizable alert dialogs.

## Files and Directory Structure

The Task Master project follows a typical Django project structure. Here's an overview of the main directories and files:

- `task/`: The main project directory
  - `asgi.py`: ASGI configuration for Django
  - `settings.py`: Configuration file for Django settings, including database setup
  - `urls.py`: URL configuration for the project
  - `wsgi.py`: Entry point for the project's WSGI application
- `taskmaster/`: The main Django app directory
  - `api/`: Contains API related files
    - `api.py`: API views and viewsets
  - `forms/`: Contains form-related files
    - `forms.py`: Custom forms for the Task Master app
  - `management/`: Contains management commands
    - `commands/`: Custom commands for managing the database and tasks
      - `database_seeder.py`: Command for seeding the database
      - `reset_daily_tasks.py`: Command for resetting daily tasks
      - `reset_weekly_tasks.py`: Command for resetting weekly tasks
      - `reset_monthly_tasks.py`: Command for resetting monthly tasks
  - `seeders/`: Contains seeder files
    - `database_seeder.py`: Seeder file for populating the database with initial data
  - `serializers/`: Contains serializer files
    - `serializers.py`: Serialization for data models in the Task Master app
  - `static/taskmaster/`: Static assets (CSS, JavaScript, images)
    - `script.js`: JavaScript code for the Task Master app
    - `style.css`: CSS styles for the Task Master app
    - `sweetalert2.js`: SweetAlert2 library for displaying alert dialogs
  - `templates/taskmaster/`: Templates for the Task Master app
    - `auth.html`: Template for authentication
    - `dailytask.html`: Template for displaying daily tasks
    - `index.html`: Template for the home page
    - `layout.html`: Base template with common elements
    - `monthlytask.html`: Template for displaying monthly tasks
    - `weeklytask.html`: Template for displaying weekly tasks
  - `admin.py`: Admin configurations for the Task Master app
  - `apps.py`: Application configuration for the Task Master app
  - `middleware.py`: Custom middleware for the Task Master app
  - `models.py`: Contains the data models for the project
  - `tests.py`: Unit tests for the Task Master app
  - `urls.py`: URL configuration for the Task Master app
  - `validators.py`: Custom validators for form fields in the Task Master app
  - `views.py`: Views for handling HTTP requests and responses in the Task Master app
  - `.env`: Environment file (not shown in the repository) for storing sensitive configuration data
  - `.gitignore`: File to specify files and directories to ignore in the Git repository
  - `LICENSE.txt`: License file for the project (if applicable)
  - `manage.py`: Django's command-line utility for managing the project
  - `README.md`: This file, providing information about the project
  - `requirements.txt`: A file listing the required Python packages for the project

## Getting Started

Follow the instructions below to set up and run the Task Master web application locally on your machine.

### Prerequisites

- Python (version 3.10.6)

### Installation

1. Clone the repository:

```
git clone https://github.com/your-username/task-master.git
```

2. Change into the project directory:

```
cd task-master
```

3. Create a `.env` file in the project root and add the following configuration:

```
# Database configuration
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port

# Django secret key (generate a new key below)
SECRET_KEY=your_secret_key

# Debug mode (set to 'True' for development)
DEBUG=True

# Allowed hosts (comma-separated list)
ALLOWED_HOSTS=localhost,127.0.0.1
```
4. Generate a new Django `SECRET_KEY`:

For security reasons, each contributor should generate their own unique `SECRET_KEY`. You can generate a new key by running the following Python code in your terminal:

```python
import secrets

print(secrets.token_hex(64))
```

Copy the generated key (a long string of random characters) and replace `your_secret_key` in the `.env` file with this new value.

**Note:** Keep the `SECRET_KEY` value confidential and do not share it publicly or commit it to version control systems. Each contributor should have their own unique key.

5. Install the project dependencies:

```
pip install -r requirements.txt
```

6. Set up the database:
   - Update the database configuration in `project/settings.py` to read the values from the `.env` file.
   - Run the database migrations:

```
python manage.py migrate
```

7. Start the development server:

```
python manage.py runserver
```

8. Access the application in your web browser:

```
http://localhost:8000
```

## Usage

1. Access the Task Master web application and either register a new account or log in using your existing credentials.

2. Once logged in, you'll be presented with the dashboard, where you can easily manage your tasks.

3. To create a new task, navigate to either the "Daily Tasks" or "Weekly Tasks" section, depending on the type of task you want to add.

4. Click on the "Add Task" button to open a form where you can provide the title, description, execution time, and other details for your task.

5. Save the task by clicking the "Add" button. The new task will appear in the task list with a badge indicating the number of incomplete tasks.

6. To update a task, simply click the "Edit" button corresponding to the task you wish to modify. You can make changes to the task details and save the updated information.

7. If a task is no longer relevant, you can remove it by clicking the "Delete" button next to the task entry. Deleted tasks will be stored in the task history for reference.

8. As you complete tasks, mark them as completed by double-clicking on the task item. The task will be visually marked as completed, and the "Completed" status will be updated accordingly.

9. The application will automatically reset daily tasks at 00:00, weekly tasks every Monday at 00:00, and monthly tasks on the 1st day of the month at 00:00, all based on your specified timezone.

10. For advanced users and developers, Task Master offers a comprehensive API that supports CRUD operations for tasks. The API includes data validation and secure endpoints to manage tasks programmatically.

11. To explore the API documentation and test the endpoints interactively, navigate to `/api/playground/` for Swagger UI or `/api/docs/` for ReDoc.

12. Task Master provides real-time notifications using SweetAlert2, ensuring you receive prompt feedback and updates about your task management activities.

13. For data analysis and sharing, Task Master enables you to export your tasks to Excel, allowing you to work with the data offline and collaborate with others.

## Contributing

Contributions are welcome! If you'd like to contribute to the Task Master project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request detailing your changes.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgements

- [Unicons](https://iconscout.com/unicons) - Icon library used in the Task Master web application.
- [DataTables](https://datatables.net/) - JavaScript library used for advanced table functionality.
- [Bootstrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/) - Front-end framework for creating responsive and mobile-first web pages.
- [Font Awesome](https://fontawesome.com/) - Icon library for adding scalable vector icons.
- [jQuery](https://jquery.com/) - JavaScript library for simplifying DOM manipulation and event handling.
- [jQuery Validation](https://jqueryvalidation.org/) - jQuery plugin for form validation.
- [Select2](https://select2.org/) - jQuery-based replacement for select boxes with search support.
- [SweetAlert2](https://sweetalert2.github.io/v10.html) - JavaScript library for beautiful and customizable alert dialogs.
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) - PostgreSQL database adapter for Python.
- [python-decouple](https://pypi.org/project/python-decouple/) - Configuration file management for Python projects.
- [parameterized](https://pypi.org/project/parameterized/) - Decorator for parameterized testing in Python.
- [djangorestframework](https://www.django-rest-framework.org/) - Django toolkit for building Web APIs.
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/) - Django REST framework support for JSON Web Tokens.
- [pytz](https://pypi.org/project/pytz/) - Python library for working with time zones.
- [openpyxl](https://pypi.org/project/openpyxl/) - Python library for working with Excel files.
- [drf-yasg](https://drf-yasg.readthedocs.io/) - Yet Another Swagger Generator for Django REST framework.

## Contact

For any inquiries or feedback, please contact us at taskmaster@example.com.
