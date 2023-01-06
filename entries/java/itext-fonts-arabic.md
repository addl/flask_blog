

BaseFont bf = BaseFont.createFont("/fonts/arial.ttf", BaseFont.IDENTITY_H,
          BaseFont.NOT_EMBEDDED);
      Font font = new Font(bf, 24, Font.NORMAL);
	  
	  
	  public class PrintFontProvider extends FontFactoryImp {

    @Override
    public Font getFont(String fontName, String encoding, boolean embedded, float size, int style, BaseColor color, boolean cached) {

        // LiberationSans – http://de.wikipedia.org/wiki/Liberation_(Schriftart) – http://scripts.sil.org/cms/scripts/page.php?item_id=OFL_web
        if (style == Font.NORMAL)     return new Font(this.load("fonts/Liberation/LiberationSans-Regular.ttf"),    size, Font.NORMAL, color);
        if (style == Font.BOLD)       return new Font(this.load("fonts/Liberation/LiberationSans-Bold.ttf"),       size, Font.NORMAL, color);
        if (style == Font.BOLDITALIC) return new Font(this.load("fonts/Liberation/LiberationSans-BoldItalic.ttf"), size, Font.NORMAL, color);
        if (style == Font.ITALIC)     return new Font(this.load("fonts/Liberation/LiberationSans-Italic.ttf"),     size, Font.NORMAL, color);
        return new Font(this.load("fonts/Liberation/LiberationSans-Regular.ttf"), size, style, color);
    }

    private BaseFont load(String path) { ... }
}