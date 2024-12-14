
def twos_comp(val, bits):
    """Convert a value into its 2-complement.

    :param int val: Value.
    :param int bits: Number of available bits.
    :return int: The number's 2-complement.
    """
    if val & (1 << (bits - 1)) != 0:
        val = val - (1 << bits)
    return val
