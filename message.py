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
        return f"{self.pre_prompt()} {self.prompt} {self.cite_sources_prompt()}"

    def cite_sources_prompt(self):
        """
        Returns the cite sources prompt text string
        """
        return (
            "after each statement of your response please cite your sources. Use the following "
            "format <citations:>"
        )

    def pre_prompt(self):
        """
        Returns the pre-prompt text string
        """
        return (
            "Pretend you are an expert research scientist with 20 years of experience teaching as "
            "a college professor. I am a freshman college student interested in your research "
            "please teach me starting with simple concepts and building more complexity as you go. "
            "Please refer to me as 'my dedicated student' when you begin your response"
        )
