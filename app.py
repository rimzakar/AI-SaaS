from flask import Flask, render_template, request, jsonify
import os
import requests
from bs4 import BeautifulSoup as bs
from openai import OpenAI
import PyPDF2

def get_job_description(url):
    # Send a GET request to the website
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:

        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = bs(page_content, 'html.parser')

        # Find the job description <div class="gtm-apply-clicks description description--jobentry">
        job_description = soup.select_one('div.description')

        # If the job description is found, return it
        if job_description:
            return job_description.get_text().strip()
        else:
            print("Job description not found")
            print("assuming that the job description is the longest line")
            # extract the text content
            text_content = soup.get_text()
            # split the text into lines
            lines = text_content.splitlines()

            # strip empty lines and extra whitespace
            lines = [line.strip() for line in lines if line.strip()]

            longest_line = max(lines, key=len)
            return longest_line
    else:
        print("Failed to retrieve the webpage")
        return None

def get_api_key():
    #read api key from file
    with open("apiKey.txt", "r") as f:
        api_key = f.read().strip()
    return api_key

def extract_pdf_text(file_path):
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def generate_cover_letter(url, pdf_path):
    # Initialize OpenAI client
    client = OpenAI(api_key=get_api_key())

    # Extract text from the PDF
    try:
        pdf_text = extract_pdf_text(pdf_path)
    except Exception as e:
        # Handle the error
        return f"Error extracting text from PDF: {e}"

    """
    # Save the pdf txt
    with open("pdf_text.txt", "w", encoding="utf-8") as f:
        f.write(pdf_text)
    """
    job_description = get_job_description(url)

    if job_description is None:
        return "No job description was provided. Please check the URL and try again."
    else:
        prompt1 = f"""Analyze the following job description and provide the key points:
                    1. Detect the language and respond in English.
                    2. Summarize key requirements, skills, and tasks mentioned in the description.

                    Job Description: {job_description}
                    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": prompt1}
        ]
    )

    # Get the response to the first message
    response_to_first_message = completion.choices[0].message

    # Construct the second message using the response to the first message
    prompt2 = f"""Based on the following details:
                1. Key points extracted from the job description: {response_to_first_message}
                2. The applicant's CV: {pdf_text}

                Write a formal, concise, and personalized cover letter tailored to this job. Highlight relevant skills, experiences, and accomplishments, ensuring alignment with the job requirements. Use professional yet approachable language.
                """

    # Send the second message
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": prompt2}
        ]
    )

    """
    # Save the new cover letter
    with open("coverLetter.txt", "w", encoding="utf-8") as f:
        f.write(completion.choices[0].message.content)

    print("Done")
    """
    return completion.choices[0].message.content

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    url = request.form.get('url')
    file = request.files.get('file')

    if not url or not file:
        return jsonify({'error': 'Missing URL or PDF file.'}), 400

    # Save the PDF file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Call your function f
    result = generate_cover_letter(url, file_path)

    # Return the result
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)