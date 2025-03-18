import pytest
from main import reduce_ATM_to_EQTM

# Positive instance: a Turing machine M_pos that always accepts.
positive_instance = (
    "TM:\n"
    "Description: This Turing machine M_pos always accepts.\n"
    "States: q0,q_accept\n"
    "Alphabet: 0,1\n"
    "Tape_Alphabet: 0,1,_\n"
    "Start: q0\n"
    "Accept: q_accept\n"
    "Reject: q_reject\n"
    "Transitions:\n"
    "q0,0 -> q_accept,0,R\n"
    "q0,1 -> q_accept,1,R\n"
    "q0,_ -> q_accept,_,R\n"
    "q_accept,0 -> q_accept,0,R\n"
    "q_accept,1 -> q_accept,1,R\n"
    "q_accept,_ -> q_accept,_,R\n"
    "\n"
    "Input:\n"
    "any"
)

# Negative instance: a Turing machine M_neg that always rejects.
negative_instance = (
    "TM:\n"
    "Description: This Turing machine M_neg always rejects.\n"
    "States: p0,p_reject\n"
    "Alphabet: 0,1\n"
    "Tape_Alphabet: 0,1,_\n"
    "Start: p0\n"
    "Accept: p_accept\n"
    "Reject: p_reject\n"
    "Transitions:\n"
    "p0,0 -> p_reject,0,R\n"
    "p0,1 -> p_reject,1,R\n"
    "p0,_ -> p_reject,_,R\n"
    "\n"
    "Input:\n"
    "any"
)


def test_reduce_ATM_to_EQTM_positive():
    """
    Test the mapping reduction on a positive instance.
    The resulting encoding should include markers and the description for a machine that always accepts.
    """
    output = reduce_ATM_to_EQTM(positive_instance)
    # Verify that the output contains the required markers and expected content.
    assert "M1:" in output, "Output should include 'M1:' marker."
    assert "---" in output, "Output should include a separator '---'."
    assert "M2:" in output, "Output should include 'M2:' marker."
    assert (
        "always accepts" in output
    ), "Positive instance should mention 'always accepts'."


def test_reduce_ATM_to_EQTM_negative():
    """
    Test the mapping reduction on a negative instance.
    The resulting encoding should include markers and the description for a machine that always rejects.
    """
    output = reduce_ATM_to_EQTM(negative_instance)
    # Verify that the output contains the required markers and expected content.
    assert "M1:" in output, "Output should include 'M1:' marker."
    assert "---" in output, "Output should include a separator '---'."
    assert "M2:" in output, "Output should include 'M2:' marker."
    assert (
        "always rejects" in output
    ), "Negative instance should mention 'always rejects'."
