#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
beacon_epochs.py
================
Generate epoch-based SHA-256 hashes and an optional forward hash-chain
from a binary bitstring (0s and 1s) for a publicly verifiable randomness beacon.
"""

import argparse
import hashlib
import pathlib
import sys

def load_bitstring(path: str) -> str:
    """Load and clean bitstring (remove whitespace, validate only 0 and 1)."""
    s = pathlib.Path(path).read_text(encoding="utf-8", errors="strict")
    clean = "".join(ch for ch in s if ch in "01")
    stripped = "".join(ch for ch in s if not ch.isspace())
    if any(ch not in "01" for ch in stripped):
        bad = {ch for ch in stripped if ch not in "01"}
        raise ValueError(f"Invalid characters found: {sorted(bad)}")
    if len(clean) == 0:
        raise ValueError("No bits found after cleaning input file.")
    return clean

def iter_epochs(bits: str, epoch_bits: int, chain: bool):
    """Yield tuples: (epoch, start, end, length, epoch_hash_hex, chain_hex or None)."""
    total_epochs = len(bits) // epoch_bits
    prev_chain = b"\x00" * 32  # Start of hash-chain (32 zero bytes)
    for i in range(total_epochs):
        start = i * epoch_bits
        end = start + epoch_bits
        chunk = bits[start:end]

        epoch_hash = hashlib.sha256(chunk.encode("ascii")).digest()
        epoch_hex = epoch_hash.hex()

        if chain:
            chain_bytes = hashlib.sha256(epoch_hash + prev_chain).digest()
            chain_hex = chain_bytes.hex()
            prev_chain = chain_bytes
        else:
            chain_hex = None

        yield (i, start, end, len(chunk), epoch_hex, chain_hex)

def write_table(rows, out_path: str, include_chain: bool):
    """Write epoch table to output file."""
    with open(out_path, "w", encoding="utf-8") as f:
        if include_chain:
            f.write("Epoch\tStart\tEnd\tBits\tSHA256_hex\tChain_hex\n")
        else:
            f.write("Epoch\tStart\tEnd\tBits\tSHA256_hex\n")
        for row in rows:
            e, s, t, blen, h, ch = row
            if include_chain:
                f.write(f"{e}\t{s}\t{t}\t{blen}\t{h}\t{ch}\n")
            else:
                f.write(f"{e}\t{s}\t{t}\t{blen}\t{h}\n")

def main():
    parser = argparse.ArgumentParser(description="Generate verifiable epochs from a bitstring file.")
    parser.add_argument("-i", "--input", required=True, help="Path to input bitstring file (data.txt).")
    parser.add_argument("-o", "--output", default="table_beacon_epochs.txt", help="Output table filename.")
    parser.add_argument("--epoch-bits", type=int, default=2048, help="Number of bits per epoch (default: 2048).")
    parser.add_argument("--chain", action="store_true", help="Include forward hash-chain for tamper-evidence.")
    args = parser.parse_args()

    try:
        bits = load_bitstring(args.input)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    rows = list(iter_epochs(bits, args.epoch_bits, args.chain))
    write_table(rows, args.output, args.chain)

    print(f"[INFO] Processed {len(bits)} bits.")
    print(f"[INFO] Generated {len(rows)} epochs.")
    print(f"[OK] Table saved as {args.output}")

if __name__ == "__main__":
    main()
