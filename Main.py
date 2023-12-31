import openai
import os
import PyPDF2
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap
from datetime import datetime
import requests
from bs4 import BeautifulSoup

load_dotenv()
# Modify the following to be included at the top of the letter
NAME = "Jannis Grimm"
PHONE = "(480) 937-7321"
EMAIL = "jannis@grimm.me"
ADDRESS = "707 S Forest Ave"

def read_pdf(file_path):
    """Reads content from a PDF file using the updated PyPDF2 library."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        return content

def generate_cover_letter(existing_content, resume, company, position, description, url_contents):
    """Generates a tailored cover letter using the OpenAI API."""
    try:
        if url_contents:
            # Automatic approach with URL contents
            user_message = (
                f"Here is the content from the job listing URL it should incldue the company name and position that i am applying to:\n{url_contents}\n\n"
                f"Based on this, please tailor the following cover letter and resume for the job application. "
                f"Here is my existing cover letter:\n{existing_content} "
                f"And here is my resume: \n{resume}\n\n"
                f"Please just slightly tailor this cover letter to the company and position above. The existing cover letters structure and content should be maintained exactly."
                f"Highlight relevant skills and experiences, and ensure the cover letter is engaging and concise."
                f"Don't ever make up anything you don't know about me. "
                f"Keep the letter nice and short and concise. "
                f"My full name at the very end must ALWAYS be on a separate line closing the document"
                f"Make sure to include a blank line every time a new paragraph starts. "
                f"Make sure it is the best cover letter ever so that they instantly want to hire me. And make sure it is complete as in ready to submit as is."
                f"Do not include contact information"
            )
        else:
            # Manual approach with individual details
            user_message = (
                f"Here is my existing cover letter:\n{existing_content} "
                f"Here is my resume: \n{resume}\n\n"
                f"Here is the role's description: \n{description}\n"
                f"Please slightly tailor this cover letter for a {position} position at {company}. "
                f"Never just list skills or talk about technology too much. Be confident. "
                f"Highlight my American dream and what sets me apart. "
                f"Don't ever make up anything you don't know about me. "
                f"Keep the letter nice and short and concise. "
                f"Make sure to include a blank line every time a new paragraph starts. "
                f"Make sure it is the best cover letter ever so that they instantly want to hire me."
            )

        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You just tailor cover letters. You never exceed 320 words."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message['content']

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_webpage_content(url):
    """Fetches the content of a webpage given its URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return ""

def save_to_pdf(content, filename):
    """Saves the tailored content to a PDF file with a clean and professional layout for a cover letter, including proper paragraph separation."""
    downloads_path = os.path.expanduser('~/Downloads')
    full_path = os.path.join(downloads_path, filename)

    # Setup PDF document
    c = canvas.Canvas(full_path, pagesize=letter)
    c.setFont("Times-Roman", 12)

    # Margin and starting position adjustments
    margin = 72  # One inch margin
    width, height = letter  # Page size
    x = margin  # Horizontal start
    y = height - margin  # Vertical start (top of the page minus margin)

    current_date = datetime.now().strftime("%m/%d/%Y")

    # Header content with smaller line height
    header_line_height = 14
    header_content = f"{NAME}\n{PHONE}\n{EMAIL}\n{ADDRESS}\n{current_date}\n\n"
    for line in header_content.split('\n'):
        c.drawString(x, y, line)
        y -= header_line_height

    # Regular content with standard line height
    line_height = 16
    paragraph_spacing = 10

    paragraphs = content.split('\n\n')  # Splitting content into paragraphs
    for paragraph in paragraphs:
        wrapped_text = textwrap.fill(paragraph, width=90)
        for line in wrapped_text.split('\n'):
            if y < margin + line_height:
                c.showPage()
                c.setFont("Times-Roman", 12)
                y = height - margin
            c.drawString(x, y, line)
            y -= line_height
        y -= paragraph_spacing

    c.save()
    print(f"Tailored content saved as PDF at {full_path}")


def main():
    """Main function to run the script."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("The OpenAI API key is not set. Please set it as an environment variable.")

    url = input("Enter the URL of the job posting or type 'NO' for manual entry: ")

    if url.strip().lower() != 'no':
        cover_letter_content = read_pdf("coverletter.pdf")
        resume_content = read_pdf("resume.pdf")

        print("Generating tailored cover letter... Please wait.")
        url_contents = fetch_webpage_content(url)

        tailored_cover_letter = generate_cover_letter(cover_letter_content, resume_content, "COMPANY", "POSITION", "DESCRIPTION", url_contents)
    else:
        # Manual entry of details
        company = input("Enter the company's name: ")
        position = input("Enter the position you're applying for: ")
        print("Enter the description of the role (type 'END' when finished):")
        description_lines = []
        while True:
            line = input()
            if line.strip().lower() == 'end':
                break
            description_lines.append(line)
        description = "\n".join(description_lines)

        cover_letter_content = read_pdf("coverletter.pdf")
        resume_content = read_pdf("resume.pdf")

        print("Generating tailored cover letter... Please wait.")
        tailored_cover_letter = generate_cover_letter(cover_letter_content, resume_content, company, position, description, "")

    current_date = datetime.now().strftime("%s-%h-%m-%d-%Y")
    print("Cover letter generation complete.")
    save_to_pdf(tailored_cover_letter, f"CoverLetter_{company if url.lower() == 'no' else current_date}.pdf")
    print(f"Cover letter saved as 'CoverLetter_{company if url.lower() == 'no' else current_date}.pdf")

if __name__ == "__main__":
    main()
