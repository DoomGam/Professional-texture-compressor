# Compressor Texture Profissioner (.ctp)

O **Compressor Texture Profissioner (CTP)** é uma solução completa de compressão, streaming e gerenciamento de memória para texturas binárias em jogos feitos em **HaxeFlixel / OpenFL**, desenvolvida sob medida para **mods mobile de Friday Night Funkin' (Android e iOS)**.

O ecossistema automatiza a conversão de spritesheets `.png` para o formato proprietário `.ctp` durante a compilação (`lime build`), reduzindo o consumo de memória RAM/VRAM e eliminando travamentos em aparelhos intermediários e fracos.

---

## 📌 Para que serve?

Spritesheets em alta resolução no FNF consomem muita VRAM. O uso de imagens `.png` tradicionais no mobile frequentemente causa:
* **Crashes por falta de memória (*Out of Memory - OOM*)** ao carregar sprites grandes ou alternar entre músicas.
* **Quedas brutas de FPS (Gargalos de GPU/CPU)** ao decodificar imagens grandes em tempo real.
* **Artefatos visuais ("Bloquinhos falhados" ou bordas pretas)** causados por compressões incorretas ou dimensões não alinhadas.

O formato `.ctp` resolve esses problemas reduzindo o overhead do cabeçalho de imagem, sanitizando canais de transparência e alinhando os dados da textura para leitura direta em bloco na GPU.

---

## ⚙️ Como funciona?

O pipeline opera automaticamente entre o momento em que você edita os assets e a compilação final da APK/IPA:

```text
  [ Pasta de Assets ]
  └── 8x8.ctp (Preset) + boyfriend.png
          │
          ▼  (Pre-Build Hook via Lime/OpenFL)
  [ ctp_builder.py ]
          │
          ├─► Auto-Padding: Ajusta largura/altura para múltiplos do bloco.
          ├─► Alpha Guard: Elimina ruídos em pixels transparentes (previne bordas escuras).
          └─► Header v2: Grava o cabeçalho binário CTP2 de 20 bytes.
          │
          ▼
  [ boyfriend.ctp ] ──► [ CTPDecoder.hx / CTPGraphic.hx ] ──► GPU Memory (RAM)
