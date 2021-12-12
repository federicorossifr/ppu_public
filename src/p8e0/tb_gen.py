import softposit as sp
import random
import datetime
import argparse
import enum

import p8e0

N = 8  # num bits

NUM_RANDOM_TEST_CASES = 200
TEST_ALL_COMBINATIONS = False


class Tb(enum.Enum):
    MUL = "mul"
    ADD = "add"

    def __str__(self):
        return self.value


parser = argparse.ArgumentParser(description="Generate test benches")
parser.add_argument(
    "--operation",
    type=Tb,
    choices=list(Tb),
    required=True,
    help="Type of test bench: adder/multiplier/etc",
)
parser.add_argument(
    "--shuffle-random", type=bool, default=False, required=False, help="Shuffle random"
)

args = parser.parse_args()


if args.shuffle_random == False:
    random.seed(3)


ans_preamble = f"""/*-------------------------------------+
 | autogenerated by tb_gen.py on       |
 | {datetime.datetime.now().strftime('%c')}            |
 +-------------------------------------*/
"""


if TEST_ALL_COMBINATIONS:
    list_a = []
    list_b = []
    for i in range(2 ** N):
        for j in range(i, 2 ** N):
            list_a.append(i)
            list_b.append(j)
    print(f"{len(list_a)=}")
else:  # test NUM_RANDOM_TEST_CASES tests.
    list_a = random.sample(range(0, 2 ** N - 1), NUM_RANDOM_TEST_CASES)
    list_b = random.sample(range(0, 2 ** N - 1), NUM_RANDOM_TEST_CASES)

# print 8-bits hex or bin repr of `val`. _bin8(3) = "0b00000011"
_hex8 = lambda val: f"8'h{val:02x}"
_bin8 = lambda val: f"8'b{val:08b}"


# force add a few special testcases first
list_a = [0b01111010, 0x00, 0x80] + list_a
list_b = [0b01011000, 0x03, 0x90] + list_b


PLACEHOLDER = "/*{add stuff here}*/"

############### multiplier ################

if args.operation == Tb.MUL:

    body = ""
    counter = 0
    for a, b in zip(list_a, list_b):
        ans_p8e0_mul = p8e0.mul(a, b)

        ui_a = ans_p8e0_mul.ui_a
        ui_b = ans_p8e0_mul.ui_b
        z = ans_p8e0_mul.z
        k_a = ans_p8e0_mul.k_a
        k_b = ans_p8e0_mul.k_b
        k_c = ans_p8e0_mul.k_c
        frac_a = ans_p8e0_mul.frac_a
        frac_b = ans_p8e0_mul.frac_b
        frac16 = ans_p8e0_mul.frac16
        rcarry = ans_p8e0_mul.rcarry

        counter += 1

        body += f"""    
                    test_no =   {counter};
                    a =         {_hex8(a)}; /* {sp.posit8(bits=a)} */
                    b =         {_hex8(b)}; /* {sp.posit8(bits=b)} */
                    a_ascii =   \"{sp.posit8(bits=a)}\";
                    b_ascii =   \"{sp.posit8(bits=b)}\";
                    ui_a_exp =  {_hex8(ui_a)};
                    ui_b_exp =  {_hex8(ui_b)};
                    k_a_exp =   {k_a};
                    k_b_exp =   {k_b};
                    k_c_exp =   {k_c};
                    frac_a_exp = {_hex8(frac_a)};
                    frac_b_exp = {_hex8(frac_b)};
                    frac16_exp = 16'h{frac16:04x};
                    rcarry_exp = {1 if rcarry else 0};
                    z_exp      = {_hex8(z)}; /* {sp.posit8(bits=z)} */
                    z_ascii    = \"{sp.posit8(bits=z)}\";
            #10;
        """

    ans = ans_preamble
    with open("tb_p8e0_mul_template.sv", "r") as f:
        ans += f.read()

    ans = ans.replace(PLACEHOLDER, body)

    output = "tb_p8e0_mul.sv"
    with open(output, "w") as f:
        print(f"Wrote {output}; {f.write(ans)} characters")


############### addder ################

if args.operation == Tb.ADD:

    counter = 0
    body = ""
    for a, b in zip(list_a, list_b):
        if (a ^ b) & 0x80 == 0:  # <-- only testing opposite sign numbers, remove later
            ans_p8e0_add = p8e0.add(a, b)
            z = ans_p8e0_add.z

            counter += 1

            body += f"""    
                        test_no =   {counter};
                        a =         {_hex8(a)}; /* {sp.posit8(bits=a)} */
                        b =         {_hex8(b)}; /* {sp.posit8(bits=b)} */
                        a_ascii =   \"{sp.posit8(bits=a)}\";
                        b_ascii =   \"{sp.posit8(bits=b)}\";
                        z_exp      = {_hex8(z)}; /* {sp.posit8(bits=z)} */
                        z_ascii    = \"{sp.posit8(bits=z)}\";
                #10;
            """

    ans = ans_preamble
    with open("tb_p8e0_add_template.sv", "r") as f:
        ans += f.read()

    ans = ans.replace(PLACEHOLDER, body)

    output = "tb_p8e0_add.sv"
    with open(output, "w") as f:
        print(f"Wrote {output}; {f.write(ans)} characters")
