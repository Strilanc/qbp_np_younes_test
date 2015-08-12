class ClassicalState:
    """
    A simple basis state, made up of bits and usable in superpositions.
    """

    def __init__(self, bit_mask_int):
        self.mask = bit_mask_int

    def bit(self, bit_index):
        return (self.mask & (1 << bit_index)) != 0

    def with_bit(self, bit_index, new_value):
        """
        >>> ClassicalState(0).with_bit(0, True)
        ClassicalState(1)
        >>> ClassicalState(0).with_bit(0, False)
        ClassicalState(0)
        >>> ClassicalState(1).with_bit(0, True)
        ClassicalState(1)
        >>> ClassicalState(1).with_bit(0, False)
        ClassicalState(0)
        >>> ClassicalState(7).with_bit(1, False)
        ClassicalState(5)
        >>> ClassicalState(7).with_bit(1, True)
        ClassicalState(7)
        """
        if self.bit(bit_index) == new_value:
            return self
        return ClassicalState(self.mask ^ (1 << bit_index))

    def __hash__(self):
        return self.mask

    def __eq__(self, other):
        return type(other) == ClassicalState and self.mask == other.mask

    def __str__(self):
        return "|{0:08b}?".format(self.mask)

    def __repr__(self):
        return "ClassicalState(" + str(self.mask) + ")"
