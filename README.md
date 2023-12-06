# Automated Cover Letter Generator

This Python script automatically tailors cover letters for specific job applications using the OpenAI GPT-4 API. It reads existing cover letters and resumes in PDF format, generates a customized cover letter based on a job description, and saves the final version as a new PDF.

## Features

- Reads existing cover letter and resume in PDF format.
- Tailors the cover letter based on the url of the job descrioption or user inputs for the company name, position, and job description.
- Utilizes OpenAI's GPT-4 model for intelligent and context-aware text generation.
- Saves the tailored cover letter as a PDF with a professional layout.

## Setup

### Prerequisites

- Python 3.x
- Install required Python libraries: `openai`, `PyPDF2`, `python-dotenv`, `reportlab`, 'bs4'

You can install these with the following command:

```bash
pip install openai PyPDF2 python-dotenv reportlab bs4
```
### Environment Variables
Set up an environment variable for the OpenAI API key. You can get an API key by signing up at OpenAI.

### Configuration
Clone or download this repository to your local machine.
Open the script and fill in your personal details (NAME, PHONE, EMAIL, ADDRESS) at the top of the script.
Create a .env file in the root of the project and add your OpenAI API key:
```plaintext
OPENAI_API_KEY=Your_OpenAI_API_Key_Here
```
## Usage

Place your existing cover letter and resume in PDF format in the same directory as the script, or adjust the file paths in the main function.
Run the script:
```bash
python main.py
```
Follow the prompts in the command line to input the company's name, the position you're applying for, and the job description or simply paste the link where the position is listed for automatic entry.
The script will generate a tailored cover letter and save it as a PDF in your Downloads folder or the specified path.

## Customization

Modify the script to change the PDF formatting, line spacing, and other parameters.
Update the generate_cover_letter function to change how the cover letter is tailored.

## Note

This tool is intended for personal use. Ensure compliance with OpenAI's usage policies and the terms of service of any job posting websites you may scrape for job descriptions.

## Contributing

Contributions to improve this tool are welcome. Please feel free to fork the repository and submit pull requests.

## License

Distributed under the MIT License. See LICENSE for more information.


This README provides a comprehensive guide covering features, setup instructions, usage steps, customization options, and contribution guidelines, making it easier for users to understand and use your tool effectively.
