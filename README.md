# Student Management -2.0

## Overview
This project is a web-based student management system designed to streamline various administrative tasks for a college. It leverages a combination of HTML, CSS, JavaScript, Flask, and MongoDB to provide a robust and interactive user experience.

## Features
- **Student Registration**: Allows students to register with their personal details.
- **Student Management**: Admins can view, edit, and delete student records.
- **Authentication**: Secure login system for both students,teachers and admins.
- **Dashboard**: Provides an overview of student,teacher and admin statistics and other relevant data.
- **Responsive Design**: Ensures usability across different devices and screen sizes.

## Technologies Used
- **HTML**: For structuring the web pages.
- **CSS**: For styling the web pages.
- **JavaScript**: For client-side scripting and interactivity.
- **Flask**: As the web framework for building the backend.
- **MongoDB**: As the database for storing student records.

## Installation

### Prerequisites
- Python 3.x
- Flask
- MongoDB
- Node.js (for managing JavaScript dependencies, if any)

### Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Rickyy-Sam07/student_management_app2.0.git
    cd student-management-website
    ```

2. **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```



3. **Set Up MongoDB**
    - Ensure MongoDB is installed and running.
    - Update the MongoDB connection string in the Flask app configuration if necessary.

4. **Run the Application**
    ```bash
    flask run
    ```
5. **Access the Application**
    Open your web browser and go to `http://127.0.0.1:5000`.

## Project Structure
