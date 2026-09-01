package ctp;

import haxe.io.Bytes;
import openfl.display.BitmapData;
import openfl.utils.ByteArray;

/**
 * Core Decoder for CTP (.ctp) texture format.
 * Reads binary payload, validates header, and reconstructs texture buffers.
 */
class CTPDecoder {
    public static const MAGIC_HEADER:String = "CTP1";

    /**
     * Decodes binary CTP bytes into OpenFL BitmapData.
     * @param bytes Raw binary bytes from .ctp file.
     * @return BitmapData ready for Flixel rendering.
     */
    public static function decode(bytes:Bytes):BitmapData {
        if (bytes == null || bytes.length < 16) {
            trace("[CTPDecoder] Error: Invalid or corrupt CTP byte stream.");
            return null;
        }

        var input = new haxe.io.BytesInput(bytes);
        
        // 1. Read Header (16 Bytes)
        var magic = input.readString(4);
        if (magic != MAGIC_HEADER) {
            trace('[CTPDecoder] Error: Invalid Magic Header "${magic}". Expected "${MAGIC_HEADER}".');
            return null;
        }

        var width:Int = input.readInt32();
        var height:Int = input.readInt32();
        var blockSize:Int = input.readInt32();

        trace('[CTPDecoder] Loading CTP Texture (${width}x${height}) with Block Size ${blockSize}x${blockSize}');

        // 2. Read Payload & Reconstruct Buffer
        var compressedPayloadSize = bytes.length - 16;
        var compressedBytes = input.read(compressedPayloadSize);
        
        // Decompress stream (LZ4/ZSTD wrapper)
        var decompressedBytes:Bytes;
        try {
            decompressedBytes = haxe.zip.Uncompress.run(compressedBytes);
        } catch (e:Dynamic) {
            trace("[CTPDecoder] Compression fallback triggered or raw raw stream read.");
            decompressedBytes = compressedBytes;
        }

        // 3. Create OpenFL BitmapData Container
        var bitmap = new BitmapData(width, height, true, 0x00000000);
        var byteArray:ByteArray = ByteArray.fromBytes(decompressedBytes);
        byteArray.position = 0;
        
        bitmap.setPixels(bitmap.rect, byteArray);
        return bitmap;
    }
}
