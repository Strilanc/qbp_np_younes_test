from cmath import sqrt
import random


class PureState:
    """
    A superposition of classical states.
    """

    def __init__(self, classical_to_amplitude):
        err = abs(1 - sum(abs(a)**2 for a in classical_to_amplitude.values()))
        if err > 0.00001:
            raise ValueError("Squared magnitudes must sum to 1.")
        self.superposition = {c: a
                              for c, a in classical_to_amplitude.items()
                              if abs(a) >= 0.0000001}

    def _weigh(self, predicate):
        return sum(abs(a)**2
                   for s, a in self.superposition.items()
                   if predicate(s))

    def post_select(self, predicate):
        """
        :param predicate: Determines which classical states to keep. All
        non-matching states are discarded out of the superposition (the
        resulting superposition is renormalized to compensate for the missing
        weight).
        :return: A (probability, PureState) pair with the probability of the
        desired predicate being satisfied (the post-selection's "power") and the
        renormalized superposition of the matching values.
        """
        p = self._weigh(predicate)
        if p == 0:
            return 0, None
        d = sqrt(p)
        return p, PureState({val: amp/d
                             for val, amp in self.superposition.items()
                             if predicate(val)})

    def measure(self, selector):
        """
        :param selector: Returns measurement results for given classical states.
        Classical states with differing measurement results end up in separate
        branches of the resulting mixed state.
        :return: The mixed state created by the measurement.
        """
        from mixed_state import MixedState  # Avoid top-level circular dep.
        used_measurement_results = {selector(c) for c in self.superposition}
        return MixedState({
            s: p
            for k in used_measurement_results
            for p, s in [self.post_select(lambda c: selector(c) == k)]
        })

    def unitary_transform(self, op):
        """
        :param: op Maps inputs to a superposition of outputs.
        Must be a unitary operation (i.e. length preserving in all cases).
        :return: The resulting pure state, after the operation has been applied
        and colliding states have been interfered.
        """
        # Each input in our superposition turns into a superposition of outputs.
        outputs = [(c2, a2*a1)
                   for c1, a1 in self.superposition.items()
                   for c2, a2 in op(c1).superposition.items()]

        # Because itertools.groupby implements the wrong thing.
        def group_by(items, key_func=lambda e: e[0], val_func=lambda e: e[1]):
            result = {}
            for e in items:
                k, v = key_func(e), val_func(e)
                if k in result:
                    result[k].append(v)
                else:
                    result[k] = [v]
            return result

        # When the same output is reached multiple ways, sum up the amplitudes.
        interfered = {k: sum(g) for k, g in group_by(outputs).items()}

        return PureState(interfered)

    def collapsed(self):
        """
        Picks a classical state at random, with frequency proportional to
        the associated amplitude's squared magnitude.
        :return: A classical state from the superposition.
        """
        t = random.random()
        for c, a in self.superposition.items():
            t -= abs(a)**2
            if t <= 0.000001:
                return c
        raise AssertionError("Probabilities didn't sum to 1")

    def __str__(self):
        return " + ".join("{:.3}".format(a) + "*" + str(c)
                          for c, a in self.superposition.items())

    def __repr__(self):
        return "PureState(" + repr(self.superposition) + ")"
