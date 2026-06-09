# Health-Prediction-Application
An AI-powered web platform built with Django that securely logs patient health data (Glucose, Haemoglobin, Cholesterol) and uses the Hugging Face `google/flan-t5-base` model to predict and categorize clinical metabolic risks (Low, Moderate, High).

The platform includes a robust patient log management subsystem, supporting full CRUD features (Create, Read, Update, Delete) with persistent storage and local logic safe-fallbacks if remote network APIs disconnect.

---

## 🛠️ Tech Stack & Requirements
* **Language:** Python 3.12.3+
* **Framework:** Django 6.0.6
* **Database:** SQLite3 (Default relational engine)
* **API Integration:** Hugging Face Inference API (`google/flan-t5-base`)
* **Styling Framework:** Bootstrap 5 (via CDN integration)

---

## 🚀 Step-by-Step Installation & Setup

Follow these exact terminal operations to get your local development server running seamlessly:

### 1. Clone the Project & Navigate In
```bash

cd "C:\Users\raman\PycharmProjects\Health prediction Application"

2. Create and Activate the Python Virtual Environment
Bash
# Create the environment
python -m venv .venv

# Activate it on Windows (Command Prompt)
.venv\Scripts\activate
3. Install Required Dependencies
Using the provided packages manifest file, compile your environments:

Bash
pip install -r requirements.txt
4. Configure Your Environment Variables (.env)
Create a file named .env in your root directory (next to manage.py) to keep your private authentication credentials hidden securely from version control history:

Code snippet
HUGGINGFACE_API_KEY=your_actual_huggingface_inference_api_token_here
5. Apply Database Migrations
Create your local database tables structured around registration profiles and physiological record indices:

Bash
python manage.py makemigrations
python manage.py migrate
6. Boot Up the Development Server
Bash
python manage.py runserver
Your application will be live at http://127.0.0.1:8000/.
