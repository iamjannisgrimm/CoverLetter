import openai
import os
import PyPDF2
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

# Load environment variables
load_dotenv()

def read_pdf(file_path):
    """Reads content from a PDF file using the updated PyPDF2 library."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        return content

def generate_cover_letter(existing_content, resume, company, position):
    """Generates a tailored cover letter using the OpenAI API."""
    prompt = (
        f"Here is my existing cover letter:\n{existing_content} "
        f"and here is my resume: \n{resume}\n\n"
        f"Please tailor this cover letter for a {position} position at {company}."
    )

    response = openai.Completion.create(
        engine="text-davinci-003",  # or another model
        prompt=prompt,
        max_tokens=1000
    )
    return response.choices[0].text.strip()

def save_to_pdf(content, filename):
    """Saves the tailored content to a PDF file with improved formatting."""
    downloads_path = os.path.expanduser('~/Downloads')  # Adjust for Windows if necessary
    full_path = os.path.join(downloads_path, filename)

    # Setup PDF document
    c = canvas.Canvas(full_path, pagesize=letter)
    c.setFont("Helvetica", 11)  # Standard font choice

    # Margin and starting position adjustments
    margin = 72  # One inch margin
    width, height = letter  # Page size
    x = margin  # Horizontal start
    y = height - margin  # Vertical start (top of the page minus margin)

    # Handling line wrapping and spacing
    line_height = 14  # Line height
    wrapped_text = textwrap.fill(content, width=60)  # Adjust the width as needed

    for line in wrapped_text.split('\n'):
        # Check for new page
        if y < margin:  # Margin of 1 inch
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - margin

        # Write the line and move to next line
        c.drawString(x, y, line)
        y -= line_height  # Adjust line height

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

    # Read existing cover letter and resume (PDF)
    cover_letter_content = read_pdf("coverletter.pdf")
    resume_content = read_pdf("resume.pdf")

    # Generate tailored cover letter
    tailored_cover_letter = generate_cover_letter(cover_letter_content, resume_content, company, position)
    save_to_pdf(tailored_cover_letter, "tailored_cover_letter.pdf")

if __name__ == "__main__":
    main()
