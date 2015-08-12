import random
from classical_state import ClassicalState
from pure_state import PureState


class MixedState:
    """
    A probability distribution of pure states.
    """

    def __init__(self, pure_to_probability_map):
        err = abs(1 - sum(pure_to_probability_map.values()))
        if err > 0.00001:
            raise ValueError("Probabilities must sum to 1.")
        self.distribution = {
            pure_state: p
            for pure_state, p in pure_to_probability_map.items()
            if p >= 0.000001  # Discard impossible states (w/ rounding-error)
        }

    def measure(self, predicate):
        """
        :param predicate: Takes classical states and returns hashable keys.
        Determines which states the measurement distinguishes between.
        States mapped to the same result by the predicate will not be split
        into separate parts of the resulting mixed state.
        :return: A mixed state of possible measurement results.
        """
        return MixedState({
            pure_2: p2 * p1
            for pure_1, p1 in self.distribution.items()
            for pure_2, p2 in pure_1.measure(predicate).distribution.items()
        })

    def post_select(self, predicate):
        """
        :param predicate: Determines which classical states to keep. All
        non-matching states are discarded out of the mixed state and its
        superpositions (the resulting mixed state is renormalized to compensate
        for the missing weight).
        :return: A (probability, MixedState) pair with the probability of the
        desired predicate being satisfied (the post-selection's "power") and the
        renormalized mixed state bof the matching values.

        >>> a, b, c = ClassicalState(0), ClassicalState(1), ClassicalState(2)
        >>> p, q = PureState({a : 1}), PureState({b : 1})
        >>> r = PureState({c : 0.8, b : 0.6})
        >>> MixedState({p: 0.25, q: 0.75}).post_select(lambda c: c.bit(0))
        (0.75, MixedState({PureState({ClassicalState(1): (1+0j)}): 1.0}))
        >>> MixedState({p: 0.25, q: 0.75}).post_select(lambda c: not c.bit(0))
        (0.25, MixedState({PureState({ClassicalState(0): (1+0j)}): 1.0}))
        >>> MixedState({r: 1}).post_select(lambda c: c.bit(0))
        (0.36, MixedState({PureState({ClassicalState(1): (1+0j)}): 1.0}))
        >>> MixedState({r: 1}).post_select(lambda c: not c.bit(0))
        (0.6400000000000001, MixedState({PureState({ClassicalState(2): (1+0j)}): 1.0}))

        # disabled due to non-deterministic ordering of dictionaries
        # >>> MixedState({p: 0.2, q: 0.3, r: 0.5}).post_select(lambda c: c.bit(0))
        # (0.48, MixedState({PureState({ClassicalState(1): (1+0j)}): 0.375, PureState({ClassicalState(1): (1+0j)}): 0.625}))
        """
        filtered = {
            filtered_state: p_hit * p_state
            for pure_state, p_state in self.distribution.items()
            for p_hit, filtered_state in [pure_state.post_select(predicate)]
            if p_hit * p_state != 0
        }
        remaining_weight = sum(filtered.values())
        if remaining_weight == 0:
            return 0, None
        normalized = MixedState({pure_state: p / remaining_weight
                                 for pure_state, p in filtered.items()})
        return remaining_weight, normalized

    def unitary_transform(self, op):
        """
        :param: op Maps inputs to a superposition of outputs.
        Must be a unitary operation (i.e. length preserving in all cases).
        :return: The resulting mixed state, after the operation has been applied
        to each pure state within the mixed state.
        """
        return MixedState({pure_state.unitary_transform(op): p
                           for pure_state, p in self.distribution.items()})

    def collapsed(self):
        """
        Picks a classical state at random, with frequency proportional to
        the containing mixed state probabilities and containing superpositions'
         amplitudes' squared magnitudes.
        :return: A classical state from the mixed state.
        """
        t = random.random()
        for pure_state, p in self.distribution.items():
            t -= p
            if t <= 0.000001:
                return pure_state.collapsed()
        raise AssertionError("Probabilities didn't sum to 1")

    def __str__(self):
        return "\n".join("{0:.1%}: {1}".format(p, pure_state)
                         for pure_state, p in self.distribution.items())

    def __repr__(self):
        return "MixedState(" + repr(self.distribution) + ")"
