# Quantum-Verifiable-Beacon
Publicly verifiable randomness beacon built from a quantum random number generator (QRNG) based on a heralded SPDC single-photon source with a 50:50 beamsplitter.

Author:
  Utkarsh Kumar Singh
  Defence Institute of Advanced Technology (DIAT), Pune, India

Repository:
  https://github.com/utkarsh207543/Quantum-Verifiable-Beacon

Overview

This project implements a publicly verifiable randomness beacon
using quantum entropy generated from a heralded SPDC single-photon
source with a 50:50 beamsplitter.

Key Features:
  - Raw quantum random bits from single-photon events
  - SHA-256 hashing per epoch (default 2048 bits)
  - Forward hash-chain for tamper-evident logging
  - Public verification using CyberChef or OpenSSL

Repository Structure

data.txt                  - Raw quantum random bit sequence
table_beacon_epochs.txt   - Epoch table with SHA-256 hashes and hash-chain
beacon_epochs.py          - Script for epoch table generation
verify_chain.py           - Script for chain verification
README.txt                - This file

Requirements

- Python 3.7 or higher
- No external dependencies (uses Python's hashlib module)

Quick Start

1. Clone the repository:
   git clone https://github.com/utkarsh207543/Quantum-Verifiable-Beacon.git
   cd Quantum-Verifiable-Beacon

2. Generate the epoch table:
   python beacon_epochs.py -i data.txt -o table_beacon_epochs.txt --epoch-bits 2048 --chain

   Output:
   [INFO] Processed 262144 bits.
   [INFO] Generated 128 epochs.
   [OK] Table saved as table_beacon_epochs.txt

3. Verify the beacon chain:
   python verify_chain.py -i data.txt -t table_beacon_epochs.txt --epoch-bits 2048

   Output:
   [OK] Verification passed for all epochs.

CyberChef Verification

Manual verification of epochs using CyberChef:

1. Open CyberChef at:
   https://gchq.github.io/CyberChef/

2. Verify Epoch 0 Hash:
   - Copy the first 2048 bits (no spaces) from data.txt
   - In CyberChef:
     a) Remove Whitespace
     b) Apply SHA2 → SHA-256, Rounds = 64, Output = Hex
   - Expected Output:
     a2abcb1fa8be15b750ea2fb4eb2342929c825eb7b4e64540f74f69af130d5034

3. Verify Chain for Epoch 0:
   - Concatenate:
     a2abcb1fa8be15b750ea2fb4eb2342929c825eb7b4e64540f74f69af130d5034
     0000000000000000000000000000000000000000000000000000000000000000
   - From Hex → SHA2 → SHA-256
   - Expected Output:
     1f0c88a5f8e1977c6a25f860cc8da958c0d7b0d7dbad6c8171ff6152b99b87cb

4. Verify Chain for Epoch 1:
   - Concatenate Epoch 1 hash and Epoch 0 chain hash
   - From Hex → SHA2 → SHA-256
   - Expected Output:
     9d02e9620a729ada89cac661c2ae64cc5d5547ca90b1db383f816394d56d879f


Command-Line Verification (OpenSSL)

Verify Epoch 0 hash:
   head -c 2048 data.txt | tr -d '\n' | openssl dgst -sha256

Expected output:
   (stdin)= a2abcb1fa8be15b750ea2fb4eb2342929c825eb7b4e64540f74f69af130d5034

Applications

- Cryptographic lotteries and consensus protocols
- Scientific reproducibility in quantum optics experiments
- Auditable randomness for blockchain or secure systems

Citation

If you use this repository, please cite:

@misc{singh2025quantumbeacon,
  title={Quantum-Sourced Verifiable Randomness Beacon Using an SPDC Heralded Single-Photon QRNG with a 50:50 Beam Splitter},
  author={Singh, Utkarsh Kumar},
  year={2025},
  note={Available at https://github.com/utkarsh207543/Quantum-Verifiable-Beacon}
}

License
This project is released under the MIT License. See LICENSE for details.
