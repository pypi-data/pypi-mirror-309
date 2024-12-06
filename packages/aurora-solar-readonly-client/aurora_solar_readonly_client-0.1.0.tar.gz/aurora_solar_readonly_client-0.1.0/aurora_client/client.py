import requests, json, hashlib, hmac, base64, urllib.parse
from datetime import datetime
from unittest.mock import Mock, patch


class AuroraSolarClient:
	def __init__(self, tenant_id, credentials, version="2024.05"):
		self.tenant_id = tenant_id
		self.base_url = "https://api.aurorasolar.com"
		self.bearer_token = credentials.get('bearer_token')
		self.api_version = "2024.05"  # Add API version
		
		if not self.bearer_token:
			raise ValueError("Bearer token is required in credentials")

	def _make_request(self, method, endpoint, **kwargs):
		url = f"{self.base_url}{endpoint}"
		headers = {
			"Authorization": f"Bearer {self.bearer_token}",
			"Content-Type": "application/json",
			"Aurora-Version": self.api_version  # Add API version header
		}
		
		response = requests.request(method, url, headers=headers, **kwargs)
		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			print(f"Error response body: {response.text}")
			raise
		
		return response.json()
	

	# Version Methods
	def retrieve_versions(self):
		"""Get available API versions"""
		endpoint = "/versions"
		return self._make_request("GET", endpoint)


	# Projects Methods
	def list_projects(self):
		"""List all projects"""
		endpoint = f"/tenants/{self.tenant_id}/projects"
		return self._make_request("GET", endpoint)

	def retrieve_project(self, project_id):
		"""Retrieve specific project details"""
		endpoint = f"/tenants/{self.tenant_id}/projects/{project_id}"
		return self._make_request("GET", endpoint)

	def list_project_assets(self, project_id):
		"""List assets for a project"""
		endpoint = f"/tenants/{self.tenant_id}/projects/{project_id}/assets"
		return self._make_request("GET", endpoint)


	# Consumption Profiles Methods
	def retrieve_consumption_profile(self, project_id):
		"""Retrieve consumption profile for a project"""
		endpoint = f"/tenants/{self.tenant_id}/projects/{project_id}/consumption_profile"
		return self._make_request("GET", endpoint)


	# Designs Methods
	def list_designs(self, project_id):
		"""List all designs for a project"""
		endpoint = f"/tenants/{self.tenant_id}/projects/{project_id}/designs"
		return self._make_request("GET", endpoint)

	def retrieve_design_summary(self, design_id):
		"""Retrieve summary for a design"""
		endpoint = f"/tenants/{self.tenant_id}/designs/{design_id}/summary"
		return self._make_request("GET", endpoint)

	def retrieve_roof_summary(self, design_id):
		"""Retrieve roof summary for a design"""
		endpoint = f"/tenants/{self.tenant_id}/designs/{design_id}/roof_summary"
		return self._make_request("GET", endpoint)

	def list_racking_arrays(self, design_id):
		"""List all racking arrays for a design"""
		endpoint = f"/tenants/{self.tenant_id}/designs/{design_id}/racking_arrays"
		return self._make_request("GET", endpoint)

	def retrieve_web_proposal(self, design_id):
		"""Retrieve web proposal for a design"""
		endpoint = f"/tenants/{self.tenant_id}/designs/{design_id}/web_proposal"
		return self._make_request("GET", endpoint)


	# Design Assets Methods
	def list_design_assets(self, design_id):
		"""List all assets for a design"""
		endpoint = f"/tenants/{self.tenant_id}/designs/{design_id}/assets"
		return self._make_request("GET", endpoint)


	# Webhooks Methods
	def list_webhooks(self):
		"""List all webhooks"""
		endpoint = f"/tenants/{self.tenant_id}/webhooks"
		return self._make_request("GET", endpoint)

	def retrieve_webhook(self, webhook_id):
		"""Retrieve specific webhook details"""
		endpoint = f"/tenants/{self.tenant_id}/webhooks/{webhook_id}"
		return self._make_request("GET", endpoint)




