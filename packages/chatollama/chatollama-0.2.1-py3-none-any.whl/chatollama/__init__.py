from dataclasses import dataclass
import inspect
from typing import Callable, List, Any
import ollama
from typing import List, Optional


class MessageNode:
    def __init__(self, role: str, content: str, parent: Optional['MessageNode'] = None):
        self.role = role
        self.content = content
        self.parent = parent
        self.children: List['MessageNode'] = []

    def __str__(self):
        return f"[{self.role}]: {self.content}"


class Conversation:
    def __init__(self):
        self.root = MessageNode(role='root', content='')
        self.current_node = self.root

    def add_message(self, role: str, content: str) -> MessageNode:
        """Adds a message to the current active path."""
        if not isinstance(role, str):
            raise ValueError(f"'role' must be a string, got {
                             type(role).__name__}")
        if not isinstance(content, str):
            raise ValueError(f"'content' must be a string, got {
                             type(content).__name__}")

        new_node = MessageNode(role=role, content=content,
                               parent=self.current_node)
        self.current_node.children.append(new_node)
        self.current_node = new_node
        return new_node

    def branch_message(self, node: MessageNode, role: str, content: str) -> MessageNode:
        """
        Creates a new branch at the same level as the specified node.
        The new node becomes a sibling of the specified node.
        """
        if node.parent is None:
            raise ValueError("Cannot branch at the root node.")

        if not isinstance(role, str):
            raise ValueError(f"'role' must be a string, got {
                             type(role).__name__}")
        if not isinstance(content, str):
            raise ValueError(f"'content' must be a string, got {
                             type(content).__name__}")

        new_node = MessageNode(role=role, content=content, parent=node.parent)
        node.parent.children.append(new_node)
        return new_node

    def set_active_path(self, node: MessageNode):
        """Sets the active node to the specified node."""
        if not self._is_node_in_tree(node):
            raise ValueError(
                "The specified node is not part of the conversation tree.")
        self.current_node = node

    def get_active_path(self) -> List[MessageNode]:
        """Returns the list of nodes from root to the current active node."""
        path: List[MessageNode] = []
        node = self.current_node
        while node:
            path.append(node)
            node = node.parent
        if len(path) > 0:
            if path[-1].role == "root":
                path.pop()
        return list(reversed(path))

    def traverse_tree(self, node: Optional[MessageNode] = None):
        """Traverses the entire conversation tree."""
        if node is None:
            node = self.root
        yield node
        for child in node.children:
            yield from self.traverse_tree(child)

    def _is_node_in_tree(self, node: MessageNode) -> bool:
        """Checks if a node is part of the conversation tree."""
        current = node
        while current:
            if current is self.root:
                return True
            current = current.parent
        return False

    def print_tree(self, node: MessageNode, indent: int = 0):
        """Prints the conversation tree starting from the given node."""
        print('    ' * indent + str(node))
        for child in node.children:
            self.print_tree(child, indent + 1)

    def system(self, content: str):
        return self.add_message(role="system", content=content)

    def assistant(self, content: str):
        return self.add_message(role="assistant", content=content)

    def user(self, content: str):
        return self.add_message(role="user", content=content)


class Event:
    def __init__(self):
        self.callbacks: List[Callable[..., Any]] = []

    def on(self, callback: Callable[..., Any]) -> None:
        self.callbacks.append(callback)

    def trigger(self, *args: Any, **kwargs: Any) -> List[Any]:
        results = []
        for callback in self.callbacks:
            # Get the signature of the callback function
            signature = inspect.signature(callback)
            parameters = signature.parameters

            # Filter `args` and `kwargs` to match the number of parameters in the callback
            required_args = len([p for p in parameters.values(
            ) if p.default == p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)])
            limited_args = args[:required_args]

            # Filter kwargs based on the callback's parameters
            limited_kwargs = {k: v for k,
                              v in kwargs.items() if k in parameters}

            # Bind the filtered args and kwargs to the function signature
            bound_args = signature.bind_partial(
                *limited_args, **limited_kwargs)
            bound_args.apply_defaults()  # Fill missing parameters with defaults or None

            # Call the callback with the matched arguments
            result = callback(*bound_args.args, **bound_args.kwargs)
            results.append(result)
        return results

    def call(self, *args: Any, **kwargs: Any) -> List[Any]:
        results = []
        for callback in self.callbacks:
            # Call each callback with all arguments; each callback will handle what it needs
            result = callback(*args, **kwargs)
            results.append(result)
        return results


