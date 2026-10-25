# Week 7 — Mining source files

`[SOURCE FILES] Mining` (eClass ubfile 72937, posted 2026-10-25 with Homework 2), unzipped from
`mining_source_files.zip`. The lecture code for proof of work.

| File | What it does |
|---|---|
| `pow.py` | `python pow.py "<text>" <zeros>`: tries nonce 0, 1, 2 … until SHA-256 of `"<text> <nonce>"` starts with that many hex zeros, then prints the nonce and the time. Each extra zero is about 16× more work |
| `blockhash.py` | `python blockhash.py <file.hex>`: double SHA-256 of an 80-byte block header, printed reversed. Same idea as week 6's `txid.py` |
| `header_968391.hex` | The real header of Bitcoin block 968,391 |
| `header_968391_nonce_plus1.hex` | The same header with the nonce raised by 1: the hash becomes unrelated and loses its leading zeros |
