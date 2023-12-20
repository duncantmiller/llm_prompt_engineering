import unittest
from message import *

class TestClient(unittest.TestCase):
    def test_aip_connection(self):
        prompt = "hello"
        client = Client().openai_client
        response = client.completions.create(model="text-davinci-003",
                                             prompt=prompt,
                                             max_tokens=1000)

        self.assertTrue(response)

class TestMessage(unittest.TestCase):
    def test_ask_client(self):
        message = Message("hello")
        response = message.ask_client()

        self.assertTrue(response)

    def test_full_prompt(self):
        prompt = "hello"
        message = Message(prompt)
        full_prompt = message.full_prompt()

        self.assertEqual(full_prompt, f"{prompt} {message.cite_sources_prompt()}")

    def test_full_prompt(self):
        prompt = "hello"
        message = Message(prompt)
        full_prompt = message.full_prompt()

        self.assertEqual(
            full_prompt, f"{message.pre_prompt()} {prompt} {message.cite_sources_prompt()}"
        )

    def test_response_includes_citation(self):
        sample_prompt = "Explain the theory of relativity"
        message = Message(sample_prompt)
        response = message.ask_client()
        response_text = response.choices[0].text

        self.assertIn(
            "citation", response_text.lower(), "Response should include the <citations:> tag"
        )

    def test_default_does_not_include_citation(self):
        sample_prompt = "Explain the theory of relativity"
        client = Client().openai_client
        response = client.completions.create(model="text-davinci-003",
                                             prompt=sample_prompt,
                                             max_tokens=1000)
        response_text = response.choices[0].text

        self.assertNotIn(
            "citation", response_text.lower(), "Response should not include the <citations:> tag"
        )

    def test_response_includes_pre_prompt(self):
        sample_prompt = "Explain the theory of relativity"
        message = Message(sample_prompt)
        response = message.ask_client()
        response_text = response.choices[0].text

        self.assertIn("my dedicated student",
                      response_text.lower(),
                      "Response should comply with pre_prompt instructions")

    def test_default_does_not_include_pre_prompt(self):
        sample_prompt = "Explain the theory of relativity"
        client = Client().openai_client
        response = client.completions.create(model="text-davinci-003",
                                             prompt=sample_prompt,
                                             max_tokens=1000)
        response_text = response.choices[0].text

        self.assertNotIn("my dedicated student",
                response_text.lower(),
                "Response should not include pre_prompt instructions")

if __name__ == '__main__':
    unittest.main()
