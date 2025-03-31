import json
import re
import os
from docx import Document
import google.generativeai as genai
import time

# Configuration
GEMINI_MODEL = 'gemini-2.0-flash-lite'
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def parse_requirements(doc_path, output_dir="."):
    """Parse requirements from a Word document and save them as JSON."""
    try:
        # Validate input path
        if not os.path.exists(doc_path):
            raise FileNotFoundError(f"Document not found: {doc_path}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Parse requirements from Word doc
        doc = Document(doc_path)
        requirements = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
        # Save requirements as JSON
        requirements_path = os.path.join(output_dir, "requirements.json")
        with open(requirements_path, "w", encoding="utf-8") as f:
            json.dump({"requirements": requirements}, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Requirements JSON generated: {requirements_path}")
        return requirements_path
    
    except Exception as e:
        print(f"❌ Error parsing requirements: {e}")
        return None

def call_gemini_api(model, prompt, gemini_key):
    """Call Gemini API with simple retry logic."""
    if not gemini_key or gemini_key == "YOUR_GEMINI_API_KEY":
        raise ValueError("❌ Invalid Gemini API key. Please provide a valid key.")
    
    for attempt in range(MAX_RETRIES):
        try:
            # Configure API
            genai.configure(api_key=gemini_key)
            gen_model = genai.GenerativeModel(model)
            
            # Make API call
            response = gen_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"⚠️ API error on attempt {attempt+1}/{MAX_RETRIES}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                raise
    
    # Should never reach here due to the raise in the loop
    raise Exception("Failed all API call attempts")

def extract_json_from_text(text):
    """Extract and validate JSON from text response."""
    try:
        # Find JSON-like content in the text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON content found in the response")
        
        json_str = match.group(0)
        
        # Validate JSON
        return json.loads(json_str)
    
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        print(f"🔍 Raw JSON string: {text}")
        raise ValueError("Invalid JSON in the response")

def generate_functionality_testplan(requirements_path, output_dir=".", gemini_key=None):
    """Generate a test plan based on requirements JSON file."""
    if not gemini_key:
        raise ValueError("Gemini API key is required")
    
    try:
        # Read the requirements JSON file
        with open(requirements_path, "r", encoding="utf-8") as f:
            requirements_data = json.load(f)
        
        # Construct prompt for Gemini
        requirements_text = "\n".join(requirements_data.get("requirements", []))
        prompt = f"""
        Based on these requirements:
        {requirements_text}

        Generate a comprehensive test plan that includes:
        1. Core functionality test cases
        2. Edge case test cases
        3. Security and performance considerations

        Format the output as JSON with the following structure:
        {{
            "core_tests": [
                {{ "description": "test description", "expected_result": "expected result" }}
            ],
            "edge_cases": [
                {{ "description": "test description", "expected_result": "expected result" }}
            ],
            "security_tests": [
                {{ "description": "test description", "expected_result": "expected result" }}
            ],
            "performance_tests": [
                {{ "description": "test description", "expected_result": "expected result" }}
            ]
        }}
        Only return valid JSON with no additional text.
        """
        
        # Call Gemini API
        print("📤 Sending test plan generation request to Gemini API...")
        response_text = call_gemini_api(GEMINI_MODEL, prompt, gemini_key)
        
        # Process response
        print("📥 Processing Gemini API response...")
        test_plan_data = extract_json_from_text(response_text)
        
        # Save test plan as JSON
        test_plan_path = os.path.join(output_dir, "test_plan.json")
        with open(test_plan_path, "w", encoding="utf-8") as f:
            json.dump(test_plan_data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Test plan JSON generated: {test_plan_path}")
        return test_plan_path
    
    except Exception as e:
        print(f"❌ Error generating test plan: {e}")
        return None

def generate_playwright_testcases(test_plan_path, output_dir=".", gemini_key=None):
    """Generate Playwright test cases based on the test plan JSON."""
    if not gemini_key:
        raise ValueError("Gemini API key is required")
    
    try:
        # Read the test plan JSON
        with open(test_plan_path, "r", encoding="utf-8") as f:
            test_plan_data = json.load(f)
        
        # Construct prompt for Gemini
        prompt = f"""
        Based on these test cases:
        {json.dumps(test_plan_data, indent=2)}

        Generate Playwright-friendly test cases with values based on the test plan.

        ONLY return a valid JSON object with the following structure:
        {{
            "tests": [
                {{
                    "name": "Test case name",
                    "description": "Detailed description of the test case",
                    "steps": [
                        {{
                            "action": "Action to perform (e.g., navigate, click, type)",
                            "selector": "CSS or XPath selector for the element",
                            "value": "Value to use for the action (if applicable)"
                        }}
                    ],
                    "expected_result": "Expected outcome of the test case"
                }}
            ]
        }}
        Do not include any explanation, only return valid JSON.
        """
        
        # Call Gemini API
        print("📤 Sending Playwright test generation request to Gemini API...")
        response_text = call_gemini_api(GEMINI_MODEL, prompt, gemini_key)
        
        # Process response
        print("📥 Processing Gemini API response...")
        playwright_data = extract_json_from_text(response_text)
        
        # Save Playwright test cases as JSON
        playwright_path = os.path.join(output_dir, "playwright_tests.json")
        with open(playwright_path, "w", encoding="utf-8") as f:
            json.dump(playwright_data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Playwright test cases JSON generated: {playwright_path}")
        return playwright_path
    
    except Exception as e:
        print(f"❌ Error generating Playwright test cases: {e}")
        return None

def run_test_generation_pipeline(doc_path, output_dir=".", gemini_key=None):
    """Run the complete test generation pipeline with proper error handling."""
    if not gemini_key:
        print("❌ Error: Gemini API key is required")
        return False
    
    try:
        print("\n🚀 Starting test generation pipeline...")
        print(f"📄 Input document: {doc_path}")
        print(f"📁 Output directory: {output_dir}")
        
        # Step 1: Parse requirements from Word doc to JSON
        print("\n--- STEP 1: Parse Requirements ---")
        requirements_path = parse_requirements(doc_path, output_dir)
        if not requirements_path:
            return False
        
        # Step 2: Generate test plan from requirements JSON
        print("\n--- STEP 2: Generate Test Plan ---")
        test_plan_path = generate_functionality_testplan(requirements_path, output_dir, gemini_key)
        if not test_plan_path:
            return False
        
        # Step 3: Generate Playwright test cases from test plan JSON
        print("\n--- STEP 3: Generate Playwright Tests ---")
        playwright_path = generate_playwright_testcases(test_plan_path, output_dir, gemini_key)
        if not playwright_path:
            return False
        
        # Print summary
        print("\n✅ Test generation pipeline completed!")
        print(f"📁 Requirements JSON: {requirements_path}")
        print(f"📁 Test Plan JSON: {test_plan_path}")
        print(f"📁 Playwright Tests JSON: {playwright_path}")
        
        # Display test count if available
        try:
            with open(playwright_path, "r", encoding="utf-8") as f:
                test_data = json.load(f)
                test_count = len(test_data.get("tests", []))
                print(f"📋 Generated {test_count} Playwright test cases")
        except Exception as e:
            print(f"⚠️ Could not count test cases: {e}")
            
        return True
    
    except Exception as e:
        print(f"❌ Error in test generation pipeline: {e}")
        return False

if __name__ == "__main__":
    # Configuration parameters
    DOC_PATH = "C:/Users/Aayush/Desktop/HackNUthon/test.docx"
    OUTPUT_DIR = "C:/Users/Aayush/Desktop/HackNUthon/"
    GEMINI_KEY = "AIzaSyDcL-kDSiP7D2db51rYtfOmFpCnVa5JQwQ"  # Replace with your actual API key
    
    # Run the pipeline
    success = run_test_generation_pipeline(DOC_PATH, OUTPUT_DIR, GEMINI_KEY)
    
    if success:
        print("\n🎉 Pipeline completed successfully!")
    else:
        print("\n⚠️ Pipeline completed with errors. Check the logs above for details.")