import pytest
import os
from pathlib import Path
from dotenv import load_dotenv
from aurora_client import AuroraSolarClient

# Clear any cached environment variables
os.environ.clear()

# Load environment variables
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent.parent.parent
env_path = project_root / '.env'
load_dotenv(env_path)

@pytest.fixture
def client():
    """Create a test client instance"""
    return AuroraSolarClient(
        tenant_id=os.getenv('AURORA_TENANT_ID'),
        credentials={"bearer_token": os.getenv('AURORA_BEARER_TOKEN')},
        version="2022.09"
    )

@pytest.fixture
def test_ids():
    """Get test IDs from environment variables located in {env_path}"""
    ids = {
        'PROJECT_ID': os.getenv('TEST_PROJECT_ID'),
        'DESIGN_ID': os.getenv('TEST_DESIGN_ID'),
        'WEBHOOK_ID': os.getenv('TEST_WEBHOOK_ID'),
    }
    return ids



