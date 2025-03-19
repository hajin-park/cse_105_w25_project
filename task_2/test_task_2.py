import pytest
from main import reduce_ATM_to_EQTM

# Positive instance: a Turing machine M_pos that always accepts.
positive_instance = """\
TM:
Description: This Turing machine M_pos always accepts.
States: q0,q_accept
Alphabet: 0,1
Tape_Alphabet: 0,1,_
Start: q0
Accept: q_accept
Reject: q_reject
Transitions:
q0,0 -> q_accept,0,R
q0,1 -> q_accept,1,R
q0,_ -> q_accept,_,R
q_accept,0 -> q_accept,0,R
q_accept,1 -> q_accept,1,R
q_accept,_ -> q_accept,_,R

Input:
any
"""

# Negative instance: a Turing machine M_neg that always rejects.
negative_instance = """\
TM:
Description: This Turing machine M_neg always rejects.
States: p0,p_reject
Alphabet: 0,1
Tape_Alphabet: 0,1,_
Start: p0
Accept: p_accept
Reject: p_reject
Transitions:
p0,0 -> p_reject,0,R
p0,1 -> p_reject,1,R
p0,_ -> p_reject,_,R

Input:
any
"""


def test_reduce_ATM_to_EQTM_positive():
    output = reduce_ATM_to_EQTM(positive_instance)
    assert "M1:" in output, "Output should include 'M1:' marker."
    assert "---" in output, "Output should include a separator '---'."
    assert "M2:" in output, "Output should include 'M2:' marker."
    assert (
        "always accepts" in output
    ), "Positive instance should mention 'always accepts'."


def test_reduce_ATM_to_EQTM_negative():
    output = reduce_ATM_to_EQTM(negative_instance)
    assert "M1:" in output, "Output should include 'M1:' marker."
    assert "---" in output, "Output should include a separator '---'."
    assert "M2:" in output, "Output should include 'M2:' marker."
    assert (
        "always rejects" in output
    ), "Negative instance should mention 'always rejects'."
