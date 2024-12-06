# Cognitive SDK

A Python SDK for interacting with the Cognitive API from Cognitive Solutions. This SDK allows you to create and manage conversations with an already defined assistant, send messages, and retrieve conversation history. The package provides a user-friendly interface for integrating assistant chat functionalities into your applications.

## Features

- **Assistant Instantiation**: Instantiate and interact with an assistant.
- **Chat Creation**: Create a chat with an initial message to start a conversation.
- **Message Handling**: Send messages to the assistant and receive responses.
- **Chat History**: Retrieve the full history of a conversation.
- **References Management**: Retrieve additional reference information associated with messages.

## Installation

To install the SDK, you can clone the repository and install it locally:

```bash
pip install -e .
```

## Usage

### Import the SDK

```python
from cogsol import Assistant
```

### Create an Assistant Instance

```python
assistant = Assistant(assistant_id=7, tenant="your_tenant_id", environment="develop")
```

### Start a Chat with an Initial Message

```python
chat, initial_response = assistant.create_chat(initial_message="Hello, who are you?")
print("Initial Assistant Response:", initial_response)
```

### Send Messages to the Chat

```python
response = chat.send_message("Can you tell me more?")
print("Assistant Response:", response)
```

### Retrieve Chat History

```python
history = chat.history
print("Chat History:", history)
```

## References

The `Message` class contains an attribute called `references`, which provides additional information related to the message. A `Reference` object includes:

- **reference_num**: An integer indicating the reference number.
- **source**: A string representing the source of the reference (e.g., a document or URL).
- **showed_num**: An optional integer that represents the number displayed for the reference.

This attribute is particularly useful when the assistant provides responses that include citations or links to supporting information. You can access these references as follows:

```python
for ref in initial_response.references:
    print(f"Reference Number: {ref.reference_num}, Source: {ref.source}, Showed Number: {ref.showed_num}")
```

## Configuration

The base URLs for the assistant API can be customized via environment variables. You can set the following environment variables to specify URLs for different environments:

- `COGSOL_PRODUCTION_URL`
- `COGSOL_DEVELOP_URL`
- `COGSOL_IMPLANTATION_URL`
- `COGSOL_TEST_URL`

If not set, the SDK defaults to `http://localhost:8000/cognitive` for all environments.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests. Make sure to follow the standard coding guidelines and include tests for new features or bug fixes.

## Requirements

- Python 3.6+
- Requests library (>=2.20.0)

Install requirements using:

```bash
pip install -r requirements.txt
```

## Example

Below is a complete example showing how to use the SDK to create a chat, send a message, get the response, and get the history:

```python
from cogsol import Assistant

# Initialize the assistant
assistant = Assistant(assistant_id=7, tenant="your_tenant_id", environment="develop")

# Start a new chat
chat, initial_response = assistant.create_chat(initial_message="Hello, who are you?")
print("Initial Assistant Response:", initial_response)

# Print references from the initial response
for ref in initial_response.references:
    print(f"Reference Number: {ref.reference_num}, Source: {ref.source}, Showed Number: {ref.showed_num}")

# Send a message to the assistant
response = chat.send_message("Can you tell me more?")
print("Assistant Response:", response)

# Get the full chat history
history = chat.history
print("Chat History:", history)
```

## Support

For any questions or support, please open an issue on [GitHub](https://github.com/Pyxis-Cognitive-Solutions/cogsol-python-sdk/).
