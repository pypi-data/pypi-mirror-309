
# Aurora Solar API Client

A Python client for interacting with the Aurora Solar API.

## Installation

```bash
pip install aurora_client
```

## Usage

python
from aurora_client import AuroraSolarClient
Initialize the client
client = AuroraSolarClient(
tenant_id="your_tenant_id",
credentials={"bearer_token": "your_token"}
)
List all projects
projects = client.list_projects()
Get specific project details
project = client.retrieve_project("project_id")
List designs for a project
designs = client.list_designs("project_id")


## Available Methods

The client provides methods for interacting with various Aurora Solar API endpoints:

- Projects
- Consumption Profiles
- Designs
- Design Assets
- Components
- Proposals
- Webhooks

For detailed documentation of all available methods, please see the class documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Testing

To run tests, first install the package with test dependencies:

bash
pip install -e ".[test]"

Then run the tests:
bash
Run all tests
pytest
Run only unit tests
pytest src/aurora_client/tests/unit_tests.py
Run only integration tests
pytest src/aurora_client/tests/integration_tests.py
Run with coverage report
pytest --cov=aurora_client
Ask
Copy
Apply

```


