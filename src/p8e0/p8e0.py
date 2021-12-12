# either:
#   pytest p8e0.py -v
# or
#   python p8e0.py -v

from typing import Tuple
import pytest
import unittest
import random
import softposit as sp
import enum

# random.seed(12)
N = 8  # num bits


class P8E0(enum.Enum):
    ZERO = 0x00
    NAR = 0x80
    REG_S = 0x40


class Ans:
    def __init__(
        self,
        z,
        ui_a=0,
        ui_b=0,
        k_a=0,
        k_b=0,
        k_c=0,
        frac_a=0,
        frac_b=0,
        frac16=0,
        rcarry=0,
    ) -> None:
        self.z = z
        self.ui_a = ui_a
        self.ui_b = ui_b
        self.k_a = k_a
        self.k_b = k_b
        self.k_c = k_c
        self.frac_a = frac_a
        self.frac_b = frac_b
        self.frac16 = frac16
        self.rcarry = rcarry


def sign_reg_ui(bits):
    return (bits & 0x40) != 0


def _separate_bits_tmp(bits):
    k = 0
    tmp = bits << 2
    if sign_reg_ui(bits):
        while (tmp & 0x80) != 0:
            k += 1
            tmp = tmp << 1
    else:
        k = -1
        while (tmp & 0x80) == 0:
            k -= 1
            tmp = tmp << 1
        tmp &= 0x7F  # zeroes the leftmost bit
    return (k, tmp & 0xFF)


def separate_bits(bits):
    # k, tmp = _separate_bits_tmp(bits)

    k, reg_len = calc_k(bits)

    tmp = bits << 0
    tmp = (tmp << reg_len) & 0xFF | 0x80

    return (k, tmp)


def calc_k(bits):
    #### TODO: find a better way
    k = (
        -6
        if (bits << 1 & 0xFF) >> 1 == 1
        else -5
        if (bits << 1 & 0xFF) >> 2 == 1
        else -4
        if (bits << 1 & 0xFF) >> 3 == 1
        else -3
        if (bits << 1 & 0xFF) >> 4 == 1
        else -2
        if (bits << 1 & 0xFF) >> 5 == 1
        else -1
        if (bits << 1 & 0xFF) >> 6 == 1
        else 0
        if (~bits << 1 & 0xFF) >> 6 == 1
        else 1
        if (~bits << 1 & 0xFF) >> 5 == 1
        else 2
        if (~bits << 1 & 0xFF) >> 4 == 1
        else 3
        if (~bits << 1 & 0xFF) >> 3 == 1
        else 4
        if (~bits << 1 & 0xFF) >> 2 == 1
        else 5
        if (~bits << 1 & 0xFF) >> 1 == 1
        else 6
    )

    reg_len = 1 + (k + 1 if sign_reg_ui(bits) == 1 else -k)
    if reg_len == 8:
        reg_len = 7

    return (k, reg_len)


def shr(bits, rhs):
    """shift right"""
    return bits >> rhs


def shl(bits, rhs):
    """shift left"""
    return (bits << rhs) & 0xFFFF if rhs > 0 else bits


def calculate_regime(k) -> Tuple[int, bool, int]:
    if k < 0:
        length = -k & 0xFFFF_FFFF
        return (shr(0x40, length), False, length)
    else:
        length = (k + 1) & 0xFFFF_FFFF
        return (0x7F - shr(0x7F, length), True, length)


def pack_to_ui(regime, frac16):
    return regime + ((frac16 & 0xFFFF) >> 8)


# def encode_posit(k, frac16):
#     regime, reg_s, reg_len = calculate_regime(k)
#     if reg_len > 6:
#         u_z = 0x7f if reg_s else 0x01
#     else:
#         # to be finished
#         uz = 0x00000


def calc_ui(k, frac16):
    regime, reg_s, reg_len = calculate_regime(k)
    if reg_len > 6:
        u_z = 0x7F if reg_s else 0x01
    else:
        frac16 = (frac16 & 0x3FFF) >> reg_len

        bit_n_plus_one = (frac16 & 0x80) != 0
        u_z = pack_to_ui(regime, frac16)
        if bit_n_plus_one:
            bits_more = (frac16 & 0x7F) != 0
            u_z += (u_z & 1) | (bits_more & 0xFF)
    return u_z


def from_bits(bits, sign):
    return c2(bits) if sign else bits


def c2(a: int) -> int:
    return (~a + 1) & 0xFF


def wrapping_neg(a):
    return c2(a) & 0x7F


def is_nar(a):
    return a == 0x80


def is_zero(a):
    return a == 0


####### end aux functions #######


