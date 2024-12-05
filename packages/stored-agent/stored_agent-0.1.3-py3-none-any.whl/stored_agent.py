import json
import fs

class StoredAgent:
    """
    A class for building agents that persist state between interactions.
    """
    def __init__(self, id: str, storage_backend: str = 'osfs://.', **kwargs):
        """
        Initialize the agent. If the agent state file exists, load it.
        Otherwise, save the current state.

        Args:
            id (str): Unique identifier for the agent
            storage_backend (str): The storage backend to use for the agent state. Defaults to 'osfs://.'
            **kwargs: Additional attributes to store on the agent
        """
        self.id = id
        self.filesystem = fs.open_fs(storage_backend)

        # Store all other kwargs as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

        # If the agent state file exists, load it
        try:
            self.load(id)
        except (FileNotFoundError, fs.errors.ResourceNotFound):
            pass
        self.save()

    def save(self):
        # Save the agent state as JSON to a file, excluding non-serializable attributes
        data = {k: v for k, v in self.__dict__.items() if k != 'filesystem'}
        with self.filesystem.open(f'{self.id}.json', 'w') as f:
            json.dump(data, f)

    def load(self, id: str):
        # Load the agent state from a JSON file
        with self.filesystem.open(f'{id}.json', 'r') as f:
            data = json.load(f)
        self.__dict__.update(data)

    def process(self, input: str):
        # Print the agent's attributes
        print(self.__dict__, input)
        return input

    def invoke(self, input: str):
        # Load the agent state from the file
        self.load(self.id)
        # Invoke the agent with input
        output = self.process(input)
        # Save the agent state to the file
        self.save()
        return output