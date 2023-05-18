FONT_DIR = "asset/font/"
IMAGES_DIR = "asset/images/"
BACKGROUND_COLOR = {"r": 209, "g": 223, "b": 232}
FONT_COLOR = {"r": 0, "g": 0, "b": 0}


def paintEntity(monitor, entity, x, y):
    monitor.blit(entity, (int(x), int(y)))
