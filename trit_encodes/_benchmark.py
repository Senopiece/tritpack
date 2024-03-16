import random

from tqdm import tqdm
from datastructs import Trit
from trit_encodes import norep, ignorant

bdc = 0.01  # chance for a bit to be defect
ldc = 0.01  # chance for a bit to be a start of a line of defects
dl = 4  # mean defect length
dso = 2  # mean data offset in data shift
packet_len = 64
runs = 10000
encode = norep.encode
decode = norep.decode

CODES = ("01", "10", "11")
RCODES = {
    "01": Trit.A,
    "10": Trit.B,
    "11": Trit.C,
}


def defect(bit: str):
    return "1" if bit == "0" else "0"


def spread(ebits: str):
    return "".join(defect(bit) if random.random() < bdc else bit for bit in ebits)


def near(ebits: str):
    c = -1
    res = ""
    for bit in ebits:
        if random.random() < ldc:
            c = dl
        res += defect(bit) if c > 0 else bit
        c -= 1
    return res


def const_line(ebits: str):
    c = -1
    s = random.choice("01")
    res = ""
    for bit in ebits:
        if random.random() < ldc:
            c = max(1, int(random.normalvariate(dl, 2)))
            s = random.choice("01")
        res += s if c > 0 else bit
        c -= 1
    return res


def data_shift(ebits: str):
    c = 0
    res = ""
    for i in range(len(ebits)):
        if random.random() < ldc:
            c += max(1, int(random.normalvariate(dso, 2)))
        i += c
        if i >= len(ebits):
            break
        res += ebits[i]
    return res + ("0" if len(res) % 2 == 1 else "")


for affect in (spread, near, const_line, data_shift):
    defected = 0
    found_defects = 0
    truncated_count = 0
    found_truncated = 0

    print(f"Defect type: {affect.__name__}")
    for _ in tqdm(range(runs)):
        # generate
        bits = "".join(random.choice("01") for _ in range(packet_len))

        # encode
        encoded = encode(bits)

        # convert to extended bits
        ebits = "".join(CODES[trit.value] for trit in encoded)

        # corrupt
        gotebits = affect(ebits)
        had_defects = ebits != gotebits
        defected += 1 if had_defects else 0

        truncated = False

        gotetrits: list[Trit] = []
        for i in range(len(gotebits) // 2):
            couple = gotebits[2 * i] + gotebits[2 * i + 1]
            if couple == "00":
                truncated = True
                truncated_count += 1
                break
            gotetrits.append(RCODES[couple])

        # decode
        try:
            decoded = decode(gotetrits)

            # verify
            if not had_defects and decoded != bits and not truncated:
                print("Expected:", bits)
                print("Decoded:", decoded)
                raise Exception("NOT ACCEPTABLE! Invalid decoding of a valid packet")

        except ValueError:
            if not had_defects:
                raise Exception("NOT ACCEPTABLE! False positive error detected!")
            found_defects += 1
            if truncated:
                found_truncated += 1

    print(f"Was defected: {defected}/{runs} ({defected/runs*100:.1f}%)")
    print(f"Found defects: {found_defects}/{runs} ({found_defects/runs*100:.1f}%)")
    print(f"Truncated: {truncated_count}/{runs} ({truncated_count/runs*100:.1f}%)")
    print(
        f"Found truncated: {found_truncated}/{runs} ({found_truncated/runs*100:.1f}%)"
    )
    print()
