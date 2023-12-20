import unittest
from openai import OpenAI
from dotenv import load_dotenv
import os
from main import *

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

load_dotenv()

class TestOpenAIResponse(unittest.TestCase):
    def test_aip_connection(self):

        prompt = "hello"

        response = client.completions.create(model="text-davinci-003",
                                             prompt=prompt,
                                             max_tokens=100)

        self.assertTrue(response)

class TestMain(unittest.TestCase):
    def test_ask_client(self):
        response = ask_client("hello")

        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
