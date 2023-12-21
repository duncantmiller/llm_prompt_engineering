This is an example project showing prompt engineering testing strategies, using the OpenAI API.

This code demonstrates how I help ensure the high quality of the prompts I create. The [test.py](https://github.com/duncantmiller/llm_prompt_engineering/blob/main/test.py) file shows a series of tests I wrote for the project using test-driven development. These tests helped me to repeatedly test a system where a user prompt is augmented by additional prompts, including a [pre_prompt](https://github.com/duncantmiller/llm_prompt_engineering/blob/15c2ffe4c476f0a1ae563ffb8498320069c14c1b/message.py#L64) and a [cite_sources_prompt](https://github.com/duncantmiller/llm_prompt_engineering/blob/15c2ffe4c476f0a1ae563ffb8498320069c14c1b/message.py#L53) which provide additional instruction to the LLM beyond the user prompt. Running these tests multiple times allowed me to hone the prompts to produce consistent responses from the LLM. I also added the ability to change the model from text-davinci-003 to gpt-3.5-turbo and still ensure that the prompts provide a consistent experience. This is a simplified version of the logic used in [OpenShiro](https://openshiro.com) prompts, which involve many more parameters including additional model versions, additional APIs like Azure, Google, HuggingFace etc., and a library of pre-formatted prompts the users can select.


#### ToDo
The following optimizations:
- Currently the tests use live API calls to the OpenAI API. This is helpful for monitoring for drift, but makes the test runs expensive, both in time and API costs. I would like to add mocks for the tests and allow for live API calls to be run optionally for certain tests using something like (vcrpi)[https://pypi.org/project/vcrpy/1.5.2/] for this.
-
