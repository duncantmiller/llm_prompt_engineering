from client import Client

class Message():
    def __init__(self, prompt):
        client = Client()
        self.client = client.openai_client
        self.prompt = prompt

    def ask_client(self, model):
        """
        Sends the prompt to the LLM client and returns the response
        """
        if model == Client.MODEL_TEXT_DAVINCI:
            response = self.client.completions.create(model=model,
                                                      prompt=self.full_prompt(),
                                                      max_tokens=1000)
        elif model == Client.MODEL_GPT_35:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": self.full_prompt(),
                    }
                ],
                model=Client.MODEL_GPT_35,
            )
        else:
            raise Exception(f"{model} not implemented")

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
            "after each sentence in your response please cite your sources. Use the following "
            "format delineated by the three ticks ```citation: <source>``` where <source> is your "
            "source for the information. Please make sure you always include citations, its very "
            "important. Take your time and make sure you follow all of these instructions."
        )

    def pre_prompt(self):
        """
        Returns the pre-prompt text string
        """
        return (
            "Pretend you are an expert research scientist with 20 years of experience teaching as "
            "a college professor. I am a freshman college student interested in your research "
            "please teach me starting with simple concepts and building more complexity as you go. "
            "Please refer to me as 'my dedicated student' when you begin your response. Please "
            "make sure you always start with 'my dedicated student' its very important."
        )
