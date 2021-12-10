"""
black posit_decode.py # code formatter (pip install black)
"""
import softposit as sp
import signal
import random
import pytest

from regime import Regime
from posit import Posit, cls, c2
from math import log2


def handler(signum, frame):
    exit(1)


signal.signal(signal.SIGINT, handler)


get_bin = lambda x, n: format(x, "b").zfill(n)


def decode(bits, size, es) -> Posit:
    """
    Posit decoder.

    Break down P<size, es> in its components (sign, regime, exponent, mantissa).

    Prameters:
    bits (unsigned): sequence of bits representing the posit
    size (unsigned): length of posit
    es (unsigned): exponent field size.

    Returns:
    Posit object
    """

    if es > size - 1:
        raise ValueError("`es` field can't be larger than the full posit itself.")

    mask = (2 ** size) - 1
    msb = 1 << (size - 1)
    sign = bits >> (size - 1)

    if (bits << 1) & mask == 0:  # 0 or inf
        return Posit(size, es, sign, Regime(size=size), 0, 0)

    if log2(bits) > size:
        raise Exception("cant fit {} in {} bits".format(bits, size))

    u_bits = bits if sign == 0 else c2(bits, size)
    reg_msb = 1 << (size - 2)
    reg_s = bool(u_bits & reg_msb)
    if reg_s == True:
        k = cls(u_bits << 1, size, 1) - 1
        reg_len = 2 + k  # min(k + 2, size - 1)
    else:
        k = -cls(u_bits << 1, size, 0)
        reg_len = 1 - k  # min(-k + 1, size - 1)

    r = Regime(size=size, k=k)

    assert r.reg_len == reg_len

    regime_bits = ((u_bits << 1) & mask) >> (size - reg_len)

    es_effective = min(es, size - 1 - reg_len)

    # align remaining of u_bits to the left after dropping sign (1 bit) and regime (`reg_len` bits)
    exp = ((u_bits << (1 + reg_len)) & mask) >> (size - es)  # max((size - es), (size - 1 - reg_len))

    mant = ((u_bits << (1 + reg_len + es)) & mask) >> (1 + reg_len + es)

    posit = Posit(
        size=size,
        es=es,
        sign=sign,
        regime=r,
        exp=exp,
        mant=mant,
    )

    assert bits == posit.bit_repr()

    return posit


if __name__ == "__main__":

    
    TESTS = 1

    if TESTS:

        NUM_RANDOM_TEST_CASES = 800

        # N = 8
        # list_of_bits = random.sample(
        #     range(0, 2 ** N - 1), min(NUM_RANDOM_TEST_CASES, 2 ** N - 1)
        # )
        # for bits in list_of_bits:
        #     posit = decode(bits, 8, 0)
        #     assert posit.to_real() == sp.posit8(bits=bits)
        #     # print(f"bits = {N}'b{get_bin(bits, N)};")
        #     # print(posit.tb())

        """
        N, ES = 5, 1
        list_of_bits = random.sample(
            range(0, 2 ** N - 1), min(NUM_RANDOM_TEST_CASES, 2 ** N - 1)
        )
        for bits in list_of_bits:
            if bits != (1 << N - 1) and bits != 0:
                posit = decode(bits, N, ES)
                # posit.to_real()
                print(f"bits = {N}'b{get_bin(bits, N)};")
                print(posit.tb())
        """

        # N = 16
        # list_of_bits = random.sample(range(0, 2 ** N - 1), min(NUM_RANDOM_TEST_CASES, 2 ** N - 1))
        # for bits in list_of_bits:
        #     assert decode(bits, 16, 1).to_real() == sp.posit16(bits=bits)

        """
        N = 32
        list_of_bits = random.sample(range(0, 2 ** N - 1), min(NUM_RANDOM_TEST_CASES, 2 ** N - 1))
        for bits in list_of_bits:
            print(get_bin(bits, N))
            if bits != (1 << N - 1) and bits != 0:
                assert decode(bits, 32, 2).to_real() == sp.posit32(bits=bits)

        print(decode(0b01110011, 8, 3))
        print(decode(0b11110011, 8, 0))
        print(decode(0b0110011101110011, 16, 1))
        """

    # N = 4
    # vals = []
    # for bits in range(2**N-1):
    #     vals.append(decode(bits, N, 2).to_real())
    # print(vals)

    REPL = 0
    if REPL:
        while True:
            bits = input(">>> 0b") or "0"
            es = int(input(">>> es: ") or 0)
            print(decode(int(bits, 2), len(bits), es))


