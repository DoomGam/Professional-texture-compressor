package ctp;

import haxe.io.Bytes;
import openfl.display.BitmapData;
import openfl.utils.ByteArray;

class CTPDecoder 
{
    private static inline var MAGIC_HEADER:String = "CTP2";
    private static inline var HEADER_SIZE:Int = 20;

    /**
     * Decodifica um arquivo binário .ctp (Header v2) diretamente para BitmapData
     */
    public static function decode(bytes:Bytes):BitmapData 
    {
        if (bytes == null || bytes.length < HEADER_SIZE) 
        {
            trace("[CTPDecoder] Erro: Dados binários inválidos ou corrompidos.");
            return null;
        }

        var magic:String = bytes.getString(0, 4);
        if (magic != MAGIC_HEADER) 
        {
            trace("[CTPDecoder] Erro: Assinatura de cabeçalho incompatível. Esperado CTP2, recebido: " + magic);
            return null;
        }

        var width:Int = bytes.getInt32(4);
        var height:Int = bytes.getInt32(8);
        var blockSize:Int = bytes.getInt32(12);
        var compressionMode:Int = bytes.get(16);

        var compressedPayload:Bytes = bytes.sub(HEADER_SIZE, bytes.length - HEADER_SIZE);

        var decompressedBytes:Bytes;
        try 
        {
            decompressedBytes = format.tools.Deflate.decompress(compressedPayload);
        } 
        catch (e:Dynamic) 
        {
            var byteArray:ByteArray = ByteArray.fromBytes(compressedPayload);
            byteArray.uncompress();
            decompressedBytes = byteArray.toBytes();
        }

        var bitmap:BitmapData = new BitmapData(width, height, true, 0x00000000);
        var pixelData:ByteArray = ByteArray.fromBytes(decompressedBytes);
        pixelData.position = 0;
        
        bitmap.setPixels(bitmap.rect, pixelData);

        return bitmap;
    }
}
