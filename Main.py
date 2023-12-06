import openai
import os
import PyPDF2
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap
from datetime import datetime

# Load environment variables
load_dotenv()

NAME = ""
PHONE = ""
EMAIL = ""
ADDRESS = ""

def read_pdf(file_path):
    """Reads content from a PDF file using the updated PyPDF2 library."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        return content

def generate_cover_letter(existing_content, resume, company, position, description):
    """Generates a tailored cover letter using the OpenAI API."""

    try:
        # Adjust the parameters as needed for your specific use case
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You just tailor cover letters. You never exceed 310 words."},
                {"role": "user",
                 "content":
                      f"Here is my existing cover letter:\n{existing_content} "
        f"Here is my resume: \n{resume}\n\n"
        f"Here is the roles description: \n{description}"
        f"Please slightly tailor this cover letter for a {position} position at {company}."
        f"Never just list skills or talk about technology too much. Be confident."
        f"Highlight my american dream and what sets me apart."
        f"Don't ever make up anything you dont know about me."
        f"Keep the letter nice and short and concise."
        f"Make sure to include a blank line everytime a new paragraph starts."
                      f"Make sure it is the best cover letter ever so that they instantly want to hire me."
                 }

            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




def save_to_pdf(content, filename):
    """Saves the tailored content to a PDF file with a clean and professional layout for a cover letter, including proper paragraph separation."""
    downloads_path = os.path.expanduser('~/Downloads')
    full_path = os.path.join(downloads_path, filename)

    # Setup PDF document
    c = canvas.Canvas(full_path, pagesize=letter)
    c.setFont("Times-Roman", 12)  # Professional font choice

    # Margin and starting position adjustments
    margin = 72  # One inch margin
    width, height = letter  # Page size
    x = margin  # Horizontal start
    y = height - margin  # Vertical start (top of the page minus margin)

    # Generate current date
    current_date = datetime.now().strftime("%m/%d/%Y")

    # Header content with smaller line height
    header_line_height = 14
    header_content = f"{NAME}\n{PHONE}\n{EMAIL}\n{ADDRESS}\n{current_date}\n\n"
    for line in header_content.split('\n'):
        c.drawString(x, y, line)
        y -= header_line_height  # Use smaller line height for header

    # Regular content with standard line height
    line_height = 16  # Line height for better readability
    paragraph_spacing = 10  # Extra space between paragraphs

    paragraphs = content.split('\n\n')  # Splitting content into paragraphs
    for paragraph in paragraphs:
        wrapped_text = textwrap.fill(paragraph, width=90)  # Wrap each paragraph
        for line in wrapped_text.split('\n'):
            if y < margin + line_height:  # Check for new page
                c.showPage()
                c.setFont("Times-Roman", 12)
                y = height - margin
            c.drawString(x, y, line)
            y -= line_height
        y -= paragraph_spacing  # Add extra space after each paragraph

    c.save()
    print(f"Tailored content saved as PDF at {full_path}")


def main():
    """Main function to run the script."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("The OpenAI API key is not set. Please set it as an environment variable.")

    # User inputs
    company = input("Enter the company's name: ")
    position = input("Enter the position you're applying for: ")
    # Read multiline description
    print("Enter the description of the role (type 'END' when finished):")
    description_lines = []
    while True:
        line = input()
        if line.strip().lower() == 'end':  # End input on 'END'
            break
        description_lines.append(line)
    description = "\n".join(description_lines)

    # Read existing cover letter and resume (PDF)
    cover_letter_content = read_pdf("coverletter.pdf")
    resume_content = read_pdf("resume.pdf")

    print("Generating tailored cover letter... Please wait.")
    # Generate tailored cover letter
    tailored_cover_letter = generate_cover_letter(cover_letter_content, resume_content, company, position, description)
    print("Cover letter generation complete.")
    save_to_pdf(tailored_cover_letter, f"CoverLetter{company}.pdf")
    print(f"Cover letter saved as 'CoverLetter_{company}.pdf'")

if __name__ == "__main__":
    main()
