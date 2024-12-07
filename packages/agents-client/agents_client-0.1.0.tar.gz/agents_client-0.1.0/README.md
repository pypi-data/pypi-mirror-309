# Agents Client Library

## Overview
The Agents Client Library provides a simple interface for interacting with the Agents API. It handles authentication, request management, and provides convenient methods for managing chatbots and agents.

## Installation

### From PyPI
```bash
pip install agents-client
```

### From Source
```bash
git clone https://github.com/Levangie-Laboratories/agents-client.git
cd agents-client
pip install -r requirements.txt
```

## Configuration
The client library uses a `config.json` file for API settings. You can either use the default configuration or provide your own:

```python
from agents.client import AgentClient

# Using default configuration
client = AgentClient()

# Using custom configuration file
client = AgentClient(config_path='path/to/config.json')

# Override configuration programmatically
client = AgentClient(base_url='https://api.example.com', api_version='v2')
```

### Configuration Options
- `base_url`: API base URL
- `version`: API version
- `timeout`: Request timeout in seconds
- `retry_attempts`: Number of retry attempts
- `retry_delay`: Delay between retries in seconds

See `config.json` for all available options.

## Quick Start

### Basic Usage
```python
from agents.client import AgentClient

# Initialize client
client = AgentClient("http://localhost:8000")

# Get API key
api_key_data = client.get_quick_api_key()
print(f"API Key: {api_key_data['api_key']}")

# Create a chatbot
config = {
    "behavior": "friendly",
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 500
}
chatbot = client.create_chatbot(name="MyBot", model="gpt-4", config=config)

# Make an inference
response = client.infer_chatbot(chatbot["id"], "Hello, how are you?")
```

### Async Streaming Example
```python
from agents.client import AgentClient
import asyncio

async def main():
    # Initialize client with async context manager
    async with AgentClient("http://localhost:8000") as client:
        client.set_api_key("your-api-key")

        # Create an agent with API execution mode
        config = {
            "behavior": "task-focused",
            "model": "gpt-4",
            "api_mode": True  # Enable API execution mode
        }
        agent = await client.create_agent_with_tools(
            name="FileManager",
            model="gpt-4",
            tools=FileTools(),  # Your tool class instance
            config=config
        )

        # Stream interactions with the agent
        async for event in client.process_agent_request(agent["id"], "Update debug mode in config.json"):
            if event["type"] == "function_call":
                print(f"Executing function: {event['data']['function']}")
                # Function is automatically executed by the client
            elif event["type"] == "execution_status":
                print(f"Execution result: {event['data']}")
            elif event["type"] == "completion":
                print(f"Task completed: {event['data']}")
            elif event["type"] == "error":
                print(f"Error: {event['data']}")

# Run the async client
asyncio.run(main())
```

### State Management Example
```python
async with AgentClient("http://localhost:8000") as client:
    # State is automatically synchronized
    async for event in client.process_agent_request(agent_id, message):
        if event["type"] == "state_update":
            print(f"Agent state updated: {event['data']}")
        elif event["type"] == "function_call":
            # State is preserved across function calls
            result = await client.execute_function(event["data"])
            # State is automatically updated with function results
            await client.submit_result(agent_id, event["data"]["sequence_id"], result)
```
```

## Authentication
The client supports two authentication methods:
1. Quick API key generation
2. Manual API key setting

```python
# Method 1: Quick API key
api_key_data = client.get_quick_api_key()

# Method 2: Manual setting
client.set_api_key("your-api-key")
```

## Chatbot Operations

### Creating a Chatbot
```python
config = {
    "behavior": "friendly",
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 500,
    "provider": "openai"
}

chatbot = client.create_chatbot(
    name="MyAssistant",
    model="gpt-4",
    config=config
)
```

### Listing Chatbots
```python
chatbots = client.list_chatbots()
for bot in chatbots:
    print(f"Bot: {bot['name']} (ID: {bot['id']})")
```

### Making Inferences
```python
response = client.infer_chatbot(
    chatbot_id=123,
    message="What's the weather like?"
)
print(response["response"])
```

### Updating Chatbots
```python
updated_config = {
    "temperature": 0.8,
    "max_tokens": 1000
}

updated_bot = client.update_chatbot(
    chatbot_id=123,
    name="UpdatedBot",
    model="gpt-4",
    config=updated_config
)
```

### Deleting Chatbots
```python
result = client.delete_chatbot(chatbot_id=123)
```

## Agent Operations

### Creating an Agent
```python
config = {
    "tool_config": {...},
    "behavior": "task-focused"
}

agent = client.create_agent(
    name="TaskAgent",
    model="gpt-4",
    class_instance="MyAgentClass",
    config=config
)
```

### Listing Agents
```python
agents = client.list_agents()
for agent in agents:
    print(f"Agent: {agent['name']} (ID: {agent['id']})")
```

### Command Execution System
The client now includes an automatic command execution system using the ClientInterpreter:

```python
from client import AgentClient
from client.command_handler import ToolConfigGenerator

