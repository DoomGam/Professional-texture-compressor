package ctp;

import openfl.display.BitmapData;
import openfl.utils.Assets;
import flixel.graphics.FlxGraphic;
import haxe.io.Bytes;

class CTPGraphic 
{
    private static var _graphicCache:Map<String, FlxGraphic> = new Map<String, FlxGraphic>();

    /**
     * Carrega um arquivo .ctp diretamente para um FlxGraphic pronto para uso em sprites de FNF.
     * @param fileKey Caminho relativo do arquivo .ctp (ex: "assets/images/BOYFRIEND.ctp")
     */
    public static function fromFile(fileKey:String):FlxGraphic 
    {
        if (_graphicCache.exists(fileKey)) 
        {
            var cachedGraphic:FlxGraphic = _graphicCache.get(fileKey);
            if (cachedGraphic != null && cachedGraphic.bitmap != null) 
            {
                return cachedGraphic;
            }
        }

        if (!Assets.exists(fileKey)) 
        {
            trace("[CTPGraphic] Erro: Arquivo CTP não encontrado no caminho: " + fileKey);
            return null;
        }

        var ctpBytes:Bytes = Assets.getBytes(fileKey);
        if (ctpBytes == null) 
        {
            trace("[CTPGraphic] Erro: Falha ao ler os bytes do arquivo: " + fileKey);
            return null;
        }

        var bitmap:BitmapData = CTPDecoder.decode(ctpBytes);
        if (bitmap == null) 
        {
            trace("[CTPGraphic] Erro: Falha na decodificação do bitmap para: " + fileKey);
            return null;
        }

        var graphic:FlxGraphic = FlxGraphic.fromBitmapData(bitmap, false, fileKey);
        graphic.persist = true;
        _graphicCache.set(fileKey, graphic);

        return graphic;
    }

    /**
     * Limpa a memória RAM/GPU liberando o cache de gráficos CTP não utilizados.
     */
    public static function clearCache():Void 
    {
        for (key in _graphicCache.keys()) 
        {
            var graphic:FlxGraphic = _graphicCache.get(key);
            if (graphic != null) 
            {
                graphic.destroy();
            }
        }
        _graphicCache.clear();
        trace("[CTPGraphic] Cache de texturas CTP limpo com sucesso.");
    }
}
