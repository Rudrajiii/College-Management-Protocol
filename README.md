# College Management Eco-system
-----------------------------------

## Why This Software ?
> [!NOTE]  
> This is for managing the whole eco-system of a college starting from managing the
> students / teachers through a admin in a single place within a centralized system
> also benefitial for handling serveral kind of stats of students / teachers /etc

## About This Project 
This project is a web-based student management system designed to streamline various administrative tasks for a college. It leverages a combination of modern day web frameworks 
like **"Flask"**

## Technologies Used 💻

### **Backend**
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/flask/flask-original.svg" alt="Flask" width="20"/> **Python (Flask)**: Main Backend Framework of this project.

### **Database**
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original.svg" alt="MongoDB" width="20"/> **MongoDB**: Free instance of MongoDB Cluster (512MB).

### **Frontend**
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="JavaScript" width="20"/> **JavaScript**: For client-side scripting and interactivity.
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sass/sass-original.svg" alt="SCSS" width="20"/> **SCSS & CSS**: For styling the HTML pages.
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" alt="HTML" width="20"/> **HTML & Jinja Templating**: For dynamic data rendering / rendering page content.

### Prerequisites 📚
> [!IMPORTANT] 
> - Python 3.10.* <= 3.11.* <= 3.12.*
> - Flask
> - MongoDB
> - JavaScript , Scss , Bootstrap For Frontend

## Setup & Installation ⚙️

> [!TIP]
> First Fork this repo to make a local copy of this software.
### [1] clone the repo to get the source code:
```bash
git clone https://github.com/Rudrajiii/College-Management-Protocol.git
``` 
### [2] navigate to the directory:
```bash
cd College-Management-Protocol
```
### [3] create a virtual environment:
```bash
python -m venv sysProj
```
### [4] navigate to the newly created virtual environment directory:
```bash
cd sysProj
```
### [5] activate the environment:
```bash
.\Scripts\activate
```
### [6] install all the dependencies:
```bash
pip install -r requirements.txt
```
### [7] run the server:
```bash
python app.py
```

## Project Structure
**Features**
- Admin Dashboard
The admin dashboard manages all staff information, processes data from MongoDB collections, and displays it through a card interface. The dashboard provides an overview of the entire system, ensuring that administrators can efficiently handle student and teacher data.


**MongoDB Database Structure**
Our MongoDB database structure is designed to store and organize data efficiently, supporting the seamless flow of information between different components of the system.
![DB Structure](https://github.com/Rudrajiii/College-Management-Protocol/blob/main/assets/data_models.png?raw=true)

**Data Flow**
The data flow diagram illustrates how student data is managed within the system, showing the routes from admin to students and vice versa. The backend server processes and formats data in JSON for seamless communication.
![DataFlow On Student Dashboard](https://github.com/Rudrajiii/College-Management-Protocol/blob/main/assets/dataflow_on_student_db.png?raw=true)

**Real-Time Notifications**
Notifications are handled using WebSockets for real-time updates. This feature is crucial for applications like teacher leave requests, ensuring that administrators and teachers are promptly informed of any changes.
![Events On Teacher Dashboard](https://github.com/Rudrajiii/College-Management-Protocol/blob/main/assets/events_on_teacher_dsb.png?raw=true)

**Teacher Applications**
The system processes teacher applications in real-time, with features to accept, reject, and send emails using Flask-Mail. Administrators can also clear notifications once actions are taken.
![Teachers Applications Event](https://github.com/Rudrajiii/College-Management-Protocol/blob/main/assets/application_history_strc.png?raw=true)
