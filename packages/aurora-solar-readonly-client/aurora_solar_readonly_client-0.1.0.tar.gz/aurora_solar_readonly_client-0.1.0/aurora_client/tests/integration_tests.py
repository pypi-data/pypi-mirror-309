import os
import sys
import pytest
from unittest.mock import Mock, patch
from aurora_client import AuroraSolarClient

# Create a new client object
BEARER_TOKEN = os.getenv('AURORA_BEARER_TOKEN')
TENANT_ID = os.getenv('AURORA_TENANT_ID')
client = AuroraSolarClient(
    tenant_id=TENANT_ID,
    credentials={"bearer_token": BEARER_TOKEN},
    version="2024.05"
)

# Create a new client object using the fixture
@pytest.fixture(autouse=True)
def setup(client, test_ids):
    global TEST_PROJECT_ID, TEST_DESIGN_ID, TEST_WEBHOOK_ID
    
    # Set global variables from test_ids fixture
    TEST_PROJECT_ID = test_ids['PROJECT_ID']
    TEST_DESIGN_ID = test_ids['DESIGN_ID']
    TEST_WEBHOOK_ID = test_ids['WEBHOOK_ID']



def skip_if_not_configured(env_var):
    """Decorator to skip tests if required environment variables are not set"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not os.getenv(env_var):
                pytest.skip(f"Test skipped: {env_var} not configured")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Add a setup function that can help identify missing IDs
def pytest_sessionstart(session):
    """Print configured test IDs at start of test session"""
    print("\nConfigured test IDs:")
    for var, value in get_test_ids().items():
        print(f"{var}: {value}")
    print("\n")

def requires_env(env_var):
    """Decorator to skip test if required environment variable is not set"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not os.getenv(env_var):
                pytest.skip(f"Test skipped: {env_var} not configured")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Version Methods
def test_retrieve_versions():
    response = client.retrieve_versions()
    assert "versions" in response


# Projects Methods
def test_list_projects():
    response = client.list_projects()
    assert "projects" in response

@skip_if_not_configured('TEST_PROJECT_ID')
def test_retrieve_project():
    response = client.retrieve_project(TEST_PROJECT_ID)
    assert "project" in response

@skip_if_not_configured('TEST_PROJECT_ID')
def test_list_project_assets():
    response = client.list_project_assets(TEST_PROJECT_ID)
    assert "project_assets" in response


# Consumption Profiles Methods
@skip_if_not_configured('TEST_PROJECT_ID')
def test_retrieve_consumption_profile():
    response = client.retrieve_consumption_profile(TEST_PROJECT_ID)
    assert "consumption_profile" in response


# Design Methods
@skip_if_not_configured('TEST_PROJECT_ID')
def test_list_designs():
    response = client.list_designs(TEST_PROJECT_ID)
    assert "designs" in response

@skip_if_not_configured('TEST_DESIGN_ID')
def test_retrieve_design_summary():
    response = client.retrieve_design_summary(TEST_DESIGN_ID)
    assert "design" in response

@skip_if_not_configured('TEST_DESIGN_ID')
def test_retrieve_roof_summary():
    response = client.retrieve_roof_summary(TEST_DESIGN_ID)
    assert "roofs" in response

@skip_if_not_configured('TEST_DESIGN_ID')
def test_list_racking_arrays():
    response = client.list_racking_arrays(TEST_DESIGN_ID)
    assert "racking_arrays" in response

@skip_if_not_configured('TEST_DESIGN_ID')
def test_retrieve_web_proposal():
    """Test retrieving web proposal for a design"""
    response = client.retrieve_web_proposal(TEST_DESIGN_ID)
    assert "web_proposal" in response


# Webhooks Methods
def test_list_webhooks():
    response = client.list_webhooks()
    assert "webhooks" in response

@skip_if_not_configured('TEST_WEBHOOK_ID')
def test_retrieve_webhook():
    response = client.retrieve_webhook(TEST_WEBHOOK_ID)
    assert "webhook" in response
    assert "created_at" in response["webhook"]


if __name__ == "__main__":
    # Check for required environment variables
    required_vars = [
        'AURORA_TENANT_ID', 'AURORA_BEARER_TOKEN',
        'TEST_PROJECT_ID', 'TEST_DESIGN_ID',
        'TEST_WEBHOOK_ID', 'TEST_AGREEMENT_ID',
        'TEST_PROPOSAL_ID', 'TEST_SURVEY_ID',
        'TEST_MODULE_ID', 'TEST_INVERTER_ID'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        exit(1)

    print("Running integration tests...")
    pytest.main([__file__, "-v"])