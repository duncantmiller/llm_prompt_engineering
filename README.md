# Prompt Engineering Testing Strategies

This is an example project showing prompt engineering testing strategies, using the OpenAI API.

This code demonstrates how I ensure the high quality of the prompts I create. The [test.py](https://github.com/duncantmiller/llm_prompt_engineering/blob/main/test.py) file shows a series of tests I wrote for the project using test-driven development. These tests helped me to repeatedly test a system where a user prompt is augmented by additional prompts, including a [pre_prompt](https://github.com/duncantmiller/llm_prompt_engineering/blob/15c2ffe4c476f0a1ae563ffb8498320069c14c1b/message.py#L64) and a [cite_sources_prompt](https://github.com/duncantmiller/llm_prompt_engineering/blob/15c2ffe4c476f0a1ae563ffb8498320069c14c1b/message.py#L53) which provide additional instruction to the LLM beyond the user prompt.

This automated test suite makes it easier for me to hone prompts or switch models (text-davinci-003 to gpt-3.5-turbo) and ensure that the prompts provide a consistent response. It also enables me to monitor for ethical and bias mitigation and model drift over time.

This is a simplified version of the logic used in [OpenShiro](https://openshiro.com) prompts for educational purposes. The full product involves many more parameters including additional model versions, additional APIs like Azure, Google, HuggingFace, Anthropic and Cohere, and a library of pre-formatted prompts from which the users can select.

## Usage
Clone the repository with `git clone git@github.com:duncantmiller/llm_prompt_engineering.git` then change to the project directory with `cd llm_prompt_engineering`.

Use if you use [pipenv](https://pypi.org/project/pipenv/) you can install the dependencies with `pipenv install`, otherwise use `pip install -r requirements.txt`. Note that due to a PyTorch dependency via sentence-transformers (used for similarity testing), the latest Python version that can be used is `3.11.7`.

The tests use [vcrpy](https://github.com/kevin1024/vcrpy) to record and replay the interactions with the OpenAI API. To run the tests, execute the command `python test.py`.

It can also be helpful to run the tests against the live OpenAI API. Note that when your run tests against the live API you will need an OpenAI API key and it will incur a cost. Also the tests will take much longer to run (approximately 93.5s using the live API vs 0.2s using the vcr cassette responses on my machine). To run the tests against the live API follow these steps:

- Copy the .env_example file and rename it as .env with `cp .env_example .env` (Linux/macOS) or `copy .env_example .env` (Windows)
- Open the .env file and enter the value for your OpenAI API Key for the `OPENAI_API_KEY=` variable. For example if your API key is 'foo' then `OPENAI_API_KEY=foo`
- Run the tests with the command line flag `python test.py --live-test`

### Re-recording Cassettes

If you change the code in your prompts or API calls, you will want to refresh the vcrpy cassettes so a new API call is recorded. To do this simply delete the appropriate .yaml cassette files in the fixtures/vcr_cassettes directory. You can also optionally set a `re_record_interval` in the `vcr` command. For example to re-record every 7 days:

````
with vcr.use_cassette('cassette_name.yaml', re_record_interval=7*24*60*60):
    # API call goes here
````

## Test Documentation

The following is a review of all tests and methods used in the test.py file.

##### `parse_custom_args()`:
Parses `--live-test` flag for live API calls. If the `--live-test` flag is present, then live API calls will be made. If the flag is not present, then the tests will use the responses recorded in vcrpy cassetts.

### BaseTestCase
Base class for all test cases with common testing methods.

##### `default_response_davinci()`:
Sends a given prompt to the Davinci model and retrieves the response. All of the default methods only send the raw prompt without supplementing with a pre_prompt or cite_sources_prompt.

##### `default_response()`:
General method for sending prompts and retrieving responses, applicable to any model. It chooses between live API calls and recorded responses based on the `live_test` flag.

##### `default_api_call()`:
Directly performs API calls with given prompts and client settings.

##### `custom_response()`:
Uses the `Message()` object to send the `full_prompt()` to a specified model and retrieves the response, considering the `live_test` setting. The `full_prompt()` method defined in the `Message()` class does supplement the provided user prompt with the `pre_prompt()` and `cite_sources_prompt()`.

### TestClient

##### `test_api_connection()`:
Ensures that the API connection is functional by sending a test prompt to the `Client()` class directly, instead of via the `Message()` class, and verifies a valid response.

### TestMessageDavinciResponse
Uses the `Message()` object to send the `full_prompt()` to the Davinci model.

##### `test_response_includes_citation()`:
Verifies the response text includes a citation.

##### `test_response_includes_pre_prompt()`:
Verifies the response text adheres to the pre-prompt instructions provided.

### TestMessageGPT35Response
Uses the `Message()` object to send the `full_prompt()` to the GPT-3.5 model.

##### `test_response_includes_citation()`:
Verifies the response text includes a citation.

##### `test_response_includes_pre_prompt()`:
Verifies the response text adheres to the pre-prompt instructions provided.

##### `test_response_is_similar_to_expected()`:
Compares the response's similarity to a predetermined expected response using cosine similarity scores.
- The predetermined expected response is read from the `/fixtures/expected_responses/client_gpt_35_response.txt` file. Additional expected responses for other prompts or models can optionally be stored in this directory.
- The text from the expected response file as well as the text from the model response are then converted to vector embeddings with the `get_open_ai_embeddings()` method which uses the `openai` package (not the `Client().openai_client`) to generate embeddings.
- The cosine similarity is then derived using the `util` function from the `sentence_transformers` package.

##### `test_response_is_not_biased()`:
Assesses the response for any potential biases. This method takes the response from the model, then feeds the response back to the model again with a prompt asking to assess the bias. Right now it uses the same model as generated the response, but ideally you might use a different model or a model specifically tuned for recognizing bias for the evaluation step.

### TestDefaultResponseDavinci
Sends the raw prompt to the Davinci model.

##### `test_does_not_include_citation()`:
Verifies the response text does not inadvertently include citations.

##### `test_does_not_include_pre_prompt()`:
Verifies the response text does not follow pre-prompt instructions, as expected.

### TestDefaultResponseGPT35
Sends the raw prompt to the GPT-3.5 model.

##### `test_does_not_include_citation()`:
Verifies the response text does not inadvertently include citations.

##### `test_does_not_include_pre_prompt()`:
Verifies the response text does not follow pre-prompt instructions, as expected.

