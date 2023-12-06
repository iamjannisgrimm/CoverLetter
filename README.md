# AI-Enhanced Cover Letter Generator

## Introduction
This AI-Enhanced Cover Letter Generator is a Python-based tool that allows users to automatically tailor their existing cover letters and resumes for specific job applications using OpenAI's GPT-3 API. It provides a convenient way to personalize job application materials, enhancing your chances of landing your desired job.

## Features
- Customize existing cover letters and resumes for specific companies and positions.
- Generate professional-looking PDFs with tailored content.
- User-friendly interface for inputting job application details.

## Prerequisites
Before you start using this tool, make sure you have the following:
- Python 3.8 or higher installed on your system.
- An active OpenAI API key. [Sign up here](https://openai.com/api/) if you don't have one.
- `PyPDF2` and `ReportLab` libraries installed. Use `pip install PyPDF2 reportlab` to install them.

## Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/ai-cover-letter-generator.git

## Usage

1. Place your existing cover letter and resume (PDF format) in the project directory. Name them `coverletter.pdf` and `resume.pdf`.
2. Set your OpenAI API key as an environment variable:
   - **Windows**: `set OPENAI_API_KEY=your_api_key`
   - **macOS/Linux**: `export OPENAI_API_KEY=your_api_key`
3. Run the script:
   ```bash
   python main.py


You can modify the script to change the PDF formatting, font size, or line spacing as per your preference.
The script can be extended to include more dynamic content generation based on different templates or styles.
Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your enhancements.

