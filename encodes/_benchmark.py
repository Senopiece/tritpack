import random
from typing import List

from tqdm import tqdm
from datastructs import Octet, Smit
from encodes import checksum

bdc = 0.01  # chance for a bit to be defect
ldc = 0.01  # chance for a bit to be a start of a line of defects
dl = 4  # mean defect length
dso = 2  # mean data offset in data shift
packet_len = 128  # as it would be in bits
runs = 10000
encode = checksum.encode
decode = checksum.decode


def defect(octet: Octet):
    return Octet((octet.value + random.randint(1, 7)) % 8)


def spread(octets: List[Octet]):
    return list(defect(octet) if random.random() < bdc else octet for octet in octets)


def near(octets: List[Octet]):
    c = -1
    res: List[Octet] = []
    for octet in octets:
        if random.random() < ldc:
            c = dl
        res.append(defect(octet) if c > 0 else octet)
        c -= 1
    return res


def const_line(octets: List[Octet]):
    c = -1
    s = Octet(random.randint(0, 7))
    res: List[Octet] = []
    for octet in octets:
        if random.random() < ldc:
            c = max(1, int(random.normalvariate(dl, 2)))
            s = Octet(random.randint(0, 7))
        res.append(s if c > 0 else octet)
        c -= 1
    return res


def data_shift(octets: List[Octet]):
    c = 0
    res: List[Octet] = []
    for i in range(len(octets)):
        if random.random() < ldc:
            c += max(1, int(random.normalvariate(dso, 2)))
        i += c
        if i >= len(octets):
            break
        res.append(octets[i])
    return res


ts = 0

affects = (spread, near, const_line, data_shift)

for affect in affects:
    defected = 0
    found_defects = 0
    truncated_count = 0
    found_truncated = 0
    corrected_defects = 0

    print(f"Defect type: {affect.__name__}")
    for _ in tqdm(range(runs)):
        # generate msg on the carrier signal
        msg = int("".join(random.choice("01") for _ in range(packet_len)), 2)

        # encode
        encoded = encode(msg)

        # convert to carrying signal
        signal = list(Octet(smit.value + 1) for smit in encoded)

        # corrupt
        got_signal = affect(signal)
        had_defects = signal != got_signal
        defected += 1 if had_defects else 0

        truncated = False

        got_smits: list[Smit] = []
        for octet in got_signal:
            if octet.value == 0:
                truncated = True
                truncated_count += 1
                break
            got_smits.append(Smit(octet.value - 1))

        # decode
        try:
            decoded = decode(got_smits)

            # verify
            if not had_defects and decoded != msg and not truncated:
                print("Expected:", msg)
                print("Decoded:", decoded)
                raise Exception("NOT ACCEPTABLE! Invalid decoding of a valid packet")
            elif had_defects and decoded == msg:
                corrected_defects += 1

        except ValueError:
            if not had_defects:
                raise Exception("NOT ACCEPTABLE! False positive error detected!")
            found_defects += 1
            if truncated:
                found_truncated += 1

    print(f"Was defected: {defected}/{runs} ({defected/runs*100:.1f}%)")
    print(
        f"Found defects: {found_defects}/{defected} ({found_defects/defected*100:.1f}%)"
    )
    print(
        "Miss rate:",
        (
            f"1 per {defected//(defected - found_defects)} defects"
            if defected != found_defects
            else "unknown"
        ),
    )
    print(
        f"Corrected defects: {corrected_defects}/{defected} ({corrected_defects/defected*100:.1f}%)"
    )
    print(
        f"Truncated: {truncated_count}/{defected} ({truncated_count/defected*100:.1f}%)"
    )
    print(
        "Found truncated:",
        (
            f"{found_truncated}/{truncated_count} ({found_truncated/truncated_count*100:.1f}%)"
            if truncated_count != 0
            else "N/A"
        ),
    )
    score = (found_defects + corrected_defects) / defected
    ts += score
    print(f"Score: {score*100 :.2f}")
    print()

print(f"Mean score: {ts*100 / len(affects):.2f}")
