# .ctp File Format Specification (v1.0.0)

A `.ctp` file is a binary container structured as follows:

1. **Header (16 Bytes):**
   - Magic Bytes: `CTP1` (4 bytes)
   - Width: `uint32` (4 bytes)
   - Height: `uint32` (4 bytes)
   - Flags / Compression Type: `uint32` (4 bytes)

2. **Payload:**
   - Compressed pixel data payload (RGB + Alpha channels compressed using optimized quantizer and LZ4/ZSTD stream).
   -
