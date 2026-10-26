# Health Prediction Application

A Django-based web application that manages patient blood test records and integrates with the **Google Gemini AI API** to predict potential health risks based on Glucose, Haemoglobin, and Cholesterol levels.

This project was built as a submission for the **AI Growth & Automation Associate - Task 2 (Python Skills Evaluation)**.

## 🚀 Features

*   **Full CRUD Operations:** Create, Read, Update, and Delete patient records.
*   **AI Integration:** Uses Google Gemini API (`google-genai` SDK) to generate clinical risk assessments in the "Remarks" field.
*   **Robust Data Validation:** 
    *   Ensures Date of Birth is valid and in the past (catches impossible dates like `31/11/2001` and future dates).
    *   Validates email formats.
    *   Prevents exact duplicate records from being saved.
    *   Ensures blood test values are numeric.
*   **Responsive UI:** Built with Bootstrap 5, featuring a sticky table header, scrollable data container, and a clean dashboard layout.
*   **Persistent Storage:** Uses SQLite database to store records permanently.
*   **Bulk AI Refresh:** A custom dashboard button to re-trigger the AI prediction for all records at once.

## 🛠️ Tech Stack

*   **Backend:** Python 3, Django 5
*   **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
*   **AI API:** Google Gemini (`google-genai`)
*   **Database:** SQLite

## ⚙️ Local Setup Instructions

To run this project locally, follow these steps:

**1. Clone the repository**
```bash
git clone https://github.com/Ramana013/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
2. Create and activate a virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies

bash
pip install -r requirements.txt
4. Set up Environment Variables
Create a .env file in the root directory (alongside manage.py) and add your Gemini API Key:

env
GEMINI_API_KEY=your_gemini_api_key_here
(Note: You can get a free key from Google AI Studio).

5. Run Database Migrations

bash
python manage.py makemigrations
python manage.py migrate
6. Start the Development Server

bash
python manage.py runserver
Open your browser and go to http://127.0.0.1:8000/

