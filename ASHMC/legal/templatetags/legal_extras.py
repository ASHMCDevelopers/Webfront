from django.template import Library, TemplateSyntaxError

from ..models import OfficialForm

import datetime
import xlrd

register = Library()


class RomanError(Exception):
    pass


class OutOfRangeError(RomanError):
    pass


class NotIntegerError(RomanError):
    pass

ROMAN_NUMBER_MAP = (('M',  1000),
                    ('CM', 900),
                    ('D',  500),
                    ('CD', 400),
                    ('C',  100),
                    ('XC', 90),
                    ('L',  50),
                    ('XL', 40),
                    ('X',  10),
                    ('IX', 9),
                    ('V',  5),
                    ('IV', 4),
                    ('I',  1))


def to_roman(n):
    """convert integer to Roman numeral"""
    if not isinstance(n, int):
        try:
            n = int(n)
        except ValueError:
            raise NotIntegerError("non-integers cannot be converted")

    if not (0 < n < 4000):
        raise OutOfRangeError("number out of range (must be 1..3999)")

    result = ""
    for numeral, integer in ROMAN_NUMBER_MAP:
        while n >= integer:
            result += numeral
            n -= integer
    return result


def roman_number(value):
    """
    Converts a number to its roman value

    Example usage::
        {{ 2007|roman_number }}
        {{ "2007"|roman_number }}
        {{ pub_date|date:"Y"|roman_number }}
    """
    try:
        value = to_roman(value)
    except RomanError, e:
        raise TemplateSyntaxError("roman_number error: %s" % str(e))
    return value

register.filter('roman_number', roman_number)


@register.simple_tag
def get_file_form_url(file_form_name):
    return OfficialForm.objects.get(name=file_form_name).file_actual.url


@register.filter
def row_generator(sheet):
    for rown in xrange(sheet.nrows):
        yield sheet.row(rown)


@register.filter
def get_value_display(cell, format_map=None):
    if cell.ctype in [0, 1, 2]:
        return cell.value
    elif cell.ctype == 3:
        date = datetime.datetime(*xlrd.xldate_as_tuple(cell.value, 0))
        return date.strftime("%m/%d/%Y")
    elif cell.ctype == 4:
        return bool(cell.value)
    elif cell.ctype == 5:
        return "ERROR"
    elif cell.ctype == 6:
        return ""


@register.filter
def get_styles(cell, wb):
    styles = []
    format = wb.xf_list[cell.xf_index]
    font = wb.font_list[format.font_index]

    cmap = wb.colour_map

    # Background color
    background_ctuple = cmap[format.background.pattern_colour_index]
    if background_ctuple:
        styles += ['background-color: rgb{}'.format(background_ctuple)]

    # Text alignment
    TEXT_ALIGN_MAP = {
        0: 'left',
        1: 'left',
        2: 'center',
        3: 'right',
    }
    styles += ['text-align: {}'.format(TEXT_ALIGN_MAP[format.alignment.hor_align])]

    # Font styles
    colour_tuple = cmap[font.colour_index]
    if colour_tuple:
        styles += ['color: rgb{}'.format(colour_tuple)]
    if font.name:
        styles += ['font-family: "{}"'.format(font.name)]
    if font.bold:
        styles += ['font-weight: 700']
    if font.italic:
        styles += ['font-style: italic']
    if font.underlined:
        styles += ['text-decoration: underline']
    if font.struck_out:
        styles += ['text-decoration: line-through']

    # Border styles
    border_string = "border-{}: 1px {} {}"

    BORDER_STYLE_MAP = {
        0: 'solid',
        1: 'solid',
    }

    if format.border.bottom_line_style:
        color = cmap[format.border.bottom_colour_index]
        styles += [border_string.format(
            'bottom',
            BORDER_STYLE_MAP[format.border.bottom_line_style],
            color or 'black',
        )]
    if format.border.top_line_style:
        color = cmap[format.border.top_colour_index]
        styles += [border_string.format(
            'top',
            BORDER_STYLE_MAP[format.border.top_line_style],
            color or 'black',
        )]
    if format.border.left_line_style:
        color = cmap[format.border.left_colour_index]
        styles += [border_string.format(
            'left',
            BORDER_STYLE_MAP[format.border.left_line_style],
            color or 'black',
        )]
    if format.border.right_line_style:
        color = cmap[format.border.right_colour_index]
        styles += [border_string.format(
            'right',
            BORDER_STYLE_MAP[format.border.right_line_style],
            color or 'black',
        )]

    return '; '.join(styles)
