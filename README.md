# StackConnect

StackConnect is a **Django** web application designed to replicate and extend the core functionalities of Stack Overflow, enabling users to ask questions, post answers, vote, and interact seamlessly. It leverages the **Django REST Framework** for robust API endpoints, **Celery** and **RabbitMQ** for scalable asynchronous processing, and integrates modern UI elements with **Tailwind CSS**.

## Screenshots
<img width="450" height="430" alt="image" src="https://github.com/user-attachments/assets/42061b77-c3cd-4eec-bc37-ceb740558a91" />
<img width="450" height="480" alt="image" src="https://github.com/user-attachments/assets/2ada0f65-56e7-429e-b4a7-fc2c8eb5d528" />
<img width="450" height="400" alt="image" src="https://github.com/user-attachments/assets/bab66739-2385-4e90-9e7b-f376f7e48304" />
<img width="450" height="400" alt="image" src="https://github.com/user-attachments/assets/ae9d8e1e-a15e-4d7b-8c86-fd6db5b7e1a9" />
<img width="450" height="450" alt="image" src="https://github.com/user-attachments/assets/11900fcf-49bd-4e6f-90ca-23238b30a770" />




## Features

- **Ask, Answer, and Vote**: Create and solve programming questions in a familiar Stack Overflow-like environment
- **OAuth 2.0 Authentication**: Secure user authentication via the Stack Exchange API for a seamless login experience
- **Asynchronous Email & Tasks**: Improve system responsiveness with Celery and RabbitMQ handling emails and background operations
- **Modern Frontend**: User interface styled using Tailwind CSS for flexibility and speed
- **API-First**: RESTful endpoints support integrations, mobile apps, and automation workflows

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: Tailwind CSS
- **Asynchronous Processing**: Celery, RabbitMQ
- **Database**: SQLite (default, easily switchable)
- **Authentication**: OAuth 2.0 via Stack Exchange API
- **Testing**: Postman for API testing

## Project Structure

```
stackconnect/
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── content/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── qna/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── templates/
├── db.sqlite3
├── manage.py
├── Procfile
├── README.md
└── requirements.txt
```

## Setup & Installation

### Prerequisites

- Python 3.8+
- RabbitMQ server (for Celery)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/<yourusername>/stackconnect.git
   cd stackconnect
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Create a `.env` file in the root directory
   - Add the necessary OAuth credentials for Stack Exchange API:
   ```env
   API_KEY= ""
   CLIENT_ID= ""
   CLIENT_SECRET= ""
   EMAIL = ""
   PASSWORD = ""
   SECRET_KEY = ""
   ```

5. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Start Celery worker** (in a separate terminal)
   ```bash
   celery -A qna worker -l info
   ```

9. **Start RabbitMQ server**
   - Ensure RabbitMQ server is running locally or configure remote connection in settings

## Usage

- **Frontend Access**: Navigate to `http://localhost:8000/` to access the web interface
- **Admin Panel**: Access Django admin at `http://localhost:8000/admin/`
- **API Testing**: Use Postman or any API client to test endpoints
- **Authentication**: Register and login with Stack Exchange OAuth for secure access
- **Core Features**: 
  - Post questions and submit answers through the web interface
  - Vote on questions and answers
  - Background tasks (emails, notifications) are handled asynchronously

## API Endpoints

The application provides RESTful API endpoints for:
- User authentication and management
- Question CRUD operations
- Answer management
- Voting system
- User profiles and statistics

*Note: Detailed API documentation and Postman collections are available for testing and integration.*

**Built with ❤️ using Django and modern web technologies**
