import os
import requests

class Assistant:
    """
    A class used to represent an Assistant.
    
    Attributes
    ----------
    assistant_id : str
        The ID of the assistant to interact with.
    description : str
        The description of the assistant.
    initial_message : str, optional
        The initial message the assistant sends when a chat is created, if any.
    tenant : str
        The tenant key used for authentication.
    environment : str
        The environment in which the assistant operates (e.g., "production", "develop").
    """
    def __init__(self, assistant_id, tenant, environment):
        """
        Parameters
        ----------
        assistant_id : str
            The ID of the assistant to interact with.
        tenant : str
            The tenant key used for authentication.
        environment : str
            The environment in which the assistant operates (e.g., "production", "develop").
        """
        self.assistant_id = assistant_id
        self.tenant = tenant
        self.environment = environment
        self.base_url = self._get_base_url()

        # Get Assistant info
        url = f"{self.base_url}/assistants/{self.assistant_id}/"
        headers = {"Content-Type": "application/json", "X-Api-Key": self.tenant}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        assistant_data = response.json()
        self.description = assistant_data.get("description")
        self.initial_message = assistant_data.get("initial_message", None)

    def _get_base_url(self):
        """
        Get the base URL depending on the environment.

        Returns
        -------
        str
            The base URL for the specified environment.
        """
        env_map = {
            "production": os.getenv("COGSOL_PRODUCTION_URL", "http://localhost:8000/cognitive"),
            "develop": os.getenv("COGSOL_DEVELOP_URL", "http://localhost:8000/cognitive"),
            "implantation": os.getenv("COGSOL_IMPLANTATION_URL", "http://localhost:8000/cognitive"),
            "test": os.getenv("COGSOL_TEST_URL", "http://localhost:8000/cognitive"),
        }
        return env_map.get(self.environment, "http://localhost:8000/cognitive")

    def create_chat(self, initial_message):
        """
        Create a chat with the assistant and send an initial message.

        Parameters
        ----------
        initial_message : str
            The initial message to start the chat.

        Returns
        -------
        tuple
            A tuple containing an instance of the Chat class representing the created chat
            and the initial response from the assistant.
        """
        url = f"{self.base_url}/assistants/{self.assistant_id}/chats/"
        headers = {"Content-Type": "application/json", "X-Api-Key": self.tenant}
        payload = {"message": initial_message}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        chat_data = response.json()
        chat = Chat(chat_data['id'], self, self.base_url, self.tenant, chat_data)
        initial_response = Message.from_json(chat_data['messages'][-1])
        return chat, initial_response

    def __repr__(self):
        return f"Assistant(assistant_id={self.assistant_id}, description={self.description}, environment={self.environment})"


class Chat:
    """
    A class used to represent a Chat.
    
    Attributes
    ----------
    chat_id : str
        The ID of the chat.
    assistant : Assistant
        The assistant object associated with the chat.
    title : str
        The title of the chat.
    ended : bool
        A flag indicating if the chat has ended.
    max_responses : int
        The maximum number of responses allowed in the chat.
    max_msg_length : int
        The maximum length of a message in the chat, in characters.
    history : list of Message
        A list of Message objects representing the chat history.
    base_url : str
        The base URL of the API.
    tenant : str
        The tenant key used for authentication.
    """
    def __init__(self, chat_id, assistant, base_url, tenant, chat_data):
        """
        Parameters
        ----------
        chat_id : str
            The ID of the chat.
        assistant : Assistant
            The assistant object associated with the chat.
        base_url : str
            The base URL of the API.
        tenant : str
            The tenant key used for authentication.
        chat_data : dict
            Additional keyword arguments to set the chat attributes.
        """
        self.chat_id = chat_id
        self.assistant = assistant
        self.base_url = base_url
        self.tenant = tenant

        # Chat info
        self._update_chat_info(**chat_data)
    
    def _update_chat_info(self, **kwargs):
        """
        Update chat attributes with the provided keyword arguments.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments to set the chat attributes.
        """
        # Chat info
        self.title = kwargs.get("title")
        self.ended = kwargs.get("ended")
        self.max_responses = kwargs.get("max_responses")
        self.max_msg_length = kwargs.get("max_msg_length")

        # Chat history
        messages_data = kwargs.get("messages", [])
        self.history = [Message.from_json(msg, self) for msg in messages_data]

    def send_message(self, message):
        """
        Send a user message to the chat.

        Parameters
        ----------
        message : str
            The message to be sent.

        Returns
        -------
        Message
            The message object representing the assistant's response.
        """
        if self.ended:
            raise ValueError("Chat has ended.")

        url = f"{self.base_url}/chats/{self.chat_id}/"
        headers = {"Content-Type": "application/json", "X-Api-Key": self.tenant}
        payload = {"message": message}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        self._update_chat_info(**response.json())
        return self.history[-1]

    def __repr__(self):
        return f"Chat(chat_id={self.chat_id}, title={self.title}, ended={self.ended})"


class Message:
    """
    A class used to represent a Message.
    
    Attributes
    ----------
    chat : Chat
        The chat object associated with the message.
    role : str
        The role of the message sender (e.g., "user", "assistant").
    content : str
        The content of the message.
    msg_num : int
        The message number in the conversation.
    references : list of Reference
        A list of Reference objects related to the message.
    """
    def __init__(self, chat, role, content, msg_num, references):
        """
        Parameters
        ----------
        chat : Chat
            The chat object associated with the message.
        role : str
            The role of the message sender (e.g., "user", "assistant").
        content : str
            The content of the message.
        msg_num : int
            The message number in the conversation.
        references : list of Reference
            A list of Reference objects related to the message.
        """
        self.chat = chat
        self.role = role
        self.content = content
        self.msg_num = msg_num
        self.references = [Reference.from_json(ref, self) for ref in references] if references else []

    @classmethod
    def from_json(cls, data, chat=None):
        return cls(
            chat=chat,
            role=data.get("role"),
            content=data.get("content"),
            msg_num=data.get("msg_num"),
            references=data.get("references", []),
        )

    def __repr__(self):
        return f"Message(role={self.role}, content={self.content}, msg_num={self.msg_num})"


class Reference:
    """
    A class used to represent a Reference related to a Message.
    
    Attributes
    ----------
    message : Message
        The message object associated with the reference.
    reference_num : int
        The reference number.
    source : str
        The source of the reference.
    showed_num : int, optional
        The number displayed for the reference.
    """
    def __init__(self, message, reference_num, source, showed_num=None):
        """
        Parameters
        ----------
        message : Message
            The message object associated with the reference.
        reference_num : int
            The reference number.
        source : str
            The source of the reference.
        showed_num : int, optional
            The number displayed for the reference.
        """
        self.message = message
        self.reference_num = reference_num
        self.source = source
        self.showed_num = showed_num

    @classmethod
    def from_json(cls, data, message=None):
        return cls(
            message=message,
            reference_num=data.get("reference_num"),
            source=data.get("source"),
            showed_num=data.get("showed_num")
        )

    def __repr__(self):
        return f"Reference(reference_num={self.reference_num}, source={self.source}, showed_num={self.showed_num})"
    