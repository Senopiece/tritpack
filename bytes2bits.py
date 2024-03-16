def bytes2bits(bytes: bytes):
    return bin(int.from_bytes(bytes, byteorder="big"))[2:].rjust(8 * len(bytes), "0")


def bits2bytes(s: str):
    return int(s, 2).to_bytes(len(s) // 8, byteorder="big")


# Example
if __name__ == "__main__":
    binary_data = b"\x04\x05\x13"
    bits_result_binary = bytes2bits(binary_data)

    print(f"Binary data: {binary_data}")
    print(f"Equivalent bits: {bits_result_binary}")
    print(f"Back to bytes: {bits2bytes(bits_result_binary)}")
