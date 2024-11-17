# Tests that the python files in this folder can be imported (and therefore run without errors)
#

def test_inference():
    import inference

def test_prompts():
    import prompt_inline
    import prompt_promptyfile

def test_search():
    import search

def test_openai():
    import openai_client

def test_evaluation():
    import evaluate_violence

def test_tracing():
    import tracing_enable

# TODO add when public: 
# def test_agents():
#     import agents