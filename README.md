# Student Grade Tracker

Student Grade Tracker is a web-based application built with Flask and MySQL that allows educators or users to manage and track student grades efficiently. It features user authentication, a dashboard for student management, and real-time statistics calculation.

## Features

- **User Authentication**: Secure user registration and login system with password hashing.
- **Student Management**: Add, edit, and delete student records (Name, Subject, Grade).
- **Dashboard Statistics**: Automatically calculates total students, average grade, passed, and failed statistics.
- **REST API Endpoint**: Provides a JSON endpoint (`/api/students`) to retrieve student data.
- **Responsive Interface**: Web pages rendered using Flask templates.

## Tech Stack

- **Backend**: Python, Flask
- **Database**: MySQL (`flask-mysqldb`)
- **Server**: Gunicorn, Nginx (for production)
- **Containerization**: Docker

## Prerequisites

Before running this project, ensure you have the following installed:
- Python 3.x
- MySQL Server

## Local Setup & Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd "student - App"
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**:
   - Ensure your MySQL server is running.
   - Run the provided `schema.sql` file to create the database and required tables (Note: the app also auto-initializes tables on the first request if they don't exist):
     ```bash
     mysql -u root -p < schema.sql
     ```
   - *Optional:* Update the MySQL connection details in `app.py` if your database credentials differ:
     ```python
     app.config['MYSQL_HOST']     = 'localhost'
     app.config['MYSQL_USER']     = 'root'
     app.config['MYSQL_PASSWORD'] = '' # Add your password here
     app.config['MYSQL_DB']       = 'studentdb'
     ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will be accessible at `http://localhost:5000`.

## Deployment

This application includes configuration files for production deployment using **Gunicorn** and **Nginx**, as well as a `Dockerfile` for containerized environments. 

For detailed deployment instructions (such as setting up systemd services and configuring Nginx), please refer to the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) included in this repository.

## API Documentation

### `GET /api/students`
Retrieves a list of all students associated with the currently logged-in user in JSON format.
- **Authentication**: Required (Session-based)
- **Response**: Array of student objects containing `id`, `name`, `subject`, `grade`, and `user_id`.
