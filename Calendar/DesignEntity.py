from PIL import Image, ImageOps, ImageDraw

class DesignEntity (object):
    """General entity that can be drawn on to a panel design or
    other design entities."""
    def __init__ (self, size, mask=False):
        self.size = size
        self.pos = (0, 0)
        self.mask = mask
        self.__init_image__()
        self.__finished_image__ = False

    def __init_image__ (self, color = 'white'):
        self.__image__ = Image.new('RGB', self.size, color=color)

    def get_image (self):
        if self.__finished_image__ is False:
            self.__finish_image__()
            self.__finished_image__ = True
        return self.__image__

    def draw (self, subimage, pos, mask=False):
        img_mask = None
        if mask:
            img_mask = ImageOps.invert(subimage.convert('L'))
        self.__image__.paste(subimage, pos, mask=img_mask)

    def draw_design (self, entity):
        self.draw(entity.get_image(), entity.pos, entity.mask)

    def draw_image (self, path, pos):
        self.draw(Image.open(path), pos)

    def __finish_image__ (self):
        pass