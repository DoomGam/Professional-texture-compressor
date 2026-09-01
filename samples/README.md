# CTP Texture Compression Sample

This folder provides a ready-to-test setup for verifying `.ctp` texture conversion and runtime loading in Friday Night Funkin' (HaxeFlixel/OpenFL).

## Contents
- **`character_folder/`**: Simulated character folder containing a sample block configuration (`8x8.ctp`) and test texture instructions.

## Quick Test Instructions

1. Place any PNG sprite (e.g. `boyfriend.png`) inside `samples/character_folder/`.
2. Run the CTP builder tool manually from the project root:
   ```bash
   python encoder/ctp_builder.py samples/character_fold
