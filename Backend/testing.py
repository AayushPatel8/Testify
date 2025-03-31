import json
import os
import sys
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def load_test_cases(filename="test_cases.json"):
    """Load test cases from a JSON file."""
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            if "tests" not in data:
                print(f"⚠️ Warning: No 'tests' array found in {filename}")
                print(f"⚠️ File structure: {list(data.keys())}")
                return None
            if len(data["tests"]) == 0:
                print(f"⚠️ Warning: Empty 'tests' array in {filename}")
                return None
            print(f"✅ Successfully loaded {len(data['tests'])} tests from {filename}")
            return data
    except FileNotFoundError:
        print(f"❌ Test case file '{filename}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in test case file '{filename}': {e}")
        return None

def execute_test_cases(test_cases, headless=True, timeout=30000, retries=2):
    """Execute Playwright test cases with proper error handling and retries."""
    if not test_cases:
        print("❌ No test cases to execute.")
        return False
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "details": []
    }
    
    start_time = time.time()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            browser_context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/90.0.4430.212 Safari/537.36"
            )
            
            for test in test_cases["tests"]:
                test_name = test["name"]
                results["total"] += 1
                test_result = {
                    "name": test_name,
                    "status": "pending",
                    "steps_executed": 0,
                    "total_steps": len(test["steps"]),
                    "error": None,
                    "retry_count": 0
                }
                
                for retry in range(retries + 1):
                    if retry > 0:
                        print(f"🔄 Retry {retry}/{retries} for test: {test_name}")
                        test_result["retry_count"] = retry
                    
                    try:
                        # Create a new page for each test to ensure clean state
                        page = browser_context.new_page()
                        page.set_default_timeout(timeout)
                        
                        print(f"⏱️ Running: {test_name}")
                        steps_executed = 0
                        
                        for step in test["steps"]:
                            action = step["action"]
                            selector = step.get("selector", "")
                            value = step.get("value", "")
                            
                            # Log the step being executed
                            step_desc = f"  Step {steps_executed + 1}: {action}"
                            if selector:
                                step_desc += f" on '{selector}'"
                            if value:
                                step_desc += f" with value '{value}'"
                            print(step_desc)
                            
                            if action == "navigate":
                                page.goto(value)
                            elif action == "click":
                                page.click(selector)
                            elif action == "type":
                                page.fill(selector, value)
                            elif action == "wait":
                                wait_time = int(value) if value.isdigit() else 1000
                                page.wait_for_timeout(wait_time)
                            elif action == "assert":
                                assert value in page.text_content(selector), f"Assertion failed: '{value}' not found in '{selector}'"
                            elif action == "assert_visible":
                                assert page.is_visible(selector), f"Element '{selector}' is not visible"
                            
                            steps_executed += 1
                            test_result["steps_executed"] = steps_executed
                        
                        # Test passed if all steps executed successfully
                        print(f"✅ {test_name} passed!")
                        test_result["status"] = "passed"
                        results["passed"] += 1
                        page.close()
                        break  # Exit retry loop on success
                        
                    except PlaywrightTimeoutError as e:
                        error_msg = f"Timeout: {str(e)}"
                        print(f"⚠️ {error_msg}")
                        test_result["error"] = error_msg
                        if retry == retries:  # Only mark as failed on last retry
                            test_result["status"] = "failed"
                            results["failed"] += 1
                        page.close()
                    
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        print(f"❌ {error_msg}")
                        test_result["error"] = error_msg
                        if retry == retries:  # Only mark as failed on last retry
                            test_result["status"] = "failed"
                            results["failed"] += 1
                        page.close()
                
                results["details"].append(test_result)
            
            browser.close()
    
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return False
    
    # Calculate execution time and generate report
    execution_time = time.time() - start_time
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"TEST EXECUTION SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Execution Time: {execution_time:.2f} seconds")
    print("=" * 50)
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.json"
    with open(report_file, "w") as f:
        json.dump({
            "summary": {
                "timestamp": timestamp,
                "execution_time": execution_time,
                "total": results["total"],
                "passed": results["passed"],
                "failed": results["failed"],
                "skipped": results["skipped"]
            },
            "tests": results["details"]
        }, f, indent=2)
    
    print(f"📝 Report saved: {report_file}")
    return results["failed"] == 0

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Run automated Playwright tests")
    parser.add_argument("--test-file", default="playwright_tests.json", help="Path to test cases JSON file")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
    parser.add_argument("--timeout", type=int, default=30000, help="Timeout in milliseconds")
    parser.add_argument("--retries", type=int, default=2, help="Number of retries for failed tests")
    parser.add_argument("--base-url", default="https://krishimitra-front.onrender.com/auth", help="Base URL for tests")
    args = parser.parse_args()
    
    # Load and execute test cases
    print(f"🚀 Starting automated test execution")
    print(f"📋 Loading test cases from: {args.test_file}")
    test_cases = load_test_cases(args.test_file)
    
    # Add base URL to test cases if needed
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
        
        # Exit with appropriate status code for CI integration
        sys.exit(0 if success else 1)
    else:
        sys.exit(1)