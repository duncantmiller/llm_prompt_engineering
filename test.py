import unittest
from message import *
import vcr
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--live-test', action='store_true', help='Run live API calls')
args, _ = parser.parse_known_args()

class BaseTestCase(unittest.TestCase):
    def default_response_davinci(self, prompt, cassette):
        client = Client().openai_client
        with vcr.use_cassette(cassette):
            response = client.completions.create(model=Client.MODEL_TEXT_DAVINCI,
                                                prompt=prompt,
                                                max_tokens=1000)
        return response

    def default_response(self, prompt, cassette):
        client = Client().openai_client
        with vcr.use_cassette(cassette):
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=Client.MODEL_GPT_35,
            )
        return response

    def custom_response(self, model, message, cassette):
        with vcr.use_cassette(cassette):
            response = message.ask_client(model)
        return response

class TestClient(BaseTestCase):
    def test_api_connection(self):
        prompt = "hello"
        response = self.default_response_davinci(prompt=prompt,
                                                 cassette="test_api_connection.yaml")

        self.assertTrue(response)

class TestMessage(BaseTestCase):
    def setUp(self):
        self.prompt = "hello"
        self.message = Message(self.prompt)

    def test_ask_client_davinci(self):
        response = self.custom_response(model=Client.MODEL_TEXT_DAVINCI,
                                        message=self.message,
                                        cassette="test_ask_client_davinci.yaml")

        self.assertTrue(response, "Client should return a response for Davinci")

    def test_ask_client_gpt_35(self):
        response = self.custom_response(model=Client.MODEL_GPT_35,
                                        message=self.message,
                                        cassette="test_ask_client_gpt_35.yaml")

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
        response = self.custom_response(model=Client.MODEL_TEXT_DAVINCI,
                                        message=message,
                                        cassette="test_davinci_response_includes.yaml")
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
        response = self.custom_response(model=Client.MODEL_GPT_35,
                                        message=message,
                                        cassette="test_gpt35_response_includes.yaml")

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
        response = self.default_response_davinci(prompt=sample_prompt,
                                                 cassette="test_default_response_davinci.yaml")

        self.response_text = response.choices[0].text

    def test_does_not_include_citation(self):
        self.assertNotIn(
            "citation", self.response_text.lower(), "Response should not include the <citation:> tag"
        )

    def test_does_not_include_pre_prompt(self):
        self.assertNotIn("my dedicated student",
                self.response_text.lower(),
                "Response should not include pre_prompt instructions")

class TestDefaultResponseGPT35(BaseTestCase):
    def setUp(self):
        sample_prompt = "Explain the theory of relativity"
        response = self.default_response(prompt=sample_prompt,
                                         cassette="test_default_response_gpt35.yaml")
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
