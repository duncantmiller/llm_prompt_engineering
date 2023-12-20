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
                                                prompt=self.full_prompt(),
                                                max_tokens=100)
        return response

    def full_prompt(self):
        """
        Returns the full prompt including cite sources
        """
        return f"{self.prompt} {self.cite_sources_prompt()}"

    def cite_sources_prompt(self):
        """
        Returns the cite sources prompt
        """
        return (
            "after each statement of your response please cite your sources. Use the following "
            "format <citations:>"
        )