# Define your tools
class FileTools:
    def read_file(self, file_path: str) -> str:
        """Read content from a file"""
        with open(file_path, 'r') as f:
            return f.read()

    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a file"""
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"

# Initialize client and tools
client = AgentClient()
tools = FileTools()

# Register tools with the interpreter
tool_config = ToolConfigGenerator.extract_command_config(tools)
client.interpreter.register_command_instance(tools, tool_config)

# Interact with agent - commands are executed automatically
response = client.interact(
    agent_id,
    "Update the config file"
)

# The interpreter automatically:
# 1. Executes any commands in the response
# 2. Collects the results
# 3. Sends them back to the agent
# 4. Returns the final response
```

The new system simplifies command execution by:
```

Key features of the new command system:
- Automatic command execution and result handling
- Built-in command validation and safety checks
- Simplified tool registration using decorators
- Automatic result mapping in responses
- Support for both synchronous and asynchronous operations
- Comprehensive error handling and reporting

### Supported Commands
The client can execute various commands locally:

```python
# File operations
commands = [
    {"view_file": {"file_path": "config.json"}},
    {"smart_replace": {
        "file_path": "config.json",
        "old_text": "debug: false",
        "new_text": "debug: true"
    }},
    {"create_file": {
        "file_path": "new_file.txt",
        "content": "Hello, world!"
    }}
]

# Execute commands with safety checks
results = client.execute_commands(commands, context={})
```

### Command Execution Safety
- File path validation
- Comprehensive error handling
- Safe text replacement
- Automatic retries for network issues

```python
# Example with error handling
try:
    results = client.execute_commands(commands, context={})
    if any(r["status"] == "error" for r in results["command_results"]):
        print("Some commands failed to execute")
        for result in results["command_results"]:
            if result["status"] == "error":
                print(f"Error: {result['error']}")
except Exception as e:
    print(f"Execution failed: {str(e)}")
```

## Streaming Operations

### Basic Streaming
```python
async with AgentClient("http://localhost:8000") as client:
    # Stream responses from agent
    async for event in client.interact_stream(agent_id, message):
        if event["type"] == "function_call":
            # Handle function execution
            result = await client.execute_function(event["data"])
            await client.submit_result(agent_id, event["data"]["sequence_id"], result)
        elif event["type"] == "completion":
            print(f"Completed: {event['data']}")
```

### Concurrent Command Execution
```python
async def process_commands(client, commands, instance_id):
    # Commands are executed concurrently
    results = await client.execute_commands(commands, instance_id)
    return results
```

## Error Handling
The client includes comprehensive error handling with streaming support:

### Streaming Error Handling
```python
async with AgentClient("http://localhost:8000") as client:
    try:
        async for event in client.interact_stream(agent_id, message):
            if event["type"] == "error":
                print(f"Error occurred: {event['data']}")
                break
            elif event["type"] == "function_call":
                try:
                    result = await client.execute_function(event["data"])
                    await client.submit_result(
                        agent_id,
                        event["data"]["sequence_id"],
                        result
                    )
                except Exception as e:
                    print(f"Function execution error: {e}")
    except Exception as e:
        print(f"Stream error: {e}")
```

### Command Execution Errors
```python
try:
    results = client.execute_commands(commands, context)
    for result in results['command_results']:
        if result['status'] == 'error':
            print(f"Command {result['command']} failed: {result['error']}")
except client.CommandExecutionError as e:
    print(f"Execution error: {str(e)}")
```

### API Errors
```python
try:
    chatbot = client.get_chatbot(999)
except Exception as e:
    print(f"API error: {str(e)}")
```

## Best Practices
1. Always handle API errors in production code
2. Store API keys securely
3. Use appropriate timeouts for API calls
4. Monitor rate limits
5. Implement proper error handling
6. Validate file paths before operations
7. Use context information for better error tracking
8. Implement proper retry strategies

### Error Handling Best Practices
```python
# Comprehensive error handling example
try:
    # Initial interaction
    response = client.interact_with_agent(agent_id, message)
    
    if response['status'] == 'pending_execution':
        try:
            # Execute commands with safety checks
            results = client.execute_commands(
                response['commands'],
                response.get('context', {})
            )
            
            # Check individual command results
            failed_commands = [
                r for r in results['command_results']
                if r['status'] == 'error'
            ]
            
            if failed_commands:
                print("Some commands failed:")
                for cmd in failed_commands:
                    print(f"- {cmd['command']}: {cmd['error']}")
            
            # Continue interaction with results
            final_response = client.interact_with_agent(
                agent_id,
                message,
                execution_results=results
            )
            
        except client.CommandExecutionError as e:
            print(f"Command execution failed: {e}")
            # Handle command execution failure
            
except Exception as e:
    print(f"Interaction failed: {e}")
    # Handle interaction failure
```

## Advanced Usage

### Custom Headers
```python
client = AgentClient(
    base_url="http://localhost:8000",
    headers={"Custom-Header": "value"}
)
```

### Batch Operations
```python
# Create multiple chatbots
configs = [
    {"name": "Bot1", "model": "gpt-4", "config": {...}},
    {"name": "Bot2", "model": "gpt-4", "config": {...}}
]

chatbots = []
for config in configs:
    bot = client.create_chatbot(**config)
    chatbots.append(bot)
```