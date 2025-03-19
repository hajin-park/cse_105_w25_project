"""
Project: CSE105W25 Task 1
Author: Hajin Park
Date: 3/15/2025
"""

from collections import deque


def parse_dfa(dfa_str):
    """
    Parses a DFA from a string representation and validates its format.

    Expected format:
        states: state1,state2,...
        alphabet: symbol1,symbol2,...
        start: start_state
        accept: accept_state1,accept_state2,...
        transitions:
        current_state,symbol,next_state
        ...

    Validations performed:
      - All required headers must be present.
      - None of the required fields (states, alphabet, start, accept) may be empty.
      - The start state must be in the set of states.
      - All accept states must be in the set of states.
      - Each transition line must consist of exactly three comma-separated values.
      - For each transition, the current state and next state must belong to the set of states,
        and the symbol must be in the alphabet.

    Returns:
        A dictionary with the following keys:
          - 'states': set of states
          - 'alphabet': set of symbols
          - 'start': start state
          - 'accept': set of accepting states
          - 'transitions': dictionary mapping (state, symbol) -> next_state

    Raises:
        ValueError: If the DFA string is not correctly encoded.
    """
    lines = [line.strip() for line in dfa_str.strip().splitlines() if line.strip()]
    dfa = {}
    transitions = {}

    # Track whether each header has been found.
    headers_found = {
        "states": False,
        "alphabet": False,
        "start": False,
        "accept": False,
        "transitions": False,
    }

    for i, line in enumerate(lines):
        if line.startswith("states:"):
            headers_found["states"] = True
            states_val = line[len("states:") :].strip()
            if not states_val:
                raise ValueError("The 'states' line is empty.")
            dfa["states"] = set(s.strip() for s in states_val.split(",") if s.strip())
        elif line.startswith("alphabet:"):
            headers_found["alphabet"] = True
            alphabet_val = line[len("alphabet:") :].strip()
            if not alphabet_val:
                raise ValueError("The 'alphabet' line is empty.")
            dfa["alphabet"] = set(
                s.strip() for s in alphabet_val.split(",") if s.strip()
            )
        elif line.startswith("start:"):
            headers_found["start"] = True
            start_val = line[len("start:") :].strip()
            if not start_val:
                raise ValueError("The 'start' state is empty.")
            dfa["start"] = start_val
        elif line.startswith("accept:"):
            headers_found["accept"] = True
            accept_val = line[len("accept:") :].strip()
            if not accept_val:
                raise ValueError("The 'accept' states line is empty.")
            dfa["accept"] = set(s.strip() for s in accept_val.split(",") if s.strip())
        elif line.startswith("transitions:"):
            headers_found["transitions"] = True
            # Process the rest of the lines as transitions.
            for trans_line in lines[i + 1 :]:
                parts = [p.strip() for p in trans_line.split(",")]
                if len(parts) != 3:
                    raise ValueError(f"Malformed transition line: '{trans_line}'")
                curr, sym, nxt = parts
                transitions[(curr, sym)] = nxt
            break  # Exit once transitions are processed.

    # Ensure all required headers were found.
    for key, found in headers_found.items():
        if not found:
            raise ValueError(f"Missing required DFA component: {key}")

    dfa["transitions"] = transitions

    # Validate that the start state is in the set of states.
    if dfa["start"] not in dfa["states"]:
        raise ValueError("The start state is not in the set of states.")
    # Validate that each accept state is in the set of states.
    if not dfa["accept"].issubset(dfa["states"]):
        raise ValueError("Some accept states are not in the set of states.")
    # Validate each transition.
    for (curr, sym), nxt in transitions.items():
        if curr not in dfa["states"]:
            raise ValueError(f"Transition error: current state '{curr}' not in states.")
        if nxt not in dfa["states"]:
            raise ValueError(f"Transition error: next state '{nxt}' not in states.")
        if sym not in dfa["alphabet"]:
            raise ValueError(f"Transition error: symbol '{sym}' not in alphabet.")

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
    return True  # An accepting state is not reachable.


def are_properties_consistent(dfa_str1, dfa_str2):
    """
    Given two DFA representations as strings, determines whether their languages are consistent

    Returns:
        True if the intersection is nonempty (properties are consistent), else False.
    """
    dfa1 = parse_dfa(dfa_str1)
    dfa2 = parse_dfa(dfa_str2)
    intersection_dfa = construct_intersection_dfa(dfa1, dfa2)
    return not is_language_empty(intersection_dfa)
