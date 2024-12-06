import pytest
from unittest.mock import Mock, patch
import os
from dotenv import load_dotenv
from aurora_client import AuroraSolarClient
from pathlib import Path


@pytest.fixture
def client():
    """Create a test client instance"""
    credentials = {"bearer_token": os.getenv("AURORA_BEARER_TOKEN")}
    return AuroraSolarClient(os.getenv("AURORA_TENANT_ID"), credentials)

@pytest.fixture
def mock_response():
    """Create a mock successful response"""
    return Mock(
        json=lambda: {"data": "success"},
        raise_for_status=lambda: None
    )

@pytest.fixture
def test_ids():
    """Get test IDs from environment variables"""
    return {
        'project_id': os.getenv('TEST_PROJECT_ID'),
        'design_id': os.getenv('TEST_DESIGN_ID'),
        'proposal_id': os.getenv('TEST_PROPOSAL_ID')
    }

@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        "name": "Test Project",
        "address": {
            "street": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip": "12345"
        }
    }

@pytest.fixture
def sample_project_data():
    return {
        "name": "Test Project",
        "address": {...}
    }

@pytest.fixture
def sample_design_data():
    return {
        "name": "Test Design",
        "system_size": 10.5
    }

@pytest.fixture
def sample_proposal_data():
    return {
        "name": "Test Proposal",
        "status": "draft"
    }


class TestProjectMethods:
    def setup_method(self):
        self.tenant_id = "test_tenant"
        self.credentials = {"bearer_token": "test_token"}
        self.client = AuroraSolarClient(
            tenant_id=self.tenant_id,
            credentials=self.credentials
        )

    def test_list_projects_success(self):
        """Test successful projects listing"""
        expected_response = {
            "projects": [
                {
                    "id": "project1",
                    "name": "First Project",
                    "status": "active"
                },
                {
                    "id": "project2",
                    "name": "Second Project",
                    "status": "complete"
                }
            ]
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.list_projects()
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/projects"
            )

    def test_retrieve_project_success(self):
        """Test successful project retrieval"""
        project_id = "test_project"
        expected_response = {
            "id": project_id,
            "name": "Test Project",
            "status": "active",
            "address": {
                "street": "123 Main St",
                "city": "Test City",
                "state": "TS",
                "zip": "12345"
            }
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.retrieve_project(project_id)
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/projects/{project_id}"
            )

    def test_list_project_assets_success(self):
        """Test successful project assets listing"""
        project_id = "test_project"
        expected_response = {
            "assets": [
                {
                    "id": "asset1",
                    "type": "document",
                    "name": "Site Survey"
                },
                {
                    "id": "asset2",
                    "type": "image",
                    "name": "Roof Photo"
                }
            ]
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.list_project_assets(project_id)
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/projects/{project_id}/assets"
            )

    def test_list_projects_empty(self):
        """Test projects listing with empty response"""
        expected_response = {"projects": []}
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.list_projects()
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/projects"
            )

    def test_list_project_assets_empty(self):
        """Test project assets listing with empty response"""
        project_id = "test_project"
        expected_response = {"assets": []}
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.list_project_assets(project_id)
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/projects/{project_id}/assets"
            )

class TestDesignMethods:
    def setup_method(self):
        """Setup test client before each test"""
        self.tenant_id = "test_tenant"
        self.credentials = {"bearer_token": "test_token"}
        self.client = AuroraSolarClient(
            tenant_id=self.tenant_id,
            credentials=self.credentials
        )

    def test_list_designs_success(self):
        """Test successful design listing"""
        project_id = "test_project"
        expected_response = {
            "designs": [
                {"id": "design1", "name": "First Design"},
                {"id": "design2", "name": "Second Design"}
            ]
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.list_designs(project_id)
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/projects/{project_id}/designs"
            )


    def test_retrieve_design_summary_success(self):
        """Test successful design summary retrieval"""
        design_id = "test_design"
        expected_response = {
            "annual_production": 10000,
            "system_size": 5.6,
            "module_count": 16
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.retrieve_design_summary(design_id)
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/designs/{design_id}/summary"
            )

    def test_list_racking_arrays_success(self):
        """Test successful racking arrays listing"""
        design_id = "test_design"
        expected_response = {
            "arrays": [
                {"id": "array1", "module_count": 8},
                {"id": "array2", "module_count": 8}
            ]
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.list_racking_arrays(design_id)
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/designs/{design_id}/racking_arrays"
            )

