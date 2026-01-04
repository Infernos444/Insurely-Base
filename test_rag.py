from query_data import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Expected Decision: {expected_decision}
Actual Response: {actual_response}

---
Answer ONLY with 'true' or 'false'.
Does the actual response clearly match the expected decision?
"""


def test_cataract_waiting_period():
    assert query_and_validate(
        question="Is cataract surgery covered under this insurance policy?",
        expected_decision="Rejected"
    )


def test_joint_replacement_non_accidental():
    assert query_and_validate(
        question="Is knee joint replacement surgery covered if it is not due to an accident?",
        expected_decision="Rejected"
    )


def test_accident_fracture_coverage():
    assert query_and_validate(
        question="Is surgery required due to a road accident covered under this policy?",
        expected_decision="Approved"
    )


def query_and_validate(question: str, expected_decision: str):
    # Query the RAG system
    response_text = query_rag(question)

    # Ask LLaMA to validate decision correctness
    prompt = EVAL_PROMPT.format(
        expected_decision=expected_decision,
        actual_response=response_text
    )

    model = Ollama(model="llama3")
    evaluation = model.invoke(prompt).strip().lower()

    print("\nEvaluation Prompt:")
    print(prompt)

    if "true" in evaluation:
        print("\033[92mDecision Correct\033[0m")
        return True
    elif "false" in evaluation:
        print("\033[91mDecision Incorrect\033[0m")
        return False
    else:
        raise ValueError(
            "Invalid evaluation result. LLM did not return true/false."
        )
