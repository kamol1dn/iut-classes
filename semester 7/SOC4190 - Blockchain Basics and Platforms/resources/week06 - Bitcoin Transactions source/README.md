# Week 6 — Bitcoin Transactions: source files

From eClass ubfile **72468** (`l06tx.zip`, 1,045 bytes), posted with the
Part 2 video (VOD 72467) on 2026-10-18.

| File | What it is |
|---|---|
| `payment.hex` | A raw, signed legacy (non-SegWit) transaction, version 2, 1 input, 225 bytes |
| `payment_plus1.hex` | The same transaction with **one hex digit changed** (byte at offset 154: `0` → `1`) |
| `txid.py` | Computes the txid: `SHA256(SHA256(raw))`, byte-reversed for display |

```bash
python txid.py payment.hex        # 225 bytes  txid: d9f91d3f…706dd6
python txid.py payment_plus1.hex  # 225 bytes  txid: 3babb094…1fed1e
```

**The point:** a one-bit edit to the transaction gives a completely unrelated txid. A txid
is a commitment to every byte of the transaction, so you can't tamper with one
without it being noticed. It also shows the **byte-reversal** convention: explorers
display the hash in reverse byte order from what SHA-256 outputs.
