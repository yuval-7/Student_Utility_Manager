# 🎓 Student Utility Manager

A **command-line based Student Utility Manager** built with **Python and MySQL** to help students organize their daily academic and personal activities from one place.

The application combines task management, note-taking, expense tracking, event planning, and a small insight/quote section into a single menu-driven program.

---

## ✨ Features

### 📋 1. Task Manager
Manage academic and personal tasks with persistent MySQL storage.

- Add new tasks
- Assign a subject to each task
- Set a due date
- Mark tasks as completed
- Delete tasks
- View all tasks
- View tasks by subject
- View pending tasks
- View task statistics
- See whether a task is:
  - Due today
  - Overdue
  - Due in a certain number of days

### 📝 2. Notes Archive
Store and manage detailed notes.

- Add notes with:
  - Title
  - Subject
  - Multi-line content
- View saved notes
- Edit existing notes
- Delete notes
- Prevent duplicate note titles

For multi-line notes, type `END` on a new line to finish entering the content.

### 💰 3. Expense Tracker
Keep track of personal/student expenses.

- Add an expense
- Store:
  - Date
  - Amount
  - Category
  - Description
- View all expenses
- Filter expenses by category
- Calculate:
  - Total expense for the last 7 days
  - Total expense for the last 30 days
  - Overall total expense

### 📅 4. Events Planner
Keep track of important upcoming events.

- Add an event
- View all events
- Automatically display:
  - Days remaining
  - Event happening today
  - Event already over
- Reschedule an event
- Cancel an event
- Prevent duplicate event titles

### 💡 5. Insight Centre
A lightweight section for motivation and interesting information.

- Random motivational messages
- Random "Did You Know?" facts
- Random quote of the day

The messages are selected randomly using Python's `random` module.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Application logic and CLI interface |
| **MySQL** | Persistent data storage |
| **mysql-connector-python** | Python ↔ MySQL database connection |
| **datetime** | Date calculations and due-date/event tracking |
| **random** | Random motivational messages, facts, and quotes |

---

## 🗄️ Database Structure

When the program starts, it automatically creates a MySQL database named:

```text
student
```

The following tables are created automatically if they do not already exist.

### `tasks`

Stores tasks and their completion status.

| Column | Type | Description |
|---|---|---|
| `task_id` | INT | Primary key, auto-incremented |
| `title` | VARCHAR(75) | Task title |
| `subject` | VARCHAR(25) | Related subject |
| `due_date` | DATE | Task deadline |
| `status` | VARCHAR(25) | `Not_Done` by default, or `Done` |

### `expense`

Stores expense records.

| Column | Type | Description |
|---|---|---|
| `ex_id` | INT | Primary key, auto-incremented |
| `date` | DATE | Expense date |
| `amount` | FLOAT | Expense amount |
| `category` | VARCHAR(45) | Expense category |
| `description` | TEXT | Additional details |

### `notes`

Stores academic/personal notes.

| Column | Type | Description |
|---|---|---|
| `event_id` | INT | Primary key, auto-incremented |
| `title` | VARCHAR(75) | Note title |
| `subject` | VARCHAR(25) | Related subject |
| `content` | TEXT | Note content |

### `events`

Stores scheduled events.

| Column | Type | Description |
|---|---|---|
| `event_id` | INT | Primary key, auto-incremented |
| `title` | VARCHAR(75) | Event title |
| `event_date` | DATE | Event date |

---

## 📁 Project Structure

A simple version of the project can be organized as:

```text
Student-Utility-Manager/
│
├── student_utility_manager.py
├── README.md
└── requirements.txt
```

> The main Python file can have any filename; update the run command accordingly.

---

## ⚙️ Requirements

Before running the project, make sure you have:

- Python 3.x
- MySQL Server
- `pip`
- MySQL Connector/Python

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

Replace `<your-username>` and `<your-repository>` with your GitHub details.

