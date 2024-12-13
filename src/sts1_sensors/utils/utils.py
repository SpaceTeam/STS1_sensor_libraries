
def twos_comp(val, bits):
    if val & (1 << (bits - 1)) != 0:
        val = val - (1 << bits)
    return val
