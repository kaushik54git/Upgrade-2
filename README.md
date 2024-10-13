# Upgrade
## Overview
This project is a Recommender System aimed at improving students' learning experiences by using the ML-KNN (Multi-Label K-Nearest Neighbor) algorithm. It provides personalized recommendations to students based on their learning patterns and performance 📊. The system is built with a Flask front-end and MongoDB as the database for managing student and course data.
## Features
- **User-friendly Dashboard:** Separate dashboards for teachers and students.
- **Course and Student File Upload:** Teachers can upload student and course data to generate tailored recommendations.
- **Personalized Learning Recommendations:** Uses the ML-KNN algorithm to provide suggestions based on student performance.
- **Secure Authentication:** Secure login system for teachers.
## Tech Stack
- Backend: Flask (Python)
- Front-end: HTML, CSS, JavaScript
- Database: MongoDB (Cloud-based using Azure Cosmos DB)
- Algorithm: ML-KNN (Multi-Label K-Nearest Neighbor)
## Set Up Instructions
### Prerequisites
Python 3.8+
Flask
MongoDB Atlas or MongoDB Server
Other dependencies listed in requirements.txt
### Installation and Setup
1. Clone the repository:
```bash
git clone https://github.com/Nehal-Khan-29/Upgrade-2
```
2. Navigate to the project directory:
```bash
cd Upgrade-2
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Configure MongoDB connection in the app.py file:
```python
mongo_client = MongoClient('your_mongo_connection_string')
```
5. Run the application:
```bash
flask run
```
6. Open your browser and go to:
```arduino
http://127.0.0.1:5000
```
## Project Structure
```graphql
UPGRADE/
│
├── static/
│   ├── class_analysis.css
│   ├── class_analysis.png
│   ├── find_stud_recom.png
│   ├── find_student_recommendations.css
│   ├── login.css
│   ├── main_page.png
│   ├── student_analysis.css
│   ├── student_analysis.png
│   ├── student_dashboard.css
│   ├── student_dashboard.png
│   ├── teacher_dashboard.css
│   ├── teacher_dashboard.png
│   ├── teacher_login.png
│   └── teacherlogin.css
│
├── templates/
│   ├── class_analysis.html
│   ├── find_student_recommendations.html
│   ├── login.html
│   ├── student_analysis.html
│   ├── student_dashboard.html
│   ├── teacher_dashboard.html
│   └── teacherlogin.html
│
├── Courses_19cse301.xlsx
├── Students_19cse301.xlsx
└── app.py
```
## Screenshots
![image](https://github.com/user-attachments/assets/834cb77d-bf06-4a78-b022-079165ec6f08)
![image](https://github.com/user-attachments/assets/7c8fb6ad-672c-47ce-9572-527a7353c36d)
![image](https://github.com/user-attachments/assets/b2960843-e7bf-4bfe-b11b-873caad9528e)
![image](https://github.com/user-attachments/assets/f2e62760-afb1-4f27-9d9f-8693a3472109)
![image](https://github.com/user-attachments/assets/13e32b0b-0068-47e4-85ce-2c9915cda563)
![image](https://github.com/user-attachments/assets/7c57430d-230f-460c-9a05-43c818dc3f25)
![image](https://github.com/user-attachments/assets/36f4e78d-b11f-4f81-b163-8e496973c6f2)

## License
This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.

