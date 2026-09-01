# Compressor Texture Profissioner (.ctp)

A high-performance texture compression library designed specifically for **Friday Night Funkin' (FNF) Mobile/iOS** engines using HaxeFlixel and OpenFL.

## Features (v1.0.0 Target)
- Optimized RAM footprint for iOS low-memory environments.
- High-fidelity transparency (Alpha channel) preservation.
- Fast runtime decoding for seamless spritesheet animations.

- # Preset Block Configurations

To compress sprites inside a specific folder during build time, copy one of the preset files below and paste it directly into your target sprites folder (e.g., `assets/characters/` or `assets/images/`).

## Available Block Presets (v1.0.0)

- **`4x4.ctp`**: High quality / Low compression. Recommended for main characters with fine details.
- **`6x6.ctp`**: Balanced quality and compression. Ideal for stage elements and UI.
- **`8x8.ctp`**: High compression. Great for background characters and large spritesheet sequences on iOS.
- **`10x10.ctp`**: Ultra compression. Maximum RAM savings for heavy background assets.

- ## Running Benchmarks & Tests

You can test the texture encoder and inspect binary headers using the built-in benchmark script:

```bash
python tests/test_benchmark.py


## How it works

During the build process (`lime build ios` or `lime build android`), the CTP build tool scans all asset folders. When it detects a `.ctp` preset file inside a folder, it automatically converts all `.png` textures in that directory using the designated block size.

## Installation

Add this library to your project via `hmm.json`:
```json
{
  "dependencies": [
    {
      "name": "Profissional-texture-compressor",
      "type": "git",
      "url": "[https://github.com/DoomGam/Professional-texture-compressor](https://github.com/DoomGam/Professional-texture-compressor/tree/main)"
    }
  ]
}
