import unittest
from message import *

class TestClient(unittest.TestCase):
    def test_api_connection(self):
        prompt = "hello"
        client = Client().openai_client
        response = client.completions.create(model="text-davinci-003",
                                             prompt=prompt,
                                             max_tokens=1000)

        self.assertTrue(response)

class TestMessage(unittest.TestCase):
    def setUp(self):
        self.prompt = "hello"
        self.message = Message(self.prompt)

    def test_ask_client(self):
        response = self.message.ask_client()

        self.assertTrue(response)

    def test_full_prompt(self):
        full_prompt = self.message.full_prompt()

        self.assertEqual(
            full_prompt,
            f"{self.message.pre_prompt()} {self.prompt} {self.message.cite_sources_prompt()}"
        )

class TestMessageResponse(unittest.TestCase):
    def setUp(self):
        sample_prompt = "Explain the theory of relativity"
        message = Message(sample_prompt)
        response = message.ask_client()
        self.response_text = response.choices[0].text

    def test_response_includes_citation(self):
        self.assertIn(
            "citation", self.response_text.lower(), "Response should include the <citations:> tag"
        )

    def test_response_includes_pre_prompt(self):
        self.assertIn("my dedicated student",
                      self.response_text.lower(),
                      "Response should comply with pre_prompt instructions")

class TestDefaultResponse(unittest.TestCase):
    def setUp(self):
        sample_prompt = "Explain the theory of relativity"
        client = Client().openai_client
        response = client.completions.create(model="text-davinci-003",
                                             prompt=sample_prompt,
                                             max_tokens=1000)
        self.response_text = response.choices[0].text

    def test_does_not_include_citation(self):
        self.assertNotIn(
            "citation", self.response_text.lower(), "Response should not include the <citations:> tag"
        )

    def test_does_not_include_pre_prompt(self):
        self.assertNotIn("my dedicated student",
                self.response_text.lower(),
                "Response should not include pre_prompt instructions")

if __name__ == '__main__':
    unittest.main()
