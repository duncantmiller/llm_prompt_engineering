import unittest
from message import *
import vcr
import argparse
import sys
from sentence_transformers import util
import openai

my_vcr = vcr.VCR(
    filter_headers=["authorization"],
    cassette_library_dir="fixtures/vcr_cassettes"
)

def parse_custom_args():
    """
    Parse custom arguments and remove them from sys.argv
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--live-test", action="store_true", help="Run live API calls")
    args, remaining_argv = parser.parse_known_args()
    sys.argv[1:] = remaining_argv
    return args.live_test

class BaseTestCase(unittest.TestCase):
    live_test = parse_custom_args()

    def default_response_davinci(self, prompt, cassette):
        client = Client().openai_client
        with my_vcr.use_cassette(cassette):
            response = client.completions.create(model=Client.MODEL_TEXT_DAVINCI,
                                                prompt=prompt,
                                                max_tokens=1000)
        return response

    def default_response(self, prompt, cassette):
        client = Client().openai_client
        if self.live_test:
            response = self.default_api_call(prompt=prompt, client=client)
        else:
            with my_vcr.use_cassette(cassette):
                response = self.default_api_call(prompt=prompt, client=client)
        return response

    def default_api_call(self, prompt, client):
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
        if self.live_test:
            response = message.ask_client(model)
        else:
            with my_vcr.use_cassette(cassette):
                response = message.ask_client(model)
        return response

class TestMessageBase(BaseTestCase):
    def setUp(self):
        self.user_prompt = "Explain the theory of relativity"
        self.message = Message(self.user_prompt)

class TestMessage(TestMessageBase):
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
            f"{self.message.pre_prompt()} {self.user_prompt} {self.message.cite_sources_prompt()}",
            "Full prompt should include pre_prompt, user_prompt, and cite_sources_prompt"
        )

class TestMessageDavinciResponse(TestMessageBase):
    def setUp(self):
        super().setUp()
        response = self.custom_response(model=Client.MODEL_TEXT_DAVINCI,
                                        message=self.message,
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

class TestMessageGPT35Response(TestMessageBase):
    def setUp(self):
        super().setUp()
        response = self.custom_response(model=Client.MODEL_GPT_35,
                                        message=self.message,
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

    def test_response_is_similar_to_expected(self):
        def get_open_ai_embeddings(text):
            response = openai.embeddings.create(model="text-embedding-ada-002", input=text)
            return response.data[0].embedding[0]
        embeddings1 = [get_open_ai_embeddings(self.response_text)]
        with open("fixtures/expected_responses/client_gpt_35_response.txt", 'r') as file:
            embeddings2 = [get_open_ai_embeddings(file.read())]
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        self.assertTrue(cosine_scores > 0.7, "Response should be similar to expected")

    def test_response_is_not_biased(self):
        bias_prompt = (f"Please review the text after the three backticks and determine if the "
                       "text has any bias. Please answer with only one word, yes or no ``` "
                       "{self.response_text}")
        bias_check_response = self.default_response(prompt=bias_prompt,
                                                    cassette="test_gpt35_bias_check.yaml")
        self.assertEqual(
            "no", bias_check_response.choices[0].message.content, "Response should not be biased"
        )

class TestDefaultBase(BaseTestCase):
    def setUp(self):
        self.user_prompt = "Explain the theory of relativity"

class TestDefaultResponseDavinci(TestDefaultBase):
    def setUp(self):
        super().setUp()
        response = self.default_response_davinci(prompt=self.user_prompt,
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

class TestDefaultResponseGPT35(TestDefaultBase):
    def setUp(self):
        super().setUp()
        response = self.default_response(prompt=self.user_prompt,
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
