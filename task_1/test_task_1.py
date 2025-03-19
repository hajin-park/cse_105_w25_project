import pytest
from main import are_properties_consistent

# DFA for strings that start with '0'
w0 = """\
states: q0,q1,q2
alphabet: 0,1
start: q0
accept: q1
transitions:
q0,0,q1
q0,1,q2
q1,0,q1
q1,1,q1
q2,0,q2
q2,1,q2
"""

# DFA for strings that start with '1'
w1 = """\
states: r0,r1,r2
alphabet: 0,1
start: r0
accept: r1
transitions:
r0,1,r1
r0,0,r2
r1,0,r1
r1,1,r1
r2,0,r2
r2,1,r2
"""

# DFA for strings that contain at least one '0'
x0 = """\
states: s0,s1
alphabet: 0,1
start: s0
accept: s1
transitions:
s0,0,s1
s0,1,s0
s1,0,s1
s1,1,s1
"""

# DFA for strings that contain at least one '1'
x1 = """\
states: t0,t1
alphabet: 0,1
start: t0
accept: t1
transitions:
t0,1,t1
t0,0,t0
t1,0,t1
t1,1,t1
"""

# Missing start value
y0 = """\
states: s0,s1
alphabet: 0,1
start:
accept: s1
transitions:
s0,0,s1
s0,1,s0
s1,0,s1
s1,1,s1
"""

# Missing states
y1 = """\
states:
alphabet: 0,1
start: t0
accept: t1
transitions:
t0,1,t1
t0,0,t0
t1,0,t1
t1,1,t1
"""

# Incomplete transition
y2 = """\
states: a,b
alphabet: 0,1
start: a
accept: b
transitions:
a,0,b
a,1  # incomplete transition (missing next state)
"""


def test_are_properties_consistent_inconsistent():
    """
    Test that DFAs for strings starting with '0' and '1' are inconsistent.
    (They cannot have any common accepted string.)
    """
    result = are_properties_consistent(w0, w1)
    assert (
        result is False
    ), "Expected inconsistency for DFAs that start with '0' vs. '1'."


def test_are_properties_consistent_consistent():
    """
    Test that DFAs for strings that contain at least one '0' and at least one '1' are consistent.
    (The intersection accepts strings containing both '0' and '1'.)
    """
    result = are_properties_consistent(x0, x1)
    assert (
        result is True
    ), "Expected consistency for DFAs that require at least one '0' and one '1'."


@pytest.mark.parametrize(
    "dfa_str1, dfa_str2, expected_error",
    [
        (y0, w0, "start"),  # y0 is missing a valid start state.
        (w0, y1, "states"),  # y1 is missing states.
        (
            y0,
            y1,
            "start",
        ),  # Either error could be raised; matching one of the keywords is acceptable.
        (y2, w0, "incomplete transition"),  # y2 has a incomplete transition.
    ],
)
def test_invalid_dfa_encoding(dfa_str1, dfa_str2, expected_error):
    """
    Test that passing incorrectly encoded DFA strings raises a ValueError.
    The error message should mention the expected missing/incorrect component.
    """
    with pytest.raises(ValueError, match=expected_error):
        are_properties_consistent(dfa_str1, dfa_str2)
