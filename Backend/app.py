from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from vw import run_test_generation_pipeline
import os
from docx import Document
from testing import load_test_cases, execute_test_cases
import sys
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/generate-tests', methods=['POST'])
def generate_tests():
    try:
        # Get the website URL and document text from the form data
        website_url = request.form.get('websiteUrl')
        document_text = request.form.get('documentText')

        def text_to_docx(text, file_name):
            # Create a new Document
            doc = Document()

            # Add text to the Document
            doc.add_paragraph(text)

            # Save the Document
            doc.save(file_name)
        
        # Convert text to DOCX file
        text_to_docx(document_text, os.path.join(app.config['UPLOAD_FOLDER'], 'output.docx'))
        run_test_generation_pipeline(os.path.join(app.config['UPLOAD_FOLDER'], 'output.docx'),output_dir='.',gemini_key="AIzaSyACIHFbDY5ty8BUR7BhPAP7ibdHHC6aUOc")

        import argparse
        parser = argparse.ArgumentParser(description="Run automated Playwright tests")
        parser.add_argument("--test-file", default="playwright_tests.json", help="Path to test cases JSON file")
        parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
        parser.add_argument("--timeout", type=int, default=5000, help="Timeout in milliseconds")
        parser.add_argument("--retries", type=int, default=2, help="Number of retries for failed tests")
        parser.add_argument("--base-url", default=website_url, help="Base URL for tests")
        args = parser.parse_args()
    
        # Load and execute test cases
        print(f"🚀 Starting automated test execution")
        print(f"📋 Loading test cases from: {args.test_file}")
        test_cases = load_test_cases(args.test_file)

        if test_cases and args.base_url:
            print(f"🌐 Base URL: {args.base_url}")
            for test in test_cases.get("tests", []):
                # If the first step isn't navigate, add it
                if not test["steps"] or test["steps"][0]["action"] != "navigate":
                    test["steps"].insert(0, {
                        "action": "navigate",
                        "value": args.base_url
                    })
                # If the first step is navigate but has no value or needs to be prefixed
                elif test["steps"][0]["action"] == "navigate":
                    # If value is empty or a relative path
                    if not test["steps"][0].get("value") or not test["steps"][0]["value"].startswith(("http://", "https://")):
                        # For empty value, use base URL directly
                        if not test["steps"][0].get("value"):
                            test["steps"][0]["value"] = args.base_url
                        # For relative paths, combine with base URL
                        else:
                            relative_path = test["steps"][0]["value"]
                            base = args.base_url.rstrip('/')
                            test["steps"][0]["value"] = f"{base}/{relative_path.lstrip('/')}"
        
            if test_cases:
                success = execute_test_cases(
                    test_cases, 
                    headless=args.headless, 
                    timeout=args.timeout,
                    retries=args.retries
                )
                
        

        if __name__ == "__main__":
            text = document_text
            file_name = "output.docx"
            text_to_docx(text, file_name)
            print(f"Text has been converted to {file_name}")

        # Process attached files
        attached_files = []
        for file_key in request.files:
            file = request.files[file_key]
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            attached_files.append(filename)

        # Mock test generation logic
        test_results = {
            "websiteUrl": website_url,
            "documentText": document_text,
            "attachedFiles": attached_files,
            "generatedTests": [
                {
                    "testName": "Test Home Page Load",
                    "description": "Verify that the home page loads successfully.",
                    "status": "Pending"
                },
                {
                    "testName": "Test Login Functionality",
                    "description": "Verify that the login functionality works as expected.",
                    "status": "Pending"
                }
            ]
        }

        # Return the generated test results as JSON
        return jsonify(test_results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)