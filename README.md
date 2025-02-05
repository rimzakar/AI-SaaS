# Flask Cover Letter Generator
This is a Flask-based web application that generates a personalized cover letter based on a job description URL and a user's resume (PDF). The application uses OpenAI's GPT-4 model to analyze the job description and the resume, and then generates a tailored cover letter.
## Features
-  **Job Description Extraction**: The application extracts the job description from a provided URL.
-  **Resume Parsing**: The application parses the text from a user-uploaded PDF resume.
-  **Cover Letter Generation**: Using OpenAI's GPT-4 model, the application generates a personalized cover letter based on the job description and resume.
## Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.x
  - https://www.python.org/downloads/ 
- Flask
- requests
- BeautifulSoup
- PyPDF2
- OpenAI

You can install the required Python packages using the following command:
```bash

pip  install  flask  requests  beautifulsoup4  PyPDF2  openai

```
## Setup
- Clone the Repository:
```bash
git  clone  https://github.com/yourusername/flask-cover-letter-generator.git
cd  flask-cover-letter-generator
```
- Set Up OpenAI API Key:
- Create a file named apiKey.txt in the root directory of the project.
- Paste your OpenAI API key into this file.
  - https://platform.openai.com
- Run the Application:
```bash
python  app.py
```
The application will start running on http://127.0.0.1:5000/
## Usage
-  **Access the Web Interface**:
    Open your web browser and navigate to `http://127.0.0.1:5000/`.
-  **Enter Job URL and Upload Resume**:
    -   Enter the URL of the job description in the provided field.
    -   Upload your resume in PDF format.
-  **Generate Cover Letter**:
    -   Click the "Submit" button to generate the cover letter.
    -   The generated cover letter will be displayed in the "Function Output" text area.
-  **Reset Form**:
    -   Click the "Reset" button to clear the form and start over.