tb = [
    (
        decode(0b01110011, 8, 3),
        Posit(
            size=8,
            es=3,
            sign=0,
            regime=Regime(size=8, k=2),
            exp=3,
            mant=0,
        ),
    ),
    (
        decode(0b01110111, 8, 2),
        Posit(
            size=8,
            es=2,
            sign=0,
            regime=Regime(size=8, k=2),
            exp=3,
            mant=1,
        ),
    ),
    (
        decode(0b11110111, 8, 2),
        Posit(
            size=8,
            es=2,
            sign=1,
            regime=Regime(size=8, k=-3),
            exp=0,
            mant=1,
        ),
    ),
    (
        decode(0b10110111, 8, 1),
        Posit(
            size=8,
            es=1,
            sign=1,
            regime=Regime(size=8, k=0),
            exp=0,
            mant=0b1001,
        ),
    ),
    (
        decode(0b01111111, 8, 0),
        Posit(
            size=8,
            es=0,
            sign=0,
            regime=Regime(size=8, k=6),
            exp=0,
            mant=0b0,
        ),
    ),
    (
        decode(0b0111111111111100, 16, 1),
        Posit(
            size=16,
            es=1,
            sign=0,
            regime=Regime(size=16, k=12),
            exp=0,
            mant=0b0,
        ),
    ),
    (
        decode(0b0111111111111110, 16, 1),
        Posit(
            size=16,
            es=1,
            sign=0,
            regime=Regime(size=16, k=13),
            exp=0,
            mant=0b0,
        ),
    ),
    (
        decode(0b0111111111111111, 16, 1),
        Posit(
            size=16,
            es=1,
            sign=0,
            regime=Regime(size=16, k=14),
            exp=0,
            mant=0b0,
        ),
    ),
    (
        decode(0b0111111111111100, 16, 1).to_real(),
        16777216.0,
    ),
    (decode(0b0111111111111111, 16, 1).to_real(), 268435456.0),
    (
        decode(0b0111111111111100, 16, 1).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m11111111111110\x1b[1;37;44m0\x1b[1;37;40m\x1b[0m",
    ),
    (decode(0b0000000000000001, 16, 1).to_real(), 3.725290298461914e-09),
    (
        decode(0b0000000000000001, 16, 1).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m000000000000001\x1b[1;37;40m\x1b[0m",
    ),
    (
        decode(0b0111111111111111, 16, 1).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m111111111111111\x1b[1;37;40m\x1b[0m",
    ),
    (decode(0b01110010000000000000000000011111, 32, 2).to_real(), 512.0004730224609),
    (
        decode(0b01110010000000000000000000011111, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m1110\x1b[1;37;44m01\x1b[1;37;40m0000000000000000000011111\x1b[0m",
    ),
    (decode(0b01111111111111111111111111110011, 32, 2).to_real(), 6.084722881095501e31),
    (
        decode(0b01111111111111111111111111110011, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m1111111111111111111111111110\x1b[1;37;44m01\x1b[1;37;40m1\x1b[0m",
    ),
    (decode(0b01111111111111111111111111111101, 32, 2).to_real(), 2.076918743413931e34),
    (
        decode(0b01111111111111111111111111111101, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m111111111111111111111111111110\x1b[1;37;44m1\x1b[1;37;40m\x1b[0m",
    ),
    (decode(0b01111111111111111111111111111011, 32, 2).to_real(), 2.596148429267414e33),
    (
        decode(0b01111111111111111111111111111011, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m11111111111111111111111111110\x1b[1;37;44m11\x1b[1;37;40m\x1b[0m",
    ),
    (decode(0b01111111111111111111111111111111, 32, 2).to_real(), 1.329227995784916e36),
    (
        decode(0b01111111111111111111111111111111, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m1111111111111111111111111111111\x1b[1;37;40m\x1b[0m",
    ),
    (decode(0b0111111111111111, 16, 1).to_real(), 268435456.0),
    (
        decode(0b0111111111111111, 16, 1).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m111111111111111\x1b[1;37;40m\x1b[0m",
    ),
    (decode(0b0111111111111110, 16, 1).to_real(), 67108864.0),
    (
        decode(0b0111111111111110, 16, 1).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m111111111111110\x1b[1;37;40m\x1b[0m",
    ),
    (
        decode(0b11111111111111111111111111111101, 32, 2).to_real(),
        -4.81482486096809e-35,
    ),
    (
        decode(0b11111111111111111111111111111101, 32, 2).bit_repr(),
        0b11111111111111111111111111111101,  # fails for some reasons
    ),
    (decode(0b10001111011111010010001111010111, 32, 2).to_real(), -321.4300003051758),
    (
        decode(0b10001111011111010010001111010111, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m1\x1b[1;30;43m1110\x1b[1;37;44m00\x1b[1;37;40m0100000101101110000101001\x1b[0m",
    ),
    (
        decode(0b10000000000000000000000000000011, 32, 2).to_real(),
        -2.076918743413931e34,
    ),
    (
        decode(0b10000000000000000000000000000011, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m1\x1b[1;30;43m111111111111111111111111111110\x1b[1;37;44m1\x1b[1;37;40m\x1b[0m",
    ),
    (
        decode(0b10000000000000000000000000000001, 32, 2).to_real(),
        -1.329227995784916e36,
    ),
    (
        decode(0b10000000000000000000000000000001, 32, 2).bit_repr(),
        0b10000000000000000000000000000001,  # wrong
    ),
    (decode(0b01111111111111111111111111111111, 32, 2).to_real(), 1.329227995784916e36),
    (
        decode(0b01111111111111111111111111111111, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m1111111111111111111111111111111\x1b[1;37;40m\x1b[0m",
    ),
    (decode(0b01111111111111111111111111111110, 32, 2).to_real(), 8.307674973655724e34),
    (
        decode(0b01111111111111111111111111111110, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m1111111111111111111111111111110\x1b[1;37;40m\x1b[0m",
    ),
    (decode(0b01111111111111111111111111111100, 32, 2).to_real(), 5.192296858534828e33),
    (
        decode(0b01111111111111111111111111111100, 32, 2).color_code(trimmed=True),
        "\x1b[1;37;41m0\x1b[1;30;43m111111111111111111111111111110\x1b[1;37;44m0\x1b[1;37;40m\x1b[0m",
    ),
]


@pytest.mark.parametrize("left,right", tb)
def test_regime(left, right):
    assert left == right


tb_against_softposit_8 = [
    0b01011111,
    0b01110010,
    0b01001011,
    0b10100000,
    0b11111010,
    0b01110011,
    0b01000001,
    0b01010100,
    0b00010011,
    0b10001011,
    0b00111101,
    0b10111101,
    0b01111001,
    0b00001010,
    0b00100110,
    0b00111011,
    0b10010010,
    0b10001000,
    0b01100100,
    0b10110111,
    0b01011000,
    0b00011111,
    0b10011101,
    0b11001110,
    0b10011010,
    0b01010000,
    0b11111000,
    0b00000010,
    0b00011100,
    0b11000101,
    0b00011001,
    0b00010101,
    0b10100001,
    0b01100111,
    0b00000100,
    0b00101010,
    0b00101111,
    0b00001000,
    0b10001101,
    0b01000010,
    0b01011110,
    0b11100101,
    0b01001101,
    0b11101000,
    0b10010111,
    0b01000100,
    0b10010000,
    0b00110000,
    0b00010010,
    0b00001110,
    0b01001111,
    0b11011001,
    0b10000101,
    0b11110001,
    0b00111000,
    0b01101010,
    0b11000011,
    0b00011011,
    0b01011101,
    0b10001110,
    0b10111100,
    0b01000011,
    0b00100101,
    0b00111111,
    0b11010100,
    0b00100001,
    0b01100010,
    0b00111010,
    0b10001010,
    0b01101100,
    0b00101000,
    0b00110111,
    0b11000110,
    0b01100000,
    0b11011111,
    0b10111111,
    0b01111110,
    0b11010001,
    0b00000101,
    0b01101011,
    0b01100001,
    0b01010010,
    0b11101011,
    0b00110001,
    0b10100011,
    0b01010001,
    0b11001000,
    0b01110100,
    0b00010001,
    0b10101101,
    0b10101011,
    0b10000100,
    0b00110010,
    0b00111100,
    0b11100001,
    0b01011011,
    0b00101100,
    0b11111011,
    0b10010100,
    0b10010101,
    0b00010111,
    0b10000111,
    0b01101111,
    0b11100011,
    0b11001111,
    0b10000001,
    0b10011000,
    0b01111100,
    0b00110101,
    0b10011001,
    0b10011111,
    0b10100100,
    0b10101010,
    0b01011010,
    0b10111010,
    0b00011101,
    0b11110011,
    0b10001001,
    0b11000100,
    0b01001100,
    0b10110010,
    0b01001000,
    0b11100111,
    0b11101101,
    0b01111101,
    0b11010011,
    0b11101110,
    0b10101100,
    0b00011000,
    0b11101001,
    0b01110111,
    0b00101001,
    0b00001001,
    0b11111100,
    0b11110101,
    0b11011010,
    0b11010111,
    0b11110111,
    0b10001100,
    0b00010110,
    0b11100010,
    0b00010100,
    0b10101111,
    0b00000000,
    0b00100011,
    0b11010010,
    0b10111110,
    0b01111011,
    0b11001011,
    0b01011100,
    0b11000111,
    0b10001111,
    0b11101010,
    0b10011110,
    0b01110101,
    0b11011101,
    0b10110110,
    0b00011010,
    0b01101000,
    0b11101111,
    0b11001010,
    0b01000101,
    0b10011100,
    0b10101001,
    0b11001100,
    0b10101000,
    0b10000011,
    0b01110001,
    0b00001011,
    0b10110011,
    0b01100011,
    0b01010011,
    0b00010000,
    0b00011110,
    0b10110100,
    0b10011011,
    0b11111001,
    0b01000110,
    0b11010110,
    0b00000001,
    0b11000001,
    0b00101110,
    0b11111110,
    0b10000000,
    0b10110000,
    0b01101001,
    0b11011000,
    0b10111000,
    0b11100000,
    0b11011100,
    0b00100111,
    0b11011110,
    0b10010001,
    0b00000111,
    0b00000011,
    0b11010000,
    0b10100110,
    0b00110100,
    0b11011011,
    0b00110011,
]


@pytest.mark.parametrize("bits", tb_against_softposit_8)
def test_real_value_against_softposit_8(bits):
    posit = decode(bits, 8, 0)
    assert posit.to_real() == sp.posit8(bits=bits)


tb_against_softposit_16 = [
    0b0110110101110100,
    0b1001111010110110,
    0b1000111111101101,
    0b1001100001101111,
    0b1010010011001011,
    0b1001011000000101,
    0b0000001110100110,
    0b1011011010000110,
    0b0101110101110111,
    0b1100100001010110,
    0b1110100111011000,
    0b1110010011100110,
    0b1101101010101111,
    0b0000111101110111,
    0b1101010011100011,
    0b1100111101001011,
    0b1110010001111110,
    0b0100110010001000,
    0b0110110110010001,
    0b1001011001101111,
    0b0100011110000100,
    0b1000010100110101,
    0b0011101001011100,
    0b0010010101111111,
    0b0101011101101011,
    0b1110000000101011,
    0b0101101111100001,
    0b0010011011001110,
    0b1000101010111100,
    0b0001101010000000,
    0b0111000001010101,
    0b1100011100000111,
    0b1101000111101100,
    0b1010101101001010,
    0b0001001101011000,
    0b0001000011000101,
    0b0011001111000111,
    0b0011010111001000,
    0b1011001101101101,
    0b0011011010011110,
    0b1000000111011000,
    0b0111010101111010,
    0b0110110101011011,
    0b0000111100100001,
    0b0000011011101010,
    0b0111011110001000,
    0b0001110011000011,
    0b0000010100001011,
    0b0010100101001011,
    0b1001001010010111,
    0b0010001100100001,
    0b0110110001011101,
    0b0001110100110010,
    0b0001101000110000,
    0b0101011110001111,
    0b1101110101011100,
    0b0001010011111001,
    0b0010100000110010,
    0b1001011111111110,
    0b1011100100100111,
    0b1111001100010110,
    0b0110101011010001,
    0b1110011110100100,
    0b0000101101111000,
    0b1101011000110001,
    0b1010100101000100,
    0b0010100001000101,
    0b0000111010111000,
    0b0011111101110111,
    0b0010011011111111,
    0b1001110101110001,
    0b0000011001011000,
    0b1001111011010101,
    0b1110111001101001,
    0b1111011000011000,
    0b1100111010001100,
    0b0111100111111001,
    0b0101001010110100,
    0b0101100110011011,
    0b0010010001000110,
    0b0110111110111001,
    0b0100010110001100,
    0b1110110000011111,
    0b0100010111101100,
    0b1110100111001001,
    0b0101011101100100,
    0b1011100000011010,
    0b1111010010110000,
    0b1011110110010110,
    0b1010011111110011,
    0b1001111100001111,
    0b1001101011010000,
    0b0001011111101111,
    0b0010011000101111,
    0b1110001110101001,
    0b1011111010000100,
    0b0011100100001010,
    0b1101100010001110,
    0b0100101010010001,
    0b1111100010101100,
    0b1000001011000011,
    0b0111110100001000,
    0b0010011101100100,
    0b1000111111101110,
    0b1101111100101011,
    0b1011101110000000,
    0b0100111010001011,
    0b0100101000010101,
    0b1001011001100110,
    0b0100100111000101,
    0b0001111111001110,
    0b0110010010000101,
    0b0101111101011000,
    0b0111010100011100,
    0b0110001101111001,
    0b1100110001101100,
    0b0010111001010001,
    0b1100000011100010,
    0b0110100001001010,
    0b1001100000100001,
    0b1100001101101110,
    0b0011000000101001,
    0b1101001000111100,
    0b1010000001000111,
    0b0100001000100011,
    0b1100111111000100,
    0b1111010001100000,
    0b1100011011010110,
    0b0100101011100100,
    0b0011100101101010,
    0b1101100111011010,
    0b0000100101010111,
    0b1001111010001110,
    0b1100000101101000,
    0b0000100110100011,
    0b0000010001000010,
    0b1110111111111000,
    0b1100011010011001,
    0b1110101011110010,
    0b1101101010111101,
    0b1101100001100101,
    0b0111110010000010,
    0b1010110010010001,
    0b0001010110110010,
    0b0100110001110011,
    0b0010100101111001,
    0b1010111100101101,
    0b1101001001010110,
    0b1101101011011000,
    0b0110010000110011,
    0b0001011110100001,
    0b0101010010001101,
    0b0011110101011001,
    0b0111011110000010,
    0b0011000000100011,
    0b0100000011011111,
    0b1010101111100011,
    0b0100100000110100,
    0b0101101111101101,
    0b0100010100011001,
    0b1110000101101001,
    0b0000010100110010,
    0b1100000010111101,
    0b0101000100111110,
    0b0001111001110100,
    0b0001111110100000,
    0b1111011111010010,
    0b1111001100000100,
    0b1011101100011010,
    0b0001000101110101,
    0b0110001010010101,
    0b0010101100010101,
    0b0000100111101010,
    0b0011011101011100,
    0b0100000000110000,
    0b0010111011000100,
    0b0000010111010101,
    0b0000110000111101,
    0b1010011101001010,
    0b0100001000110110,
    0b0001000010001000,
    0b1111000100101001,
    0b1000001111111010,
    0b0101100011000001,
    0b0100111011010110,
    0b0000010010011100,
    0b1110100100000001,
    0b0010111101110010,
    0b1111111000110011,
    0b1111011000001000,
    0b0010100011110110,
    0b0011001110101000,
    0b1101101110101010,
    0b0010111000110011,
    0b0101110001010100,
    0b0101110010001110,
    0b1101101110110011,
    0b1110010100000000,
    0b0111011111001001,
    0b0001111110110101,
    0b0000101010111100,
    0b1101001100101111,
    0b0100101010100111,
    0b0100110010000010,
    0b0100110111110111,
    0b1001101110000001,
    0b0101000100101011,
    0b1001110000111101,
    0b1010100010001110,
    0b1010100110101100,
    0b1110011001101111,
    0b0111000000110100,
    0b0000100110010000,
    0b0110000100000011,
    0b0010001101010011,
    0b1111110100001001,
    0b0101101111000001,
    0b1100001000000111,
    0b0101111000001110,
    0b0111110001001100,
    0b0101011001011101,
    0b1000111011101110,
    0b1010011101010111,
    0b0001110100100010,
    0b1000000011001111,
    0b0011011000101110,
    0b0001001001110110,
    0b1101010010110011,
    0b1010011010000011,
    0b0011001101110001,
    0b1001011111000001,
    0b1100010101000010,
    0b0000101100100010,
    0b0011101000010111,
    0b0000001110111100,
    0b1010110000100011,
    0b1100100110101100,
    0b0110101111110101,
    0b0101001001101001,
    0b0011100001010011,
    0b1100101000101011,
    0b1100110011000010,
    0b1011010110010000,
    0b0000001101100011,
    0b1000101111101111,
    0b1010110010011000,
    0b1000111101001011,
    0b1000101011100010,
    0b1101011111011111,
    0b1100101011110101,
    0b0100101001110010,
    0b1100001010001111,
    0b1101000101111011,
    0b1101010011111101,
    0b1010111111111001,
    0b1110111111000001,
    0b1100010011110110,
    0b0101110101111001,
    0b0111101101001100,
    0b0001010110111101,
    0b0000011001101110,
    0b0111000010111110,
    0b1010011001011010,
    0b1011010111100110,
    0b0010010000001000,
    0b0111000101101100,
    0b0011001111101100,
    0b0010001001010110,
    0b0011000000110000,
    0b0100011100000001,
    0b1100100110001001,
    0b1011100110110100,
    0b1010110110000111,
    0b0111010100110011,
    0b1010000011011010,
    0b1101011100101010,
    0b0101100100001110,
    0b0010101011111110,
    0b1111010100010000,
    0b0100001101100111,
    0b0101101110100111,
    0b1001001111111010,
    0b1111101100010111,
    0b1010100111110010,
    0b0000100000000111,
    0b0101000010001100,
    0b0001101010010111,
    0b0011110010000001,
    0b1011111110001110,
    0b1000000100011111,
    0b1100101110001111,
    0b1110111111110001,
    0b1101100001110100,
    0b1101100011110000,
    0b0111111011011101,
    0b0000101100111010,
    0b1010111110110110,
    0b1011100000101000,
    0b1101110100101000,
    0b0101001011110111,
    0b1000110010100110,
    0b1100110101101110,
    0b0010011000000101,
    0b1110110011001001,
    0b1110111110110111,
    0b1010000000110110,
    0b1011110010111010,
    0b1011001011010110,
    0b1010110111010111,
    0b1111010000101110,
    0b1101100001110000,
    0b1001010000100011,
    0b0101010101100000,
    0b0011010001111111,
    0b1101010001011001,
    0b0110111110011001,
    0b1101100100111011,
    0b1111101010000111,
    0b0111011101000010,
    0b0111010100111101,
    0b0000001100010011,
    0b0011001111011110,
    0b1001011000111010,
    0b0111011110111110,
    0b1000001001011000,
    0b1011110110011010,
    0b0101101011100111,
    0b1001001110001011,
    0b1110101100011100,
    0b1011010101110010,
    0b1110111111000101,
    0b1001000111001110,
    0b1111011101111001,
    0b0110110101010011,
    0b0000011000011011,
    0b0100000111110101,
    0b0011000011111011,
    0b0011000010111011,
    0b1010101101111101,
    0b1001001101011100,
    0b1110110110100010,
    0b0001001100010111,
    0b1010100000101000,
    0b0101100110000000,
    0b0011010101110000,
    0b0111000101100001,
    0b0100011011000111,
    0b1110100100111011,
    0b1011000101110101,
    0b1001111010111011,
    0b0000101000111111,
    0b1101010010001000,
    0b0111101011010001,
    0b0011000001010000,
    0b0011101001100011,
    0b0100010000001010,
    0b0011001000001100,
    0b0101101111100111,
    0b1001010111110010,
    0b1010010011110110,
    0b0111001010010101,
    0b1101101100000010,
    0b0011111001101111,
    0b0010101100100111,
    0b0111101111100111,
    0b1001010101000001,
    0b0011101010000011,
    0b0001100111001001,
    0b1000100010011110,
    0b0001111001111100,
    0b0001001100001111,
    0b0101100100101100,
    0b1100111110001000,
    0b1011100101011010,
    0b0101100101101010,
    0b0111000001100010,
    0b1001100000110001,
    0b1000101100001110,
    0b0100011011101110,
    0b0010000000110100,
    0b0011101011010010,
    0b0000011101111101,
    0b1101100100111110,
    0b0010000110101000,
    0b0001101000101111,
    0b0011010111001110,
    0b0100100111011100,
    0b0000110101011110,
    0b0111110100111100,
    0b1101001101001111,
    0b0101100100011010,
    0b1010100011001010,
    0b0000100010000101,
    0b0001011011101101,
    0b0111010011100100,
    0b0100101110110010,
    0b0011101101101001,
    0b1000101111001101,
    0b1011011101101000,
    0b0100001110001110,
    0b0011000010100101,
    0b1001101111110111,
    0b0010110111011011,
    0b0101110101000010,
    0b0111011100001010,
    0b0011010000000000,
    0b0010101111110111,
    0b1100100001010100,
    0b0011001001100111,
    0b0001010001000111,
    0b1001001011101001,
    0b0101111001011100,
    0b1000110111010100,
    0b0011001010111010,
    0b1100111111011011,
    0b0100000101101110,
    0b1001110100000001,
    0b0010011110011111,
    0b0101100001010011,
    0b0111100111111100,
    0b0011000011101010,
    0b0111110000111000,
    0b0010011101100111,
    0b0101000000011111,
    0b1001000000011101,
    0b1100001111111001,
    0b0110110001011100,
    0b1110110111011001,
    0b1100100010001001,
    0b0111010111000010,
    0b1010000011000111,
    0b1010010110010011,
    0b1000010010011110,
    0b1011000010100110,
    0b1000110001101000,
    0b1100001001111001,
    0b0011111101001000,
    0b0001000001000111,
    0b0101111010101111,
    0b1001000011111110,
    0b1001100110001010,
    0b1111001111111001,
    0b0001111100001110,
    0b0010100011011110,
    0b1011011110111001,
    0b1001010001001100,
    0b1100101111000011,
    0b1010001010001111,
    0b0110000011110100,
    0b0011010001010111,
    0b1100111100111011,
    0b0111011101101000,
    0b0010001011110100,
    0b1100111000110101,
    0b0000100001111111,
    0b0010101000010101,
    0b0001110011101011,
    0b0011111100001000,
    0b0111010001010000,
    0b1011011110011001,
    0b0111001011100100,
    0b1100000000011011,
    0b0010111110100111,
    0b1100111001110100,
    0b0010101010000000,
    0b0000111111111110,
    0b0010010101001110,
    0b0010110001001101,
    0b0001001011111100,
    0b0001101001011111,
    0b1101111010010011,
    0b0010011001110001,
    0b1101111111100011,
    0b1010110011101001,
    0b1000101111010100,
    0b1111111000010110,
    0b0100110001001000,
    0b0010011100010011,
    0b1110110111111000,
    0b0100010010110110,
    0b1100001110101001,
    0b0110010101011110,
    0b0110000111011000,
    0b1111101111111000,
    0b0101100110101010,
    0b0111100111010111,
    0b1111111100101101,
    0b0010010001100110,
    0b1110001111101101,
    0b0101110011101010,
    0b1101101111110010,
    0b0010101011110111,
    0b1111000100000101,
    0b0110010001100010,
    0b0000100111001001,
    0b0100011100011010,
    0b1001000010110011,
    0b1000100101110000,
    0b1110111101000001,
    0b1000010101001100,
    0b1100000000101101,
    0b1001010100101110,
    0b0101111100111001,
    0b1111111111010010,
    0b0011110101000100,
    0b0101111111100010,
    0b0010101011001110,
    0b1000011011100010,
    0b1111101101011010,
    0b1100100000010001,
    0b0111011100000001,
    0b0110010011011011,
    0b0000000111010010,
    0b0011011110000110,
    0b0010110100100011,
    0b1011010111110001,
    0b0110010111100101,
    0b1101101110000010,
    0b1010010000101111,
    0b1011111110000000,
    0b0111011100100001,
    0b0110101101011100,
    0b0111010000010110,
    0b1010000110000010,
    0b0000101111011011,
    0b1001101011101011,
    0b0100011111111001,
    0b1110010110001001,
    0b1111000000001110,
    0b0111100011000000,
    0b0011011101110100,
    0b0100001110100001,
    0b0001001001001011,
    0b0101110010011100,
    0b1000101111011000,
    0b1011010100010010,
    0b1000110101000101,
    0b1000100000001110,
    0b0100101111000111,
    0b0001101100010110,
    0b1000011011010001,
    0b0111101001011110,
    0b1000000100011110,
    0b0000001001001010,
    0b1001010111011111,
    0b0001011010111111,
    0b0001101001110100,
    0b0110010101101110,
    0b0110111000000000,
    0b1111010000010011,
    0b0100001001100110,
    0b0011100111011101,
    0b1000101101111000,
    0b0111111010000110,
    0b1000010001101101,
    0b1010100000101011,
    0b0101111110111010,
    0b1110001111000111,
    0b1011101010011000,
    0b1010101001101110,
    0b0000011110011011,
    0b1101001100100001,
    0b1000100111011101,
    0b1110100100110010,
    0b0011011111111010,
    0b1011110100001011,
    0b1000001111001011,
    0b0111010110011111,
    0b1110001001011000,
    0b0111010110000100,
    0b0100001000001010,
    0b0111011101111110,
    0b0101101000011110,
    0b1101011010101000,
    0b0000011010110100,
    0b0100111001100110,
    0b0111111101011011,
    0b1011110010101001,
    0b0000100001101000,
    0b1101000110101001,
    0b1011000101100011,
    0b0000100000111000,
    0b1001101100010101,
    0b1000010110010100,
    0b1111000011101000,
    0b1100110100011111,
    0b0010101001011001,
    0b1011000011110111,
    0b0111011100000110,
    0b1011100001011100,
    0b0111000001110100,
    0b0010010110011000,
    0b0001111100100011,
    0b1100100110010001,
    0b1000100010001001,
    0b1101011100011111,
    0b0000111101011100,
    0b1001100000111110,
    0b0000111110000110,
    0b1000001000111011,
    0b0110011110111111,
    0b1111011110010100,
    0b1001101111001000,
    0b1000010001000000,
    0b0110111001001110,
    0b0011111011011110,
    0b0101001011100010,
    0b0101100011100100,
    0b0001010011100010,
    0b0110010011111000,
    0b1110011000100111,
    0b0111010010110100,
    0b0111101001100100,
    0b0111001110001111,
    0b1011100000111100,
    0b0001111011100001,
    0b1101111110110111,
    0b0110101001011011,
    0b0101001110110100,
    0b0111010100000001,
    0b0111001000001011,
    0b1010000110100001,
    0b1110110110111111,
    0b1010111010001110,
    0b1010111110010010,
    0b0000110010110000,
    0b0100011101100011,
    0b0111000111001000,
    0b0011111101010000,
    0b1001111001100111,
    0b0110111000100110,
    0b1010111001011001,
    0b0000101001101011,
    0b0111101100010001,
    0b1111111011011010,
    0b0000011001110011,
    0b1011011011011100,
    0b0011011111000000,
    0b1000000110010101,
    0b1110100101110010,
    0b1001011110010010,
    0b0001101010010110,
    0b1001011000110110,
    0b0100111110101100,
    0b0110001011111001,
    0b1010000111101001,
    0b1100111110001111,
    0b1011010010111010,
    0b1000000011001011,
    0b0111001110000110,
    0b0010000100101000,
    0b1001010000010110,
    0b1000010100110010,
    0b1011000110000010,
    0b1101101010101000,
    0b1000110011100010,
    0b0000010011101000,
    0b1011100110001111,
    0b0110001011001110,
    0b0001101000001000,
    0b0101000101110100,
    0b0000100010011111,
    0b0110101101000100,
    0b1100011011001101,
    0b0001101111111101,
    0b1000110011000000,
    0b0101001101011011,
    0b0101010100101000,
    0b1001111011101111,
    0b1111011000110111,
    0b1100011010010011,
    0b0100101001100111,
    0b1101010000001100,
    0b1000111000110101,
    0b0100010001101001,
    0b0000011011001011,
    0b1001101100101101,
    0b0111010101011001,
    0b1101010111100110,
    0b0111011011000100,
    0b0110011111011101,
    0b0001100100011111,
    0b1000001100000110,
    0b0001010011000000,
    0b0000111101001101,
    0b0010111000100100,
    0b0011000001100111,
    0b0001101001101011,
    0b0110010101000010,
    0b1100010001101001,
    0b1101010100100000,
    0b0111000010100011,
    0b1000110100011001,
    0b0100011011111010,
    0b0100010111000010,
    0b0011101010000101,
    0b1000001100000111,
    0b1011111100101010,
    0b1101000001110001,
    0b1011101101110000,
    0b1001010011101000,
    0b1110011001111000,
    0b0011100100111101,
    0b1110111011001001,
    0b1011000001101000,
    0b0101110110110001,
    0b1101000011011010,
    0b1101100011100111,
    0b1100101001111010,
    0b1011010111010110,
    0b1011101111111011,
    0b0100001101101100,
    0b1010010010011001,
    0b1101101100111101,
    0b1101011100101100,
    0b1001101101101011,
    0b0001011001100000,
    0b1011001111010000,
    0b0101101110111011,
    0b0100101010001011,
    0b0000100110100000,
    0b0101100010111010,
    0b0000101011001001,
    0b1100010110011000,
    0b0100111001011001,
    0b0011010011010111,
    0b1000010111111111,
    0b0010111110111101,
    0b1101110011111001,
    0b0111101000000100,
    0b1100000111001001,
    0b0100100111100111,
    0b0100100001110010,
    0b0001101001110010,
    0b0100110000101100,
    0b1011100011100001,
    0b0011100011010110,
    0b0011100100111001,
    0b0010110101001111,
    0b0001100011100000,
    0b0000101000000111,
    0b1011111010000101,
    0b1100110110000100,
    0b1000111000110110,
    0b1111010001111100,
    0b1000110011010001,
    0b0100111111011001,
    0b0010011100110101,
    0b0000000000000011,
    0b0111110001100010,
    0b1110101110011101,
    0b0001100010100111,
    0b1011111000100010,
    0b0100000001111111,
    0b1011100001000010,
    0b0111100100100011,
    0b0101111110010011,
    0b0110010110111100,
    0b1100010000101100,
    0b0001111111001000,
    0b1000000011101100,
    0b0000110000010001,
    0b0001111101011111,
    0b1000011110111011,
    0b0100010110111100,
    0b0000000011001100,
    0b1000011001111100,
    0b1010000001100010,
    0b1011111000010010,
    0b0110001010111101,
    0b0101000111111010,
    0b0011111100000001,
    0b0111111001100001,
    0b0111000010111010,
    0b1000111101110010,
    0b1001111111011100,
    0b0000000001110010,
    0b0110101001000111,
    0b1110110111011100,
    0b1010001110101110,
    0b0011111011111011,
    0b1111100001010000,
    0b1000011011000010,
    0b0001011100110001,
    0b0001011010010000,
    0b1100010111011010,
    0b0101001111001111,
    0b0000010010101000,
    0b0100011000011001,
    0b1110011001001110,
    0b1000001000111100,
    0b1100110010111100,
    0b1101011010100000,
    0b0011100011011110,
    0b1000111001110101,
    0b0111000101011011,
    0b0110101000010001,
    0b1001100010010100,
    0b0010000011100111,
    0b0,
    0b1000000000000000,
]


@pytest.mark.parametrize("bits", tb_against_softposit_16)
def test_real_value_against_softposit_16(bits):
    posit = decode(bits, 16, 1)
    assert posit.to_real() == sp.posit16(bits=bits)
