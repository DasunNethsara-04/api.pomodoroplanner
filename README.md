# Pomodoro Planner Backend

This is the backend for the Pomodoro Planner app, designed to help students effectively manage their study sessions using the Pomodoro technique. The Pomodoro Planner app includes a Pomodoro Timer and a Todo list. This backend is built using Python, FastAPI, and MySQL.

## Features

- **Pomodoro Timer**: Manage and track Pomodoro sessions.
- **Todo List**: Create, update, and delete Todos.
- **User Management**: Register and authenticate users.

## Setup

### Prerequisites

- Python 3.10+
- MySQL 8.x
- Git

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DasunNethsara-04/api.pomodoroplanner.git
   cd api.pomodoroplanner
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the MySQL database:**
   - Create a new MySQL database named `pomodoro_planner`.
     ```sql
     CREATE DATABASE pomodoro_planner;
     ```
   - Update the `DATABASE_URL` in the `database.py` file with your database credentials.

## Running the Application

1. **Start the FastAPI server:**

   ```bash
   fastapi dev app.py
   ```

2. **Access the API documentation:**
   Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation.

## API Endpoints

- **Testing Message**: `GET /api/`
- **API Info**: `GET /api/info`
- **User Registration**: `POST /auth/`
- **User Login**: `POST /api/token/`
- **Create Todo**: `POST /api/todo/`
- **Get Todos**: `GET /api/todos/`
- **Get Todo by ID**: `GET /api/todo/{todo_id}`
- **Update Todo**: `PUT /api/todo/{todo_id}/`
- **Delete Todo**: `DELETE /api/todo/{todo_id}/`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
