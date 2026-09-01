package ctp;

import haxe.io.Bytes;
import openfl.display.BitmapData;
import openfl.utils.ByteArray;

class CTPDecoder 
{
    /**
     * Decodifica a stream de bytes CTP2 para BitmapData de forma segura para Android e iOS.
     */
    public static function decode(bytes:Bytes):BitmapData 
    {
        if (bytes == null || bytes.length < 20) 
        {
            trace('[CTP Error] Arquivo CTP nulo ou truncado (menos de 20 bytes).');
            return null;
        }

        try 
        {
            var magic:String = bytes.getString(0, 4);
            if (magic != "CTP2") 
            {
                trace('[CTP Error] Assinatura inválida! Esperado CTP2, recebido: ' + magic);
                return null;
            }

            var origWidth:Int = bytes.getInt32(4);
            var origHeight:Int = bytes.getInt32(8);
            var padWidth:Int = bytes.getInt32(12);
            var padHeight:Int = bytes.getInt32(16);

            if (origWidth <= 0 || origHeight <= 0 || padWidth <= 0 || padHeight <= 0) 
            {
                trace('[CTP Error] Dimensões inválidas no cabeçalho: ' + origWidth + 'x' + origHeight);
                return null;
            }

            var compressedData:Bytes = bytes.sub(20, bytes.length - 20);
            var decompressedBytes:Bytes = haxe.zip.Uncompress.run(compressedData);

            if (decompressedBytes == null || decompressedBytes.length == 0) 
            {
                trace('[CTP Error] Falha na descompactação zlib.');
                return null;
            }

            var byteArray:ByteArray = ByteArray.fromBytes(decompressedBytes);
            byteArray.position = 0;

            var bitmap:BitmapData = new BitmapData(padWidth, padHeight, true, 0x00000000);
            bitmap.setPixels(bitmap.rect, byteArray);

            return bitmap;
        } 
        catch (e:Dynamic) 
        {
            trace('[CTP Critical Error] Exceção capturada na decodificação: ' + e);
            return null;
        }
    }
}
