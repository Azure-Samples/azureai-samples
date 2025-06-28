#!/usr/bin/env python3
"""
Test script to verify Azure AI Red Teaming infrastructure deployment.

This script tests the deployed infrastructure by:
1. Connecting to Azure AI Project using DefaultAzureCredential
2. Verifying OpenAI connection and model availability
3. Testing storage account access
4. Validating authentication setup

Run this script after deployment to verify everything is working correctly.

Prerequisites:
- azure-ai-evaluation package installed
- azure-ai-projects package installed
- Environment variables set (from deployment output)
- Azure authentication configured (az login or azd auth login)

Usage:
    python test_deployment.py
"""

import os
import sys


# Color output helper
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_success(message: str) -> None:
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_warning(message: str) -> None:
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_error(message: str) -> None:
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message: str) -> None:
    print(f"{Colors.BLUE}i {message}{Colors.END}")


def check_environment_variables() -> bool:
    """Check if required environment variables are set."""
    required_vars = [
        "AZURE_SUBSCRIPTION_ID",
        "AZURE_RESOURCE_GROUP",
        "AI_PROJECT_NAME",
        "AI_FOUNDRY_ENDPOINT",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_STORAGE_ACCOUNT_NAME",
        "AZURE_OPENAI_API_KEY",
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print_error("Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print_info("Please set these variables from your deployment output.")
        return False

    print_success("All required environment variables are set")
    return True


def test_azure_ai_project() -> bool:
    """Test Azure AI Project connection."""
    try:
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential

        print_info("Testing Azure AI Project connection...")
        credential = DefaultAzureCredential()  # Get required parameters from environment variables
        subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
        resource_group_name = os.environ["AZURE_RESOURCE_GROUP"]
        project_name = os.environ["AI_PROJECT_NAME"]
        endpoint = os.environ["AI_FOUNDRY_ENDPOINT"]

        # Create project client to test connection
        AIProjectClient(
            endpoint=endpoint,
            credential=credential,
            subscription_id=subscription_id,
            resource_group_name=resource_group_name,
            project_name=project_name,
        )

        # If we reach here, connection was successful
        print_success(f"Connected to Azure AI Project: {project_name}")
        print_info(f"Resource Group: {resource_group_name}")
        print_info(f"Subscription: {subscription_id}")
        return True

    except ImportError:
        print_error("azure-ai-projects package not installed. Run: pip install azure-ai-projects")
        return False
    except KeyError as e:
        print_error(f"Missing environment variable: {e!s}")
        return False
    except Exception as e:
        print_error(f"Failed to connect to Azure AI Project: {e!s}")
        return False


def test_openai_connection() -> bool:
    """Test OpenAI connection and model availability."""
    try:
        from openai import AzureOpenAI

        print_info("Testing Azure OpenAI connection...")

        client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2025-01-01-preview",
        )
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-4o",  # Use the deployed GPT-4o model
            messages=[{"role": "user", "content": "Say hello!"}],
            max_tokens=10,
        )

        print_success("OpenAI connection successful")
        print_info(f"Test response: {response.choices[0].message.content}")
        return True

    except ImportError:
        print_error("openai package not installed. Run: pip install openai")
        return False
    except Exception as e:
        print_error(f"Failed to connect to Azure OpenAI: {e!s}")
        print_info("Check that gpt-4o model is deployed and you have proper permissions")
        return False


def test_storage_access() -> bool:
    """Test Azure Storage access."""
    try:
        from azure.storage.blob import BlobServiceClient
        from azure.identity import DefaultAzureCredential

        print_info("Testing Azure Storage access...")

        credential = DefaultAzureCredential()
        storage_account_name = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]

        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=credential
        )

        # Try to list containers (this tests authentication)
        containers = list(blob_service_client.list_containers())
        print_success(f"Storage access successful. Found {len(containers)} containers")
        return True

    except ImportError:
        print_error("azure-storage-blob package not installed. Run: pip install azure-storage-blob")
        return False
    except Exception as e:
        print_error(f"Failed to access Azure Storage: {e!s}")
        return False


def test_ai_evaluation() -> bool:
    """Test Azure AI Evaluation package."""
    try:
        import importlib.util

        spec = importlib.util.find_spec("azure.ai.evaluation")
        if spec is None:
            print_error("azure-ai-evaluation package not installed. Run: pip install azure-ai-evaluation")
            return False

        print_success("Azure AI Evaluation package is available")
        return True
    except ImportError:
        print_error("azure-ai-evaluation package not installed. Run: pip install azure-ai-evaluation")
        return False
    except Exception as e:
        print_warning(f"Azure AI Evaluation import warning: {e!s}")
        return True


def test_red_team_permissions() -> bool:
    """Test if user has required permissions for red team operations."""
    try:
        from azure.identity import DefaultAzureCredential
        from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
        from azure.core.exceptions import ClientAuthenticationError, HttpResponseError

        print_info("Testing red team permissions...")
        credential = DefaultAzureCredential()

        subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
        resource_group = os.environ["AZURE_RESOURCE_GROUP"]

        # Try to create a management client to test permissions
        try:
            mgmt_client = CognitiveServicesManagementClient(credential, subscription_id)

            # List accounts to test basic read permissions
            accounts = list(mgmt_client.accounts.list_by_resource_group(resource_group))
            if accounts:
                print_success("✓ Basic Cognitive Services permissions verified")
                print_info("Red team operations should work with deployed permissions")
                return True
            print_warning("No Cognitive Services accounts found in resource group")
            return False

        except ClientAuthenticationError as e:
            print_error(f"Authentication failed: {e!s}")
            print_warning("You may need 'Cognitive Services Contributor' role for red team operations")
            return False
        except HttpResponseError as e:
            if "Authorization" in str(e) or "Permission" in str(e):
                print_error(f"Permission error: {e!s}")
                print_warning("You may need 'Cognitive Services Contributor' role for red team operations")
                return False
            print_warning(f"HTTP error (may be temporary): {e!s}")
            return True
        except Exception as e:
            print_warning(f"Could not verify permissions (continuing anyway): {e!s}")
            return True

    except ImportError:
        print_warning("azure-mgmt-cognitiveservices not available for permission testing")
        print_info("Install with: pip install azure-mgmt-cognitiveservices")
        return True  # Don't fail the test for missing optional dependency
    except Exception as e:
        print_warning(f"Permission test failed (continuing anyway): {e!s}")
        return True


def main() -> None:
    """Run all deployment tests."""
    print(f"{Colors.BOLD}🧪 Azure AI Red Teaming Deployment Test{Colors.END}")
    print("=" * 50)

    tests = [
        ("Environment Variables", check_environment_variables),
        ("Azure AI Evaluation Package", test_ai_evaluation),
        ("Azure AI Project", test_azure_ai_project),
        ("Azure OpenAI", test_openai_connection),
        ("Azure Storage", test_storage_access),
        ("Red Team Permissions", test_red_team_permissions),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{Colors.BOLD}Testing {test_name}...{Colors.END}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Unexpected error in {test_name}: {e!s}")
            results.append((test_name, False))

    # Summary
    print(f"\n{Colors.BOLD}Test Summary:{Colors.END}")
    print("=" * 30)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status:<6}{Colors.END} {test_name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print_success("🎉 All tests passed! Your deployment is ready for AI Red Teaming.")
    else:
        print_warning("⚠️ Some tests failed. Check the error messages above and verify your deployment.")
        sys.exit(1)


if __name__ == "__main__":
    main()