@dataclass
class GenerationParameters:
    # Controls randomness; range 0.0-1.0. Lower is more predictable, higher is more creative.
    temperature: float = 0.7

    # Limits token choices to the top k options; range 0-100. Lower is more focused, higher is more diverse.
    top_k: int = 50

    # Probability threshold for token choices; range 0.0-1.0. Lower focuses on most probable words.
    top_p: float = 1.0

    # Reduces word repetition; range 0.0-2.0. Higher values make responses less repetitive.
    frequency_penalty: float = 0

    # Encourages new words/topics; range 0.0-2.0. Higher values make responses more varied.
    presence_penalty: float = 0

    def to_dict(self):
        return {
            'temperature': self.temperature,
            'top_k': self.top_k,
            'top_p': self.top_p,
            'frequency_penalty': self.frequency_penalty,
            'presence_penalty': self.presence_penalty
        }

    def creative(self):
        """Configures settings for highly creative, varied responses."""
        self.temperature = 0.9
        self.top_k = 80
        self.top_p = 0.9
        self.frequency_penalty = 0.2
        self.presence_penalty = 0.5
        return self

    def coding(self):
        """Configures settings for focused, precise responses suitable for technical or coding answers."""
        self.temperature = 0.2
        self.top_k = 20
        self.top_p = 0.8
        self.frequency_penalty = 0
        self.presence_penalty = 0
        return self

    def informative(self):
        """Configures settings for clear, informative responses with minimal creativity."""
        self.temperature = 0.3
        self.top_k = 40
        self.top_p = 0.9
        self.frequency_penalty = 0
        self.presence_penalty = 0
        return self

    def conversational(self):
        """Configures settings for natural, engaging conversation flow."""
        self.temperature = 0.7
        self.top_k = 60
        self.top_p = 0.95
        self.frequency_penalty = 0.2
        self.presence_penalty = 0.3
        return self

    def story_telling(self):
        """Configures settings for imaginative storytelling and longer responses."""
        self.temperature = 1.0
        self.top_k = 100
        self.top_p = 0.85
        self.frequency_penalty = 0.5
        self.presence_penalty = 0.6
        return self
    
    def brute(self):
        """Configures settings for a brutish style of responses"""
        self.temperature = 0
        self.top_k = 1
        self.top_p = 0
        self.frequency_penalty = 0
        self.presence_penalty = 0
        return self


class Engine:
    def __init__(self, model: str = "llama3.1:8b"):
        self.model = model
        self.conversation = Conversation()
        self.message_attributes = ["role", "content"]
        self.tools = []
        self.use_tools = False
        self.stream = False
        self.format = ''
        self.options = GenerationParameters()

        self.keep_alive = -1

        self.response_event = Event()
        self.stream_event = Event()
        self.tool_event = Event()

        self.print_if_loading = True

    def system(self, content: str):
        return self.conversation.system(content=content)

    def assistant(self, content: str):
        return self.conversation.assistant(content=content)

    def user(self, content: str):
        return self.conversation.user(content=content)

    def get_messages(self):
        return self.conversation.get_active_path()

    def get_ollama_messages(self):
        messages = self.get_messages()
        ollama_messages = []
        for message in messages:
            ollama_message = {}
            for element in self.message_attributes:
                if hasattr(message, element):
                    data = getattr(message, element)
                    ollama_message[element] = str(data)
            ollama_messages.append(ollama_message)

        return ollama_messages

    def chat(self):
        """Progresses the conversation allowing the model to respond and store the response into the conversation"""

        models = ollama.ps()
        models = models.get("models", [])

        if self.print_if_loading:
            found = False
            for model in models:
                name = model.get("name", None)
                model_name = model.get("model", None)
                if self.model == name or self.model == model_name:
                    found = True
                    break

            if not found:
                print(f"Model: [{self.model}] is loading...")

        messages = self.get_ollama_messages()

        self.stream_stop = False

        response = ollama.chat(
            model=self.model,
            messages=messages,
            tools=self.tools if self.use_tools else None,
            stream=False if self.use_tools else self.stream,
            format=self.format,
            options=self.options.to_dict(),
            keep_alive=self.keep_alive
        )

        self.on_response(response)

    def on_response(self, response):
        if self.use_tools:
            self.tool_event.trigger(tool_calls=response.get(
                "message", {}).get("tool_calls", {}), response=response)
        elif self.stream:
            if self.stream_stop:
                return
            self.stream_event.trigger(mode=0, delta="", text="", response=None)
            text = ""
            for chunk in response:
                if self.stream_stop:
                    return
                delta = chunk.get("message", {}).get("content", {})
                text += delta
                self.stream_event.trigger(
                    mode=1, delta=delta, text=text, response=chunk)
            if self.stream_stop:
                return
            self.stream_event.trigger(
                mode=2, delta="", text=text, response=None)
        else:
            self.response_event.trigger(message=response.get(
                "message", {}).get("content", {}), response=response)

    def prompt(self, message: str, **kwargs):
        """Sends a single message to the model, its a temporary message that is not stored into the conversation"""
        pass

    def vision_model(self, has_vision: bool = True):
        """Set if the model has vision abilities. If true, the engine will pass the 'images' element in a message to the model on inference"""
        if has_vision:
            # Add 'images' if not already present
            if 'images' not in self.message_attributes:
                self.message_attributes.append('images')
        else:
            # Remove 'images' if present
            if 'images' in self.message_attributes:
                self.message_attributes.remove('images')

    def unload(self):
        """
        This function tries unloading the model by setting the keep_alive value to 0
        However it requires one more call to the model using an empty conversation with the singular instruction:
        'Respond with just the word "stop"'
        This has a high chance of working but a low chance the model says more than just stop. So the function might not finish instantly
        It also uses its own settings for the model so no tools, no format, no stream...etc
        """
        options = {
            'temperature': 0.1,
            'top_p': 1.0,
            'frequency_penalty': 0,
            'presence_penalty': 0
        }
        ollama.chat(
            self.model, [{"role": "user", "content": "Respond with just the word 'stop'"}], options=options, keep_alive=0)
