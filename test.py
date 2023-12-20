import unittest
from openai import OpenAI
from dotenv import load_dotenv
import os
from message import *

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

load_dotenv()

class TestOpenAIResponse(unittest.TestCase):
    def test_aip_connection(self):

        prompt = "hello"

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

        self.assertEqual(full_prompt, f"{prompt} {message.cite_sources_prompt()}")

    def test_response_includes_citation(self):
        sample_prompt = "Explain the theory of relativity"
        message = Message(sample_prompt)
        response = message.ask_client()
        response_text = response.choices[0].text

        self.assertIn("citation", response_text.lower(), "Response should include the <citations:> tag")


if __name__ == '__main__':
    unittest.main()