class TestVersionMethods:
    def setup_method(self):
        self.tenant_id = "test_tenant"
        self.credentials = {"bearer_token": "test_token"}
        self.client = AuroraSolarClient(
            tenant_id=self.tenant_id,
            credentials=self.credentials
        )

    def test_retrieve_versions(self):
        """Test successful version retrieval"""
        expected_response = {
            "versions": ["2024.03", "2024.05"]
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.retrieve_versions()
            
            assert response == expected_response
            mock_request.assert_called_once_with("GET", "/versions")

    def test_retrieve_versions_empty(self):
        """Test version retrieval with empty response"""
        expected_response = {"versions": []}
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.retrieve_versions()
            
            assert response == expected_response
            mock_request.assert_called_once_with("GET", "/versions")

class TestConsumptionProfileMethods:
    def setup_method(self):
        self.tenant_id = "test_tenant"
        self.credentials = {"bearer_token": "test_token"}
        self.client = AuroraSolarClient(
            tenant_id=self.tenant_id,
            credentials=self.credentials
        )

    def test_retrieve_consumption_profile_success(self):
        """Test successful consumption profile retrieval"""
        project_id = "test_project"
        expected_response = {
            "annual_consumption": 12000,
            "monthly_data": [
                {"month": 1, "consumption": 1000},
                {"month": 2, "consumption": 900}
            ]
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.retrieve_consumption_profile(project_id)
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/projects/{project_id}/consumption_profile"
            )

    def test_retrieve_consumption_profile_empty(self):
        """Test consumption profile retrieval with empty response"""
        project_id = "test_project"
        expected_response = {"monthly_data": []}
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.retrieve_consumption_profile(project_id)
            
            assert response == expected_response
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/projects/{project_id}/consumption_profile"
            )

class TestWebhookMethods:
    def setup_method(self):
        """Setup test client before each test"""
        self.tenant_id = "test_tenant"
        self.credentials = {"bearer_token": "test_token"}
        self.client = AuroraSolarClient(
            tenant_id=self.tenant_id,
            credentials=self.credentials
        )

    def test_list_webhooks_success(self):
        """Test successful webhook listing"""
        expected_response = {
            "webhooks": [
                {"id": "webhook1", "url": "http://example.com/webhook1"},
                {"id": "webhook2", "url": "http://example.com/webhook2"}
            ]
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.list_webhooks()
            
            # Assert the response matches expected data
            assert response == expected_response
            # Assert the correct endpoint was called with correct method
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/webhooks"
            )

    def test_retrieve_webhook_success(self):
        """Test successful webhook retrieval"""
        webhook_id = "test_webhook_id"
        expected_response = {
            "id": webhook_id,
            "url": "http://example.com/webhook",
            "status": "active"
        }
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.retrieve_webhook(webhook_id)
            
            # Assert the response matches expected data
            assert response == expected_response
            # Assert the correct endpoint was called with correct method
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/webhooks/{webhook_id}"
            )

    def test_list_webhooks_empty(self):
        """Test webhook listing with empty response"""
        expected_response = {"webhooks": []}
        
        with patch.object(self.client, '_make_request') as mock_request:
            mock_request.return_value = expected_response
            response = self.client.list_webhooks()
            
            # Assert the response matches expected data
            assert response == expected_response
            # Assert the correct endpoint was called with correct method
            mock_request.assert_called_once_with(
                "GET", 
                f"/tenants/{self.tenant_id}/webhooks"
            )

