### Prompt Engineering Testing Strategies

This is an example project showing prompt engineering testing strategies, using the OpenAI API.

This code demonstrates how I help ensure the high quality of the prompts I create. The [test.py](https://github.com/duncantmiller/llm_prompt_engineering/blob/main/test.py) file shows a series of tests I wrote for the project using test-driven development. These tests helped me to repeatedly test a system where a user prompt is augmented by additional prompts, including a [pre_prompt](https://github.com/duncantmiller/llm_prompt_engineering/blob/15c2ffe4c476f0a1ae563ffb8498320069c14c1b/message.py#L64) and a [cite_sources_prompt](https://github.com/duncantmiller/llm_prompt_engineering/blob/15c2ffe4c476f0a1ae563ffb8498320069c14c1b/message.py#L53) which provide additional instruction to the LLM beyond the user prompt. Running these tests multiple times allowed me to hone the prompts to produce consistent responses from the LLM. I also added the ability to change the model from text-davinci-003 to gpt-3.5-turbo and still ensure that the prompts provide a consistent experience. This is a simplified version of the logic used in [OpenShiro](https://openshiro.com) prompts, which involve many more parameters including additional model versions, additional APIs like Azure, Google, HuggingFace etc., and a library of pre-formatted prompts the users can select.


#### Usage
Clone the repository and with `git clone git@github.com:duncantmiller/llm_prompt_engineering.git` then change to the project directory with `cd lm_prompt_engineering`.

The tests use [vcrpy](https://github.com/kevin1024/vcrpy) to record and replay the interactions with the OpenAI API. To run the tests, run the command `python test.py`.

It can be helpful to also run the tests against the live OpenAI API, in order to monitor for model drift. Note that when your run tests against the live API you will need an OpenAI API key and it will incur a cost. Also the tests will take much longer to run (approximately 93.5s vs 0.2s running the stubbed responses on my machine). To run the tests against the live API follow these steps:

- Copy the .env-example file, rename it to .env and include enter the value for your `OPENAI_API_KEY`
- Run the tests with the command line flag `python test.py --live-test`

##### Re-recording Cassettes

If you change the code in your prompts or API calls, you will want to refresh the vcrpy cassettes so a new fresh API call is recorded. To do this simply delete the appropriate .yaml cassette files. You can also optionally set a `re_record_interval` in the vcr command. For example to re-record every 7 days:

````
with vcr.use_cassette('cassette_name.yaml', re_record_interval=7*24*60*60):

````