def mul(a: int, b: int) -> Ans:
    if is_nar(a) or is_nar(b):
        return Ans(z=0x80)  # NaR
    elif is_zero(a) or is_zero(b):
        return Ans(z=0)  # 0

    sign_a = a & 0x80
    sign_b = b & 0x80
    sign_z: bool = (sign_a ^ sign_b) != 0

    ui_a = a if sign_a == 0 else wrapping_neg(a)
    ui_b = b if sign_b == 0 else wrapping_neg(b)

    #### sign_a, reg_a, es_a, frac_a = decode_posit(a)
    k_a, frac_a = separate_bits(ui_a)
    k_b, frac_b = separate_bits(ui_b)

    k_c = k_a + k_b

    frac_c = (frac_a * frac_b) & 0xFFFF  # on twice the width

    rcarry = (frac_c & 0x8000) != 0

    if rcarry:
        k_c_updated = k_c + 1
        frac16 = frac_c >> 1
    else:
        k_c_updated = k_c
        frac16 = frac_c

    u_z = calc_ui(k_c_updated, frac16)
    z = from_bits(u_z, sign_z)

    return Ans(
        ui_a=ui_a,
        ui_b=ui_b,
        k_a=k_a,
        k_b=k_b,
        k_c=k_c_updated,
        frac_a=frac_a,
        frac_b=frac_b,
        frac16=frac16,
        rcarry=rcarry,
        z=z,
    )


def add_mags(a, b):
    sign = (a & 0x80) != 0

    ui_a = a if sign == 0 else c2(a)
    ui_b = b if sign == 0 else c2(b)

    if ui_a < ui_b:
        ui_a, ui_b = ui_b, ui_a

    k_a, frac_a = separate_bits(ui_a)
    frac16_a = ((frac_a & 0xFF) << 7) & 0xFFFF

    k_b, frac_b = separate_bits(ui_b)
    shift_right = k_a - k_b

    frac16_a += shl(frac_b, (7 - shift_right) & 0xFFFF_FFFF)

    rcarry = (frac16_a & 0x8000) != 0
    if rcarry:
        k_a += 1
        frac16_a >>= 1

    u_z = calc_ui(k_a, frac16_a)
    return from_bits(u_z, sign)


def _update_k_and_frac16_a(k, frac):
    while (frac >> 14) == 0:
        k -= 1
        frac = (frac << 1) & 0xFFFF
    return (k, frac)


def update_k_and_frac16_a(k, frac):
    n = 0 if frac >> 14 == 1 else \
        1 if frac >> 13 == 1 else \
        2 if frac >> 12 == 1 else \
        3 if frac >> 11 == 1 else \
        4 if frac >> 11 == 1 else \
        5 if frac >> 10 == 1 else \
        6 if frac >> 9  == 1 else \
        7 if frac >> 8 == 1 else \
        8 if frac >> 7 == 1 else \
        9 if frac >> 6 == 1 else \
        10 if frac >> 5 == 1 else \
        11 if frac >> 4 == 1 else \
        12 if frac >> 3 == 1 else \
        13 if frac >> 2 == 1 else \
        14 if frac >> 1 == 1 else \
        15 if frac >> 0 == 1 else 16
    

    # for i in range(13):
    #     if frac >> (13 - i) == 1:
    #         n = i

    frac = shl(frac, n - 1) & 0xFFFF  ## both -1 and -0 fails
    k = k - (n - 1)  ## both -1 and -0 fails
    return (k, frac)


def sub_mags(a, b):
    sign = a & 0x80 != 0
    if sign:
        ui_a = c2(a)
        ui_b = b
    else:
        ui_a = a
        ui_b = c2(b)

    if ui_a == ui_b:
        return 0x00

    if ui_a < ui_b:
        ui_a, ui_b = ui_b, ui_a
        sign = not sign

    k_a, frac_a = separate_bits(ui_a)
    frac16_a = ((frac_a & 0xFF) << 7) & 0xFFFF

    k_b, frac_b = separate_bits(ui_b)

    shift_right = k_a - k_b

    frac16_b = ((frac_b & 0xFF) << 7) & 0xFFFF

    if shift_right >= 14:
        return from_bits(ui_a, sign)
    else:
        frac16_b >>= shift_right
    frac16_a -= frac16_b

    (k_a, frac16_a) = _update_k_and_frac16_a(k_a, frac16_a)

    ecarry = ((0x4000 & frac16_a) >> 14) != 0
    if not ecarry:
        k_a -= 1
        frac16_a <<= 1

    u_z = calc_ui(k_a, frac16_a)
    return from_bits(u_z, sign)


u8 = int


def add(a: u8, b: u8) -> Ans:
    if a == 0 or b == 0:
        z = a | b
    elif a == 0x80 or b == 0x80:
        z = 0x80
    else:
        if (a ^ b) & 0x80 == 0:  # same sign
            z = add_mags(a, b)
        else:  # opposite sign
            z = sub_mags(a, b)
    return Ans(z)


