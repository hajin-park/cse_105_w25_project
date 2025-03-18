"""
Project: CSE105W25 Task 2
Author: Hajin Park
Date: 3/16/2025
"""


def parse_instance(instance_str):
    """
    Parses the instance string to extract the Turing machine (TM) description and input string w.

    The expected input format is:
        TM:
        <description of Turing machine M>
        Input:
        <input string w>

    Parameters:
        instance_str (str): The complete input string.

    Returns:
        tuple: (M_description (str), w (str))
    """
    tm_lines = []
    input_lines = []
    reading_tm = False
    reading_input = False

    for line in instance_str.strip().splitlines():
        line = line.strip()
        if line.startswith("TM:"):
            reading_tm = True
            reading_input = False
            continue
        elif line.startswith("Input:"):
            reading_input = True
            reading_tm = False
            continue

        if reading_tm:
            tm_lines.append(line)
        elif reading_input:
            input_lines.append(line)

    M_description = "\n".join(tm_lines).strip()
    w = "\n".join(input_lines).strip()
    return M_description, w


def construct_M1(M_description, w):
    """
    Constructs the encoding for M1.

    M1 is defined to:
      - Accept any input x that is not "0" immediately.
      - For x equal to "0", simulate the provided Turing machine M on input w.

    Parameters:
        M_description (str): A high-level description of Turing machine M.
        w (str): The input string for simulation.

    Returns:
        str: The string encoding of M1.
    """
    M1 = (
        "TM:\n"
        "Description: This Turing machine M1 works as follows:\n"
        "  - If input x != '0', accept immediately.\n"
        "  - If input x == '0', simulate the following Turing machine M on input w.\n"
        "M_simulation:\n" + M_description + "\n"
        "Input for simulation: " + w + "\n"
        "Note: Thus, L(M1)=Σ* if M accepts w, otherwise L(M1)=Σ* - {'0'}.\n"
    )
    return M1


def construct_M2():
    """
    Constructs the encoding for M2.

    M2 is defined as a Turing machine that unconditionally accepts any input.

    Returns:
        str: The string encoding of M2.
    """
    M2 = (
        "TM:\n"
        "Description: This Turing machine M2 accepts every input unconditionally.\n"
        "States: A, B\n"
        "Alphabet: 0,1\n"
        "Tape_Alphabet: 0,1,_\n"
        "Start: A\n"
        "Accept: B\n"
        "Reject: B\n"
        "Transitions:\n"
        "A,0 -> B,0,R\n"
        "A,1 -> B,1,R\n"
        "A,_ -> B,_,R\n"
        "B,0 -> B,0,R\n"
        "B,1 -> B,1,R\n"
        "B,_ -> B,_,R\n"
    )
    return M2


def reduce_ATM_to_EQTM(instance_str):
    """
    Implements the mapping reduction from A_TM to EQ_TM.

    Parameters:
        instance_str (str): A string representing an instance of A_TM, formatted with a 'TM:' section
                            for the Turing machine description and an 'Input:' section for the input w.

    Returns:
        str: A string representing the pair ⟨M1, M2⟩ in the format:
              M1:
              <encoding of M1>
              ---
              M2:
              <encoding of M2>
    """
    M_description, w = parse_instance(instance_str)
    M1_description = construct_M1(M_description, w)
    M2_description = construct_M2()
    output = "M1:\n" + M1_description + "\n---\nM2:\n" + M2_description
    return output
