#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_chain.py
===============
Verify integrity of the beacon table by checking:
1. SHA-256 of each epoch slice.
2. Forward hash-chain consistency.
"""

import argparse
import hashlib
import pathlib
import sys

def load_bitstring(path: str) -> str:
    """Load and clean binary bitstring from file."""
    s = pathlib.Path(path).read_text(encoding="utf-8", errors="strict")
    return "".join(ch for ch in s if ch in "01")

def verify_chain(bits: str, table_path: str, epoch_bits: int):
    """Verify the hash and chain for each epoch."""
    errors = 0
    prev_chain = b"\x00" * 32

    with open(table_path, "r", encoding="utf-8") as f:
        header = f.readline().strip().split("\t")
        has_chain = "Chain_hex" in header

        for line in f:
            cols = line.strip().split("\t")
            epoch = int(cols[0])
            start, end = int(cols[1]), int(cols[2])
            sha_expected = cols[4]
            chain_expected = cols[5] if has_chain else None

            # Recompute epoch hash
            segment = bits[start:end]
            epoch_hash = hashlib.sha256(segment.encode("ascii")).digest()
            epoch_hex = epoch_hash.hex()

            if epoch_hex != sha_expected:
                print(f"[ERROR] Epoch {epoch}: SHA mismatch!")
                errors += 1

            # Recompute chain if enabled
            if has_chain:
                chain_hash = hashlib.sha256(epoch_hash + prev_chain).digest()
                chain_hex = chain_hash.hex()
                if chain_hex != chain_expected:
                    print(f"[ERROR] Epoch {epoch}: Chain mismatch!")
                    errors += 1
                prev_chain = chain_hash

    if errors == 0:
        print("[OK] Verification passed for all epochs.")
    else:
        print(f"[FAIL] Verification failed with {errors} mismatch(es).")

def main():
    parser = argparse.ArgumentParser(description="Verify hash and chain integrity of beacon epochs.")
    parser.add_argument("-i", "--input", required=True, help="Path to input data.txt file.")
    parser.add_argument("-t", "--table", required=True, help="Path to table_beacon_epochs.txt file.")
    parser.add_argument("--epoch-bits", type=int, default=2048, help="Number of bits per epoch (default: 2048).")
    args = parser.parse_args()

    bits = load_bitstring(args.input)
    verify_chain(bits, args.table, args.epoch_bits)

if __name__ == "__main__":
    main()
