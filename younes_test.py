from cmath import sqrt, exp
from math import pi, log10

from classical_state import ClassicalState
from mixed_state import MixedState
from pure_state import PureState


def not_op(bit_index):
    return lambda c: PureState({c.with_bit(bit_index, not c.bit(bit_index)): 1})


def hadamard_op(bit_index):
    s = sqrt(0.5)
    return lambda c: PureState({
        c.with_bit(bit_index, False): s,
        c.with_bit(bit_index, True): -s if c.bit(bit_index) else +s
    })


def partial_x_rotation_op(bit_index, denominator):
    t = exp(1j * pi / denominator)
    a, b = (1 + t) / 2, (1 - t) / 2
    return lambda c: PureState({
        c.with_bit(bit_index, False): b if c.bit(bit_index) else a,
        c.with_bit(bit_index, True): a if c.bit(bit_index) else b
    })


def controlled_by(op, bit_index_to_desired_map):
    return lambda c: op(c) \
        if all(c.bit(i) == v for i, v in bit_index_to_desired_map.items()) \
        else PureState({c: 1})


def bit_check_predicate(i, desired=True):
    return lambda c: c.bit(i) == desired


def simulate_younes_algo(anti_clauses):
    n = max(max(used_variables) for used_variables in anti_clauses) + 1
    m = len(anti_clauses)
    var_bits = range(n)
    clause_bits = range(n, n + m)
    ancilla_bit = n + m

    initial_state_classical = ClassicalState(0)
    initial_state_pure = PureState({initial_state_classical: 1})
    initial_state_mixed = MixedState({initial_state_pure: 1})
    state = initial_state_mixed

    # Put variable bits into uniform superposition.
    for i in var_bits:
        state = state.unitary_transform(hadamard_op(i))

    # Initialize clause bits.
    for j in range(m):
        state = state.unitary_transform(not_op(n + j))
        state = state.unitary_transform(
            controlled_by(not_op(n + j), anti_clauses[j]))

    def all_clause_bits_set(c):
        return all(c.bit(index) for index in clause_bits)

    # Perform iterative post-selection until p_correct is high enough.
    log_p_survived = 0
    step = 0
    while True:
        if step % 10 == 0:
            p_correct = state.post_select(all_clause_bits_set)[0]
            p_survived = 10**log_p_survived
            print("iter {:};\t".format(step),
                  "p_survived: {:0.04%};\t".format(p_survived),
                  "p_correct: {:0.04%};\t".format(p_correct),
                  "p_correct*p_survived: {:0.04%}".format(p_correct*p_survived))

            if p_correct >= 0.99:
                break

        step += 1
        for j in clause_bits:
            op = controlled_by(
                    partial_x_rotation_op(ancilla_bit, m),
                    {j: True})
            state = state.unitary_transform(op)
        p_pass, state = state.post_select(bit_check_predicate(ancilla_bit))
        state = state.unitary_transform(not_op(ancilla_bit))
        log_p_survived += log10(p_pass)

    # Final details.
    print("Samples:")
    for _ in range(5):
        s = state.collapsed()
        print(s, all_clause_bits_set(s))
    p_survived = 10**log_p_survived
    p_correct = state.post_select(all_clause_bits_set)[0]
    print("Chance of survival: {:0.8%}".format(p_survived))
    print("Chance of correct: {:0.8%}".format(p_correct))
    print("Chance of survived and correct: {:0.8%}".format(
        p_survived * p_correct))
    print("Expected number of attempts needed: {:0.9}".format
          (1 / (p_survived * p_correct)))
    print("2**n: {:}".format(2**n))


simulate_younes_algo(anti_clauses=[
    # Force 0 true
    {0: False, 1: False, 2: False},
    {0: False, 1: True, 2: False},
    {0: False, 1: False, 2: True},
    {0: False, 1: True, 2: True},

    # Force 1 true
    {0: True, 1: False, 2: False},
    {0: True, 1: False, 2: True},

    # Force all true
    {0: True, 1: True, 2: False},
    {0: True, 1: True, 3: False},
    {0: True, 1: True, 4: False},
    {0: True, 1: True, 5: False},
    {0: True, 1: True, 6: False},
    {0: True, 1: True, 7: False},
    {0: True, 1: True, 8: False},
    {0: True, 1: True, 9: False},
    {0: True, 1: True, 10: False},
])
