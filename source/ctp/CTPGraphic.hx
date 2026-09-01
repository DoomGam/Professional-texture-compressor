package ctp;

import flixel.graphics.FlxGraphic;
import openfl.display.BitmapData;
import openfl.utils.Assets;
import haxe.io.Bytes;

/**
 * High-level HaxeFlixel integration helper for CTP textures.
 */
class CTPGraphic {
    /**
     * Loads a .ctp texture asset directly as a FlxGraphic instance.
     * @param path Path to the .ctp asset file.
     * @return FlxGraphic instance cached and ready for FNF Sprites.
     */
    public static function fromAsset(path:String):FlxGraphic {
        if (!Assets.exists(path)) {
            trace('[CTPGraphic] Error: Asset path "${path}" does not exist.');
            return null;
        }

        var bytes:Bytes = Assets.getBytes(path);
        var bitmapData:BitmapData = CTPDecoder.decode(bytes);

        if (bitmapData == null) return null;

        var graphic:FlxGraphic = FlxGraphic.fromBitmapData(bitmapData, false, path);
        graphic.persist = true; // Retain in memory cache like standard FNF assets
        return graphic;
    }
}
