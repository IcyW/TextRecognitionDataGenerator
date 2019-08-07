import random as rnd

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter

IS_SQUARE = True  # added by Me
is_abnormal = False


def generate(text, font, text_color, font_size, orientation, space_width, fit):
    if orientation == 0:
        return _generate_horizontal_text(text, font, text_color, font_size, space_width, fit)
    elif orientation == 1:
        return _generate_vertical_text(text, font, text_color, font_size, space_width, fit)
    else:
        raise ValueError("Unknown orientation " + str(orientation))


def generate_overlap(text, font, text_color, font_size, orientation, space_width, fit):
    """
        Generate abnormal words
    :param text:
    :param font:
    :param text_color:
    :param font_size:
    :param orientation:
    :param space_width:
    :param fit:
    :return:
    """
    import random
    image_font = ImageFont.truetype(font=font, size=font_size)
    words = text.split(' ')
    mid = int(len(words) / 2)
    words1 = words[0:mid]
    words2 = words[mid:]
    space_width = image_font.getsize(' ')[0] * space_width

    words_width1 = [image_font.getsize(w)[0] for w in words1]
    words_width2 = [image_font.getsize(w)[0] for w in words2]
    text_width1 = sum(words_width1) + int(space_width) * (len(words) - 1)
    text_width2 = sum(words_width2) + int(space_width) * (len(words) - 1)
    text_height = max([image_font.getsize(w)[1] for w in words])

    longer_words, shorter_words = words1, words2
    longer_words_width, shorter_words_width = words_width1, words_width2
    longer_text_width, shorter_text_width = text_width1, text_width2
    if text_width1 < text_width2:
        longer_words, shorter_words = words2, words1
        longer_words_width, shorter_words_width = words_width2, words_width1
        longer_text_width, shorter_text_width = text_width2, text_width1

    # side = max(text_width1, text_width2)
    side = text_width1 + text_width2
    txt_img = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2]))
    )

    y = side / 2
    for i, w in enumerate(longer_words):
        x = sum(longer_words_width[0:i]) + i * int(space_width)
        txt_draw.text((x, y), w, fill=fill, font=image_font)

    w_bias = random.randint(0, side - shorter_text_width)
    if is_abnormal:
        _y = y + random.randint(-text_height + 2, text_height - 2)
        for i, w in enumerate(shorter_words):
            _x = sum(shorter_words_width[0:i]) + w_bias + i * int(space_width)
            txt_draw.text((_x, _y), w, fill=fill, font=image_font)
    else:
        _y = y + random.randint(text_height, text_height * 2)
        for i, w in enumerate(shorter_words):
            _x = sum(shorter_words_width[0:i]) + w_bias + i * int(space_width)
            txt_draw.text((_x, _y), w, fill=fill, font=image_font)

    return txt_img


def _generate_horizontal_text(text, font, text_color, font_size, space_width, fit):
    image_font = ImageFont.truetype(font=font, size=font_size)
    words = text.split(' ')
    space_width = image_font.getsize(' ')[0] * space_width

    words_width = [image_font.getsize(w)[0] for w in words]
    text_width = sum(words_width) + int(space_width) * (len(words) - 1)
    text_height = max([image_font.getsize(w)[1] for w in words])
    print("text_width, text_height:", text_width, text_height)

    if IS_SQUARE:
        txt_img = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
    else:
        txt_img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))

    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2]))
    )

    for i, w in enumerate(words):
        txt_draw.text((sum(words_width[0:i]) + i * int(space_width), 0), w, fill=fill, font=image_font)

    if IS_SQUARE or not fit:
        return txt_img
    else:
        if fit:
            return txt_img.crop(txt_img.getbbox())


def _generate_vertical_text(text, font, text_color, font_size, space_width, fit):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_height = int(image_font.getsize(' ')[1] * space_width)

    char_heights = [image_font.getsize(c)[1] if c != ' ' else space_height for c in text]
    text_width = max([image_font.getsize(c)[0] for c in text])
    text_height = sum(char_heights)

    txt_img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))

    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(c1[0], c2[0]),
        rnd.randint(c1[1], c2[1]),
        rnd.randint(c1[2], c2[2])
    )

    for i, c in enumerate(text):
        txt_draw.text((0, sum(char_heights[0:i])), c, fill=fill, font=image_font)

    if fit:
        return txt_img.crop(txt_img.getbbox())
    else:
        return txt_img
