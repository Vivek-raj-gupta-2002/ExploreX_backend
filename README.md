# ExploreX
ExploreX is a mental health app designed to enhance emotional well-being through AI-driven features and user-focused solutions. The app provides personalized personality analysis, mood tracking, and tailored task suggestions to help users manage their mental health effectively. With an anonymous chat feature, it creates a safe and supportive environment for users to express themselves freely. Built using React Native for a seamless interface, Django and Django REST Framework for a robust backend, and PostgreSQL for efficient data management, ExploreX combines advanced technology with practical utility. The app was tested with real users, showcasing its potential to make a meaningful impact on mental wellness.


# ExploreX Backend

The backend system for the **ExploreX** application, designed to provide API services, real-time chat features, and data management for user self-awareness and analytics.

## Features
- **API Services**: Backend APIs for user authentication, profile management, and activity tracking.
- **Real-time Chat**: Implements one-on-one real-time chat functionality.
- **Data Management**: Robust mechanisms to store and manage user data.
- **Integration**: Seamlessly integrates with the ExploreX frontend for enhanced user experience.

## Tech Stack
- **Backend Framework**: Django
- **Real-time Communication**: Django Channels/WebSocket
- **Database**: SQLite/PostgreSQL
- **Authentication**: Google Sign-In
- **Environment Management**: Python `venv`
- **Package Management**: pip

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Vivek-raj-gupta-2002/exploreX_backend.git
   ```
2. Navigate to the project directory:
   ```bash
   cd exploreX_backend
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure
- `AgentApp/`: Handles AI-powered features.
- `apiApp/`: Manages APIs for user-related functionalities.
- `chatApp/`: Implements chat features with Django Channels.
- `MySite/`: Core Django project settings.
- `utils/`: Contains utility scripts for various backend operations.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with detailed descriptions of your changes.
