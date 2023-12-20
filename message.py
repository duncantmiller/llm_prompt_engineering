from client import Client

class Message():
    def __init__(self, prompt):
        client = Client()
        self.client = client.openai_client
        self.prompt = prompt

    def ask_client(self):
        """
        Sends the prompt to the LLM client and returns the response
        """
        response = self.client.completions.create(model="text-davinci-003",
                                                prompt=self.prompt,
                                                max_tokens=100)
        return response
