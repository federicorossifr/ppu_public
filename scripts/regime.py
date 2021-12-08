from numpy import inf
import pytest


# class Regime:
#     (reg_s, reg_len) = (None, None)
#     k = None

#     def __init__(self, size, reg_s=None, reg_len=None, k=None):
#         self.size = size

#         if ((reg_s, reg_len) == (None, None)) and (k != None):
#             self._init_k(k)
#         elif (reg_s != None and reg_len != None) and (k == None):
#             if bool(reg_s).real != reg_s:
#                 print("reg_s has to be either 0 or 1.")
#             elif reg_len <= 1:
#                 print(
#                     "`reg_len` has to be > 0. It can be 1 but it's an edge case not yet handled."
#                 )
#             else:
#                 self._init_reg_s_reg_len(reg_s, reg_len)
#         else:
#             self._init_k(-inf)
#             # print('initialized a "subnormal" regime')

#     def _init_k(self, k):
#         if (self.reg_s, self.reg_len) == (None, None):
#             self.k = k
#             self._calc_reg_s_reg_len()

#     def _init_reg_s_reg_len(self, reg_s, reg_len):
#         if self.k == None:
#             self.reg_s = reg_s
#             self.reg_len = reg_len
#             self._calc_k()

#     def _calc_reg_s_reg_len(self):
#         """Given k, computes leftmost regime bit (reg_s) and regime length (reg_len)"""
#         if self.k == -inf:
#             self.reg_s = None
#             self.reg_len = None
#         elif self.k >= 0:
#             self.reg_s = 1
#             if self.k < self.size - 1:
#                 self.reg_len = self.k + 2
#             else:
#                 self.reg_len = self.k + 1
#         else:
#             self.reg_s = 0
#             if -self.k < self.size - 1:
#                 self.reg_len = -self.k + 1
#             else:
#                 self.reg_len = -self.k

#     def _calc_k(self):
#         """Given leftmost regime bit (reg_s) and regime length (reg_len), computes k"""
#         if self.reg_s == 1:
#             self.k = self.reg_len - 2
#         else:
#             self.k = -(self.reg_len - 1)

#     def calc_reg_bits(self):
#         if self.k == -inf:
#             return 0
#         elif self.k >= 0:
#             return (2 ** (self.k + 1) - 1) << 1
#         else:
#             return 1
#             mask = 2 ** self.size - 1
#             return ~((2 ** (-self.k) - 1) << 1) & mask

#     # def get_bits(self, size):
#     #     mask = 2**size - 1
#     #     return self.bits  # ~ (~1 << (self.reg_len - 2) << 1) & mask

#     def __eq__(self, other):
#         if isinstance(other, self.__class__):
#             return self.__dict__ == other.__dict__
#         else:
#             return False

#     def __repr__(self):
#         return f"(reg_s, reg_len) = ({self.reg_s}, {self.reg_len}) -> k = {self.k} | {self.calc_reg_bits()}"


# tb = [
#     (Regime(size=8, k=1).calc_reg_bits(), 0b00000110),
#     (Regime(size=8, k=2).calc_reg_bits(), 0b00001110),
#     (Regime(size=8, k=0).calc_reg_bits(), 0b00000010),
#     (Regime(size=8, k=-3).calc_reg_bits(), 0b00000001),
#     (Regime(size=8, reg_s=1, reg_len=4).calc_reg_bits(), 0b00001110),
#     (Regime(size=8).calc_reg_bits(), 0b00000000),
#     (Regime(size=8, reg_s=1, reg_len=5), Regime(size=8, k=3)),
#     (Regime(size=16, reg_s=1, reg_len=15), Regime(size=16, k=13)),
#     (
#         Regime(size=16, reg_s=1, reg_len=15),
#         Regime(size=16, k=14),
#     ),  # edge case: only ones, no trailing 0 like any other regime sequence.
#     # when printed it's actually >> 1 and the rightmost bit is chopped off.
# ]


# @pytest.mark.parametrize("left,right", tb)
# def test_regime(left, right):
#     assert left == right

################################################################################


class Regime:
    def __init__(self, size, k=None):
        self.size = size
        self.k = k

    @property
    def reg_s(self):
        if self.k == None:  # 0 or inf
            return None
        elif self.k >= 0:
            return 1
        else:
            return 0

    @property
    def reg_len(self):
        if self.k == None:  # 0 or inf
            return None
        elif self.k >= 0:
            return self.k + 2
        else:
            return -self.k + 1

    def calc_reg_bits(self):
        if self.k == None:
            return 0
        elif self.k >= 0:
            return (2 ** (self.k + 1) - 1) << 1
        else:
            return 1
            mask = 2 ** self.size - 1
            return ~((2 ** (-self.k) - 1) << 1) & mask

    # def get_bits(self, size):
    #     mask = 2**size - 1
    #     return self.bits  # ~ (~1 << (self.reg_len - 2) << 1) & mask

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __repr__(self):
        return f"(reg_s, reg_len) = ({self.reg_s}, {self.reg_len}) -> k = {self.k} | {self.calc_reg_bits()}"


if __name__ == "__main__":
    print(f"run `pytest regime.py -v` to run the tests.")


tb = [
    (Regime(size=8, k=1).calc_reg_bits(), 0b00000110),
    (Regime(size=8, k=2).calc_reg_bits(), 0b00001110),
    (Regime(size=8, k=0).calc_reg_bits(), 0b00000010),
    (Regime(size=8, k=-3).calc_reg_bits(), 0b00000001),
    (Regime(size=8).calc_reg_bits(), 0b00000000),
    (
        Regime(size=16, k=14).calc_reg_bits(),
        0b1111111111111110,
    ),  # technically true but it needs to be >> 1 later on because it doesn't fit.
    (Regime(size=16, k=13).calc_reg_bits(), 0b111111111111110),
]


@pytest.mark.parametrize("left,right", tb)
def test_regime(left, right):
    assert left == right