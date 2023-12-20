from client import Client

class Message():
    def __init__(self):
        client = Client()
        self.client = client.openai_client

    def ask_client(self, prompt):
        response = self.client.completions.create(model="text-davinci-003",
                                                prompt=prompt,
                                                max_tokens=100)
        return response
