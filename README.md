# Task Master

Task Master is a web application that allows users to manage their daily and weekly tasks. Users can register an account, log in, create, view, update, and delete their tasks. The application provides a user-friendly interface with features like task completion tracking.

## Features

- User authentication: Register an account and log in to access the task management features.
- CRUD Daily Tasks: Create, view, update, and delete daily tasks.
- CRUD Weekly Tasks: Create, view, update, and delete weekly tasks.
- Task Completion Tracking: Mark tasks as completed and track their completion status.

## Tech Stack

- HTML: Markup language for creating the structure of web pages.
- CSS: Styling language for designing the appearance of web pages.
- Unicons: Icon library for adding icons to the user interface.
- jQuery: JavaScript library for simplifying DOM manipulation and event handling.
- JavaScript: Programming language for adding interactivity to web pages.
- Django: Python web framework for building the backend of the application.
- DataTables: JavaScript library for adding advanced features to HTML tables.

## Files and Directory Structure

The Task Master project follows a typical Django project structure. Here's an overview of the main directories and files:

- `task/`: The main project directory
  - `settings.py`: Configuration file for Django settings, including database setup
  - `urls.py`: URL configuration for the project
  - `wsgi.py`: Entry point for the project's WSGI application
- `taskmaster/`: The main Django app directory
  - `migrations/`: Database migration files
  - `static/taskmaster`: Static assetes(CSS, JavaScript, image)
  - `template/taskmater`: Templates for the Task Master app
    - `layout.html`: Base template with common elements
    - `dailytask.html`: Template for displaying daily tasks
    - `weeklytask.html`: Template for displaying weekly tasks
    - `auth.html`: Template for authentication
    - `index.html`: Template for home page
  - `admin.py`: Custom middleware for the Task Master app
  - `apps.py`: Application configuration for the Task Master app
  - `middleware.py`: Custom middleware for the Task Master app
  - `models.py`: Contains the data models for the project
  - `tests.py`: Unit tests for the Task Master app
  - `urls.py`: URL configuration for the Task Master app
  - `views.py`: Views for handling HTTP requests and responses
- `LICENSE`: License file for the project 
- `README.md`: This file, providing information about the project
- `manage.py`: Django's command-line utility for managing the project
- `requirements.txt`: A file listing the required Python packages for the project

You can customize this structure according to your actual file and directory layout. Provide an explanation of the purpose of each main directory and important files, highlighting any specific files or directories that are relevant to understanding and contributing to the project.

## Getting Started

Follow the instructions below to set up and run the Task Master web application locally on your machine.

### Prerequisites

- Python (version 4.2)
- Django (version 3.10.6)

### Installation

1. Clone the repository:

```
git clone https://github.com/your-username/task-master.git
```

2. Change into the project directory:

```
cd task-master
```

3. Install the project dependencies:

```
pip install -r requirements.txt
```

4. Set up the database:
   - Update the database configuration in `project/settings.py` according to your database setup.
   - Run the database migrations:
     ```
     python manage.py migrate taskmaster
     ```

5. Start the development server:

```
python manage.py runserver
```

6. Access the application in your web browser:

```
http://localhost:8000
```

## Usage

1. Register a new account or log in with your existing credentials.
2. Navigate to the "Daily Tasks" or "Weekly Tasks" section to manage your tasks.
3. Click on "Add Task" to create a new task and provide the necessary details.
4. Edit or delete tasks using the corresponding buttons in the task list.
5. Mark them as completed if you have complete the task.

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

## Contact

For any inquiries or feedback, please contact us at taskmaster@example.com.
