from . import rust

def decode_bc1(data: bytes, width: int, height: int):
    return rust.decode_bcn(data, width, height, "bc1")

def decode_bc3(data: bytes, width: int, height: int):
    return rust.decode_bcn(data, width, height, "bc3")

def decode_bc5(data: bytes, width: int, height: int):
    return rust.decode_bcn(data, width, height, "bc5")