"""
Project: CSE105W25 Task 1
Author: Hajin Park
Date: 3/15/2025
"""

from collections import deque


def parse_dfa(dfa_str):
    """
    Parses a DFA from a string representation.

    Expected format:
        states: state1,state2,...
        alphabet: symbol1,symbol2,...
        start: start_state
        accept: accept_state1,accept_state2,...
        transitions:
        current_state,symbol,next_state
        ...

    Returns:
        A dictionary with the following keys:
          - 'states': set of states
          - 'alphabet': set of symbols
          - 'start': start state
          - 'accept': set of accepting states
          - 'transitions': dictionary mapping (state, symbol) -> next_state
    """
    lines = [line.strip() for line in dfa_str.strip().splitlines() if line.strip()]
    dfa = {}
    transitions = {}

    # Process each header line until we reach transitions
    for i, line in enumerate(lines):
        if line.startswith("states:"):
            dfa["states"] = set(s.strip() for s in line[len("states:") :].split(","))
        elif line.startswith("alphabet:"):
            dfa["alphabet"] = set(
                s.strip() for s in line[len("alphabet:") :].split(",")
            )
        elif line.startswith("start:"):
            dfa["start"] = line[len("start:") :].strip()
        elif line.startswith("accept:"):
            dfa["accept"] = set(s.strip() for s in line[len("accept:") :].split(","))
        elif line.startswith("transitions:"):
            # The rest of the lines specify transitions.
            for trans_line in lines[i + 1 :]:
                parts = [p.strip() for p in trans_line.split(",")]
                if len(parts) != 3:
                    continue  # Skip malformed lines.
                curr, sym, nxt = parts
                transitions[(curr, sym)] = nxt
            break  # Exit once transitions are processed.
    dfa["transitions"] = transitions
    return dfa


def construct_intersection_dfa(dfa1, dfa2):
    """
    Constructs the intersection DFA of two DFAs using the Cartesian product construction.

    Assumes both DFAs share a common alphabet (the intersection of their alphabets is used).

    Returns:
        A dictionary representing the intersection DFA with keys:
          'states', 'alphabet', 'start', 'accept', and 'transitions'.
    """
    common_alphabet = dfa1["alphabet"] & dfa2["alphabet"]
    if not common_alphabet:
        raise ValueError("The two DFAs do not share a common alphabet.")

    new_states = set()
    new_transitions = {}
    new_accept = set()

    start_state = (dfa1["start"], dfa2["start"])
    queue = deque([start_state])
    new_states.add(start_state)

    while queue:
        (s1, s2) = queue.popleft()
        # Mark a state as accepting if both components are accepting.
        if s1 in dfa1["accept"] and s2 in dfa2["accept"]:
            new_accept.add((s1, s2))
        for sym in common_alphabet:
            next1 = dfa1["transitions"].get((s1, sym))
            next2 = dfa2["transitions"].get((s2, sym))
            if next1 is None or next2 is None:
                continue  # Skip if any DFA has no transition for this symbol.
            next_state = (next1, next2)
            new_transitions[((s1, s2), sym)] = next_state
            if next_state not in new_states:
                new_states.add(next_state)
                queue.append(next_state)

    return {
        "states": new_states,
        "alphabet": common_alphabet,
        "start": start_state,
        "accept": new_accept,
        "transitions": new_transitions,
    }


def is_language_empty(dfa):
    """
    Determines whether the language recognized by a DFA is empty.

    Uses Breadth-First Search (BFS) from the DFA's start state to see if any accepting state is reachable.

    Returns:
        True if the language is empty (no accepting state is reachable); otherwise, False.
    """
    visited = set()
    queue = deque([dfa["start"]])

    while queue:
        state = queue.popleft()
        if state in dfa["accept"]:
            return False  # An accepting state is reachable.
        if state in visited:
            continue
        visited.add(state)
        for sym in dfa["alphabet"]:
            next_state = dfa["transitions"].get((state, sym))
            if next_state and next_state not in visited:
                queue.append(next_state)
    return True


def are_properties_consistent(dfa_str1, dfa_str2):
    """
    Given two DFA representations as strings, determines whether their languages are consistent
    (i.e., whether there exists at least one string accepted by both DFAs).

    Returns:
        True if the intersection is nonempty (properties are consistent), else False.
    """
    dfa1 = parse_dfa(dfa_str1)
    dfa2 = parse_dfa(dfa_str2)
    intersection_dfa = construct_intersection_dfa(dfa1, dfa2)
    return not is_language_empty(intersection_dfa)