### 2. Install the Python dependency

```bash
pip install mysql-connector-python
```

Or, if you create a `requirements.txt` file:

```text
mysql-connector-python
```

Then install using:

```bash
pip install -r requirements.txt
```

### 3. Start MySQL

Make sure your MySQL server is running.

The program connects using:

```text
host     = localhost
user     = root
password = <your MySQL password>
```

When the program starts, it asks for your MySQL root password instead of storing the password directly in the source code.

### 4. Run the application

```bash
python student_utility_manager.py
```

---

## 🖥️ Main Menu

After successful database setup, the application provides:

```text
----------  Student Utility Manager  ----------
1. Task Manager
2. Notes Archive
3. Expenses Tracker
4. Events Planner
5. Insight Centre
6. Exit
-----------------------------------------------
```

Choose the required module and follow the interactive prompts.

---

## 🔄 Application Flow

```text
                    ┌─────────────────────────┐
                    │ Student Utility Manager │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
       │ Task Manager│    │ Notes Archive│    │Expense Tracker│
       └─────────────┘    └─────────────┘    └──────────────┘
              │                  │                  │
              ▼                  ▼                  ▼
           MySQL DB           MySQL DB           MySQL DB

                         ┌────────────────┐
                         │ Events Planner │
                         └───────┬────────┘
                                 │
                                 ▼
                              MySQL DB

                         ┌────────────────┐
                         │ Insight Centre │
                         └────────────────┘
```

---

## 📌 Example Use Cases

### Student Task Management
Add assignments, projects, exams, or other academic tasks and monitor their deadlines.

### Study Notes
Save subject-wise notes and update them whenever necessary.

### Personal Budgeting
Record daily expenses and quickly check spending over the previous 7 or 30 days.

### Event Planning
Keep track of exams, college events, meetings, submissions, or other important dates.

### Daily Motivation
Use the Insight Centre for a random motivational message, fact, or quote.

---

## 🔐 Database & Security Note

The application asks for the MySQL password at runtime, so the password does not need to be hard-coded into the source.

However, the current implementation constructs several SQL queries using Python f-strings. For a production-quality application, these queries should be changed to **parameterized SQL queries** to reduce the risk of SQL injection and to handle special characters safely.

For example, instead of dynamically inserting user input into a query, use MySQL connector parameters:

```python
cursor.execute(
    "SELECT * FROM tasks WHERE title = %s",
    (title,)
)
```

---

## ⚠️ Current Limitations

This project is intentionally designed as a simple CLI-based student utility application. Some areas that could be improved include:

- Input validation for dates and numeric values
- More robust exception handling
- Parameterized SQL queries throughout the application
- Better handling of duplicate titles
- A GUI or web interface
- User authentication/profiles
- More detailed expense analytics
- Exporting data to CSV/PDF
- Search functionality for notes
- Sorting and filtering options
- Configuration through environment variables

---

## 🔮 Future Improvements

Possible future versions could include:

- 🖥️ GUI using Tkinter/PyQt
- 🌐 Web version using Flask/Django
- 📊 Expense charts and dashboards
- 🔔 Deadline reminders
- 🔎 Advanced note and task search
- 📤 CSV/PDF data export
- 👥 Multiple student accounts
- 🔐 Secure authentication
- ☁️ Cloud database support
- 📱 Mobile-friendly interface

---

## 🎯 Project Objective

The main goal of the **Student Utility Manager** is to provide students with a simple, centralized tool for managing everyday academic and personal information.

Instead of maintaining separate systems for tasks, notes, expenses, and events, the application brings these utilities together through a single command-line interface backed by a MySQL database.

---

## 👨‍💻 Author

**Yuval Verma**

If you found this project useful, consider ⭐ starring the repository!

---

## 📜 License

This project is available for educational and personal use.

You can add a specific open-source license such as the **MIT License** if you intend to allow broader reuse and distribution.
