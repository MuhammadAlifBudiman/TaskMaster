# Task Master

Task Master is a feature-rich web application that empowers users to efficiently manage their daily, weekly, and monthly tasks. The application offers a seamless user experience with real-time task management capabilities, allowing users to effortlessly add, edit, delete, and mark tasks as complete without the need to refresh the page.

This project is part of the CS50 course: [HarvardX: CS50's Web Programming with Python and JavaScript](https://www.edx.org/learn/web-development/harvard-university-cs50-s-web-programming-with-python-and-javascript).

#### Demo: [Youtube](https://youtu.be/zhIjcGUKfak)

#### Website: [TaskMaster](https://alif.pythonanywhere.com)

#### API Docs: [Docs](https://alif.pythonanywhere.com/api/docs)

#### API Playground: [Playground](https://alif.pythonanywhere.com/api/playground)

## Features

1. **Task Types:** Task Master provides support for daily, weekly, and monthly tasks, enabling users to organize and prioritize their tasks effectively.
2. **API for Task Management:** The application offers a robust API to handle Create, Read, Update, and Delete (CRUD) operations for tasks, complete with input validation for enhanced data integrity.
3. **Interactive Data Tables:** Task lists are displayed using dynamic data tables with built-in functionalities such as pagination, sorting, and searching, making it easy for users to find and access their tasks efficiently.
4. **Smart Task Sorting:** Tasks are intelligently sorted based on completion status and execution time, ensuring that users can effortlessly focus on their pending tasks.
5. **Task Completion Tracking:** A badge prominently displays the number of incomplete tasks, providing users with a quick overview of their pending responsibilities.
6. **Automatic Task Reset:** The application automatically resets daily tasks at 00:00, weekly tasks every Monday at 00:00, and monthly tasks on the 1st day of the month at 00:00, all based on the user's specified timezone.
7. **Secure Registration Form:** The registration form is equipped with validations, including checks for alphanumeric full names, username availability, strong password requirements, and matching passwords.
8. **User-Friendly Login and Registration:** Users can seamlessly register an account and log in using Django views, ensuring a smooth onboarding experience.
9. **Task History:** Completed tasks are automatically saved to the task history, providing users with a comprehensive record of their accomplishments.
10. **Task Export to Excel:** Users can export their tasks to Excel, facilitating easy data sharing and analysis.

## Tech Stack

Front-end:

- HTML: Markup language for creating the structure of web pages.
- CSS: Styling language for designing the appearance of web pages.
- JavaScript: Programming language for adding interactivity to web pages.
- Bootstrap (v5.2.3): Front-end framework for creating responsive and mobile-first web pages.

Back-end:

- Django (v4.2): Python web framework for building the backend of the application.
- Python libraries:
  - psycopg2-binary (v2.9.6): PostgreSQL database adapter for Python.
  - python-decouple (v3.8): Configuration file management for Python projects.
  - parameterized (v0.9.0): Decorator for parameterized testing in Python.
  - djangorestframework (v3.14.0): Django toolkit for building Web APIs.
  - djangorestframework-simplejwt (v5.2.2): Django REST framework support for JSON Web Tokens.
  - pytz (v2022.1): Python library for working with time zones.
  - openpyxl (v3.1.2): Python library for working with Excel files.
  - drf-yasg (v1.21.7): Yet Another Swagger Generator for Django REST framework.

Front-end Libraries and Plugins (Used in HTML File):

- Font Awesome (latest version): Icon library for adding scalable vector icons.
- Unicons (v2.1.9): Icon library for adding icons to the user interface.
- jQuery (v3.7.0): JavaScript library for simplifying DOM manipulation and event handling.
- jQuery Validation (v1.19.5): jQuery plugin for form validation.
- DataTables (1.13.5): JavaScript library for adding advanced features to HTML tables.
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

- Python (version 3.8) or higher.

### Installation

1. Clone the repository:

```
git clone https://github.com/MuhammadAlifBudiman/TaskMaster.git
```

2. Change into the project directory:

```
cd TaskMaster
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
python manage.py makemigrations taskmaster
```

```
python manage.py migrate
```

7. Set up database seeder (optional):
   - Change the number of num_tasks_records and num_users_records in `taskmaster/management/command` according to the amount you want
   - Run database seeder:

```
python manage.py database_seeder
```

8. Start the development server:

```
python manage.py runserver
```

9. Access the application in your web browser:

```
http://localhost:8000
```

## Usage

1. Access the Task Master web application and either register a new account or log in using your existing credentials.
2. Once logged in, you'll be presented with the dashboard, where you can easily manage your tasks.
3. The application will automatically reset daily tasks at 00:00, weekly tasks every Monday at 00:00, and monthly tasks on the 1st day of the month at 00:00, all based on your specified timezone.
4. For data analysis and sharing, Task Master enables you to export your tasks to Excel, allowing you to work with the data offline and collaborate with others.
5. For advanced users and developers, Task Master offers a comprehensive API that supports CRUD operations for tasks. The API includes data validation to manage tasks programmatically.
6. To explore the API documentation and test the endpoints interactively, navigate to `/api/playground/` for Swagger UI or `/api/docs/` for ReDoc.

## Contributing

Contributions are welcome! If you'd like to contribute to the Task Master project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature, bug fix, or any other improvement. Choose a descriptive and meaningful name for your branch, such as `feature/new-task-manager` or `bugfix/issue-42`.
3. Make your changes in the new branch.
4. Commit your changes with clear and concise commit messages. A good commit message should explain the purpose of the change and be easy to understand by others.
5. Push your changes to your forked repository on GitHub.
6. Submit a pull request from your branch to the original repository's `development` branch (or `main` branch if it is the stable version). In your pull request description, provide a detailed explanation of the changes you have made and the reason for the contribution. Additionally, reference any related issues or feature requests if applicable.
7. The maintainers of the Task Master project will review your pull request. They may ask for additional changes or clarifications before merging your contribution into the project.
8. Once your pull request is approved, your changes will be merged into the `development` branch. For bug fixes or critical changes, they might be directly merged into the `main` branch for deployment.
9. Congratulations! You've successfully contributed to the Task Master project. Your changes will be available in the next release.

Branching Workflow:

- `main`: The main branch contains the stable version of the project that is suitable for deployment.
- `development`): The development branch serves as the integration branch for ongoing development. New features and bug fixes are merged into this branch for testing and review.
- `feature/feature-name`: Feature branches are used for developing new features or major changes. Each feature has its own branch, and it is merged into `development` after it is completed and reviewed.
- `bugfix/issue-number`: Bugfix branches are used to address specific issues or bugs reported in the project. Each bugfix has its own branch, and it is merged into `development` after the bug is fixed and reviewed.
- `hotfix/issue-number`: Hotfix branches are used for critical fixes that need to be deployed to production immediately. Once the hotfix is complete and reviewed, it is merged into both `main` and `development`.
- `release/version-number`: Release branches are used when preparing a new version for deployment. They are created from `development`, and once all the features and bugfixes for a specific version are complete and tested, the release branch is merged into `main` for deployment.

**Note:** Please make sure to keep your forked repository up to date with the original repository's `development` branch to avoid conflicts during the pull request process.

Thank you for your interest in contributing to Task Master! We look forward to your valuable contributions and collaboration. If you have any questions or need further assistance, feel free to reach out to the maintainers. Happy coding! 🚀

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

For any inquiries or feedback, please contact me at alifm2101@gmail.com.
