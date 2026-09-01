# CTP (.ctp) Binary Format Specification (v1.1.0)

## Overview
The CTP (Compressor Texture Profissioner) format is a lightweight binary container designed for fast GPU streaming and reduced RAM footprint in FNF mobile engines (HaxeFlixel/OpenFL).

---

## 1. Header Structure (v2 - 20 Bytes)

All integers are stored in **Big-Endian** byte order.

| Offset (Bytes) | Field Name | Type | Description |
|---|---|---|---|
| `0x00 - 0x03` | Magic Header | ASCII (`4s`) | Signature bytes: `CTP2` |
| `0x04 - 0x07` | Width | uint32 | Image width in pixels |
| `0x08 - 0x0B` | Height | uint32 | Image height in pixels |
| `0x0C - 0x0F` | Block Size | uint32 | Preset block size ($4\times4$, $6\times6$, $8\times8$, $10\times10$) |
| `0x10` | Compression Mode | uint8 | `0x00` = Raw RGBA, `0x01` = Block Palette Quantized |
| `0x11 - 0x13` | Reserved | Bytes | Alignment padding bytes for direct C++ GPU memory pointer mapping |

---

## 2. Payload Layout (v1.1.0)

Depending on the `Compression Mode` flag set at offset `0x10`:

### Mode 0x00 (Legacy RGBA Stream)
- **Data Stream**: Compressed RGBA raw byte stream (Zlib/LZ4 stream).

### Mode 0x01 (Block Palette Quantized - v1.1.0)
1. **Palette Table Header**: `uint16` specifying total unique colors in the local palette.
2. **Color Palette Data**: Interleaved RGBA bytes (`Count * 4` bytes).
3. **Index Map**: LZ4/Zlib compressed block index map pointing to color palette references.

---

## 3. Alpha Guard & Vector Edge Rule
To maintain vector line integrity on FNF sprites:
- Alpha values strictly equal to `0x00` skip block quantization calculations.
- Edge pixels adjacent to full transparency are locked to full opacity color channels to eliminate black artifact borders on mobile GPU interpolation.
- 