class TestSum(unittest.TestCase):
    def test_zeros(self):
        a = 0x00
        b = random.randint(0, 2 ** N - 1)
        a_p8, b_p8 = sp.posit8(bits=a), sp.posit8(bits=b)

        z_int = mul(a, b).z
        self.assertEqual(a_p8 * b_p8, sp.posit8(bits=z_int))

    def test_nar(self):
        a = 0x80
        b = random.randint(0, 2 ** N - 1)
        a_p8, b_p8 = sp.posit8(bits=a), sp.posit8(bits=b)

        z_int = mul(a, b).z
        self.assertEqual(a_p8 * b_p8, sp.posit8(bits=z_int))

    def test_zero_times_nar(self):
        a = 0
        b = 0x80
        a_p8, b_p8 = sp.posit8(bits=a), sp.posit8(bits=b)

        z_int = mul(a, b).z
        self.assertEqual(a_p8 * b_p8, sp.posit8(bits=z_int))

    def test3(self):
        a = b = 0x7F
        a_p8, b_p8 = sp.posit8(bits=a), sp.posit8(bits=b)

        z_int = mul(a, b).z
        self.assertEqual(a_p8 * b_p8, sp.posit8(bits=z_int))

    def test_mix_mul(self):
        for _ in range(100):
            # 1) generate random 8bits numbers
            a = random.randint(0, 2 ** N - 1)
            b = random.randint(0, 2 ** N - 1)

            # 3) compute posit multiplication with my procedure (returns int)
            z_int = mul(a, b).z

            a_p8, b_p8 = sp.posit8(bits=a), sp.posit8(bits=b)

            c_p8 = a_p8 * b_p8
            self.assertEqual(c_p8, sp.posit8(bits=z_int))

    def test_mix_add(self):
        for _ in range(100):
            # 1) generate random 8bits numbers
            a = random.randint(0, 2 ** N - 1)
            b = random.randint(0, 2 ** N - 1)

            # 3) compute posit multiplication with my procedure (returns int)
            z_int = add(a, b).z

            a_p8, b_p8 = sp.posit8(bits=a), sp.posit8(bits=b)

            c_p8 = a_p8 + b_p8
            self.assertEqual(c_p8, sp.posit8(bits=z_int))


if __name__ == "__main__":
    unittest.main()


test_k_params = [
    (0b00000001, (-6, 7)),
    (0b10001010, (-3, 4)),
    (0b10001011, (-3, 4)),
    (0b00001110, (-3, 4)),
    (0b10001000, (-3, 4)),
    (0b00001010, (-3, 4)),
    (0b01110001, (2, 4)),
    (0b11110010, (2, 4)),
    (0b11110111, (2, 4)),
    (0b01110100, (2, 4)),
    (0b01110010, (2, 4)),
    (0b01111111, (6, 7)),
    (0b11111111, (6, 7)),
    (0b01100011, (1, 3)),
    (0b11100110, (1, 3)),
    (0b01100111, (1, 3)),
    (0b11101110, (1, 3)),
]
# └── p8e0     │  │
#              │  └── regime length
#              └── regime value


@pytest.mark.parametrize("test_input,expected", test_k_params)
def test_k(test_input, expected):
    assert calc_k(test_input) == expected


test_tmp = [
    (0b01001100, 0b10110000),
    (0b01100100, 0b10100000),
    (0b00010000, 0b10000000),
    (0b01011010, 0b11101000),
    (0b01010001, 0b11000100),
    (0b01000000, 0b10000000),
    (0b01110001, 0b10010000),
    (0b01000001, 0b10000100),
    (0b00000101, 0b10100000),
    (0b01110111, 0b11110000),
    (0b01100010, 0b10010000),
    (0b01000000, 0b10000000),
]


@pytest.mark.parametrize("test_input,expected", test_tmp)
def test_tmp(test_input, expected):
    assert separate_bits(test_input)[1] == expected


test_mul = [
    ((0x7A, 0x58), 0x7D),
    ((0x42, 0x76), 0x77),
    ((0x03, 0x29), 0x02),
]  # │      │       │
# └─ a   └─ b    └─ P<8,0>::(a * b)
@pytest.mark.parametrize("test_input,expected", test_mul)
def test_mul(test_input, expected):
    a, b = test_input
    assert sp.posit8(bits=mul(a, b).z) == sp.posit8(
        bits=expected
    )  # sp.posit8(bits=a) * sp.posit8(bits=b)


"""
>>> import softposit as sp
>>> sp.posit8(bits=0x41) + sp.posit8(bits=0xe)
1.25
>>> _.toBinaryFormatted()
01001000
>>>
"""
test_add = [
    ((0x74, 0x51), 0x77),
    ((0x72, 0x71), 0x79),
    ((0xac, 0x10), 0xb4),
    ((0x71, 0x8f), 0x00),
    ((0x02, 0x04), 0x06),
    ((0x7f, 0x1),  0x7f),
    ((0xf1, 0x4c), 0x44),
    ((0x00, 0x4c), 0x4c),
    ((0x70, 0x40), 0x72),
    ((0x41, 0xbc), 0xfa),
    ((0x41, 0x0e), 0x48),
    ((0x68, 0x5c), 0x72),
]   # │      │       │
    # └─ a   └─ b    └─ P<8,0>::(a + b)
@pytest.mark.parametrize("test_input,expected", test_add)
def test_add(test_input, expected):
    a, b = test_input
    assert sp.posit8(bits=add(a,b).z) == sp.posit8(bits=expected)




# a = random.sample(range(0,5), 5)
# b = random.sample(range(0,5), 5)
# c = [i+j for i,j in zip(a,b)]

# [((i,j),k) for i,j,k in zip(a,b,c)]

