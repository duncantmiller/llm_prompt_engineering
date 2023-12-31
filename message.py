from client import Client

class Message():
    SUPPORTED_GPT_MODELS = [Client.MODEL_GPT_35, Client.MODEL_GPT_4]
    LEGACY_CHAT_MODELS = [Client.MODEL_TEXT_DAVINCI]

    def __init__(self, prompt):
        client = Client()
        self.client = client.openai_client
        self.user_prompt = prompt

    def ask_client(self, model):
        """
        Sends the prompt to the LLM client and returns the response
        """
        if model in Message.LEGACY_CHAT_MODELS:
            response = self.legacy_chat_completion(model)
        elif model in Message.SUPPORTED_GPT_MODELS:
            response = self.chat_completion(model)
        else:
            raise NotImplementedError(f"{model} not implemented")

        return response

    def chat_completion(self, model):
        """
        Sends the prompt using the new openAI format and returns the response.
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": self.full_prompt()
                }
            ],
            model=model
        )
        return response

    def legacy_chat_completion(self, model):
        """
        Sends the prompt to using the legacy openAI format returns the response
        """
        response = self.client.completions.create(model=model,
                                                  prompt=self.full_prompt(),
                                                  max_tokens=1000)

        return response

    def full_prompt(self):
        """
        Returns the full prompt including pre_prompt and cite sources
        """
        return f"{self.pre_prompt()} {self.user_prompt} {self.cite_sources_prompt()}"

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
