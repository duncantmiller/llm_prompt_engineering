import unittest
from message import *

class BaseTestCase(unittest.TestCase):
    def default_response_davinci(self, prompt):
        client = Client().openai_client
        response = client.completions.create(model=Client.MODEL_TEXT_DAVINCI,
                                             prompt=prompt,
                                             max_tokens=1000)
        return response

    def custom_response(self, model, message):
        response = message.ask_client(model)
        return response

class TestClient(BaseTestCase):
    def test_api_connection(self):
        prompt = "hello"
        response = self.default_response_davinci(prompt)

        self.assertTrue(response)

class TestMessage(BaseTestCase):
    def setUp(self):
        self.prompt = "hello"
        self.message = Message(self.prompt)

    def test_ask_client_davinci(self):
        response = self.custom_response(model=Client.MODEL_TEXT_DAVINCI, message=self.message)

        self.assertTrue(response, "Client should return a response for Davinci")

    def test_ask_client_gpt_35(self):
        response = self.custom_response(model=Client.MODEL_GPT_35, message=self.message)

        self.assertTrue(response, "Client should return a response for GPT-35")

    def test_ask_client_not_implemented(self):
        """NotImplementedError should be raised if not one of the accepted models"""
        with self.assertRaises(NotImplementedError):
            self.message.ask_client("Foo")

    def test_full_prompt(self):
        full_prompt = self.message.full_prompt()

        self.assertEqual(
            full_prompt,
            f"{self.message.pre_prompt()} {self.prompt} {self.message.cite_sources_prompt()}",
            "Full prompt should include pre_prompt, prompt, and cite_sources_prompt"
        )

class TestMessageDavinciResponse(BaseTestCase):
    def setUp(self):
        sample_prompt = "Explain the theory of relativity"
        message = Message(sample_prompt)
        response = self.custom_response(model=Client.MODEL_TEXT_DAVINCI, message=message)
        self.response_text = response.choices[0].text

    def test_response_includes_citation(self):
        self.assertIn(
            "citation", self.response_text.lower(), "Response should include the <citation:> tag"
        )

    def test_response_includes_pre_prompt(self):
        self.assertIn("my dedicated student",
                      self.response_text.lower(),
                      "Response should comply with pre_prompt instructions")

class TestMessageGPT35Response(BaseTestCase):
    def setUp(self):
        sample_prompt = "Explain the theory of relativity"
        message = Message(sample_prompt)
        response = self.custom_response(model=Client.MODEL_GPT_35, message=message)

        self.response_text = response.choices[0].message.content

    def test_response_includes_citation(self):
        self.assertIn(
            "citation", self.response_text.lower(), "Response should include the <citation:> tag"
        )

    def test_response_includes_pre_prompt(self):
        self.assertIn("my dedicated student",
                      self.response_text.lower(),
                      "Response should comply with pre_prompt instructions")

class TestDefaultResponseDavinci(BaseTestCase):
    def setUp(self):
        sample_prompt = "Explain the theory of relativity"
        response = self.default_response_davinci(sample_prompt)

        self.response_text = response.choices[0].text

    def test_does_not_include_citation(self):
        self.assertNotIn(
            "citation", self.response_text.lower(), "Response should not include the <citation:> tag"
        )

    def test_does_not_include_pre_prompt(self):
        self.assertNotIn("my dedicated student",
                self.response_text.lower(),
                "Response should not include pre_prompt instructions")

class TestDefaultResponseGPT35(unittest.TestCase):
    def setUp(self):
        sample_prompt = "Explain the theory of relativity"
        client = Client().openai_client
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": sample_prompt,
                }
            ],
            model=Client.MODEL_GPT_35,
        )
        self.response_text = response.choices[0].message.content

    def test_does_not_include_citation(self):
        self.assertNotIn(
            "citation", self.response_text.lower(), "Response should not include the <citation:> tag"
        )

    def test_does_not_include_pre_prompt(self):
        self.assertNotIn("my dedicated student",
                self.response_text.lower(),
                "Response should not include pre_prompt instructions")

if __name__ == '__main__':
    unittest.main()
