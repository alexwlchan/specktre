# -*- encoding: utf-8

from specktre.cli import Settings
from specktre.colors import RGBColor
from specktre.specktre import draw_speckled_wallpaper
from specktre.tilings import generate_triangles


def test_draw_speckled_wallpaper():
    s = Settings(
        generator=generate_triangles,
        width=200,
        height=300,
        start_color=RGBColor(0, 0, 256),
        end_color=RGBColor(0, 0, 0),
        name="output.jpg"
    )

    im = draw_speckled_wallpaper(s)
    assert im.size == (200, 300)
