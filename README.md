### Prompt Engineering Testing Strategies

This is an example project showing prompt engineering testing strategies, using the OpenAI API.

This code demonstrates how I ensure the high quality of the prompts I create. The [test.py](https://github.com/duncantmiller/llm_prompt_engineering/blob/main/test.py) file shows a series of tests I wrote for the project using test-driven development. These tests helped me to repeatedly test a system where a user prompt is augmented by additional prompts, including a [pre_prompt](https://github.com/duncantmiller/llm_prompt_engineering/blob/15c2ffe4c476f0a1ae563ffb8498320069c14c1b/message.py#L64) and a [cite_sources_prompt](https://github.com/duncantmiller/llm_prompt_engineering/blob/15c2ffe4c476f0a1ae563ffb8498320069c14c1b/message.py#L53) which provide additional instruction to the LLM beyond the user prompt.

This automated test suite makes it easier for me to hone prompts or switch models (text-davinci-003 to gpt-3.5-turbo) and ensure that the prompts provide a consistent response. It also enables me to monitor for ethical and bias mitigation and model drift over time.

This is a simplified version of the logic used in [OpenShiro](https://openshiro.com) prompts for educational purposes. The full product involves many more parameters including additional model versions, additional APIs like Azure, Google, HuggingFace, Anthropic and Cohere, and a library of pre-formatted prompts from which the users can select.

#### Usage
Clone the repository with `git clone git@github.com:duncantmiller/llm_prompt_engineering.git` then change to the project directory with `cd llm_prompt_engineering`.

Use if you use [pipenv](https://pypi.org/project/pipenv/) you can install the dependencies with `pipenv install`, otherwise use `pip install -r requirements.txt`. Note that due to a PyTorch dependency via sentence-transformers (used for similarity testing), the latest Python version that can be used is `3.11.7`.

The tests use [vcrpy](https://github.com/kevin1024/vcrpy) to record and replay the interactions with the OpenAI API. To run the tests, execute the command `python test.py`.

It can also be helpful to run the tests against the live OpenAI API. Note that when your run tests against the live API you will need an OpenAI API key and it will incur a cost. Also the tests will take much longer to run (approximately 93.5s using the live API vs 0.2s using the vcr cassette responses on my machine). To run the tests against the live API follow these steps:

- Copy the .env_example file and rename it as .env with `cp .env_example .env` (Linux/macOS) or `copy .env_example .env` (Windows)
- Open the .env file and enter the value for your OpenAI API Key for the `OPENAI_API_KEY=` variable. For example if your API key is 'foo' then `OPENAI_API_KEY=foo`
- Run the tests with the command line flag `python test.py --live-test`

##### Re-recording Cassettes

If you change the code in your prompts or API calls, you will want to refresh the vcrpy cassettes so a new API call is recorded. To do this simply delete the appropriate .yaml cassette files in the fixtures/vcr_cassettes directory. You can also optionally set a `re_record_interval` in the `vcr` command. For example to re-record every 7 days:

````
with vcr.use_cassette('cassette_name.yaml', re_record_interval=7*24*60*60):
    # API call goes here
````
