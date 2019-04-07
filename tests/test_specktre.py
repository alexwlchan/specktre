# -*- encoding: utf-8

import os

from PIL import Image

from specktre.cli import Settings
from specktre.colors import RGBColor
from specktre.specktre import draw_speckled_wallpaper, save_speckled_wallpaper
from specktre.tilings import generate_hexagons, generate_triangles


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


def test_save_speckled_wallpaper(tmpdir):
    name = tmpdir / "output.jpg"
    s = Settings(
        generator=generate_hexagons,
        width=200,
        height=300,
        start_color=RGBColor(0, 0, 256),
        end_color=RGBColor(0, 0, 0),
        name=str(name)
    )

    save_speckled_wallpaper(s)
    assert name.exists()
    im = Image.open(name)
    assert im.size == (200, 300)


def test_save_speckled_wallpaper_generates_name(tmpdir):
    os.chdir(str(tmpdir))
    s = Settings(
        generator=generate_hexagons,
        width=200,
        height=300,
        start_color=RGBColor(0, 0, 256),
        end_color=RGBColor(0, 0, 0),
        name=None
    )

    assert tmpdir.listdir() == []
    save_speckled_wallpaper(s)

    assert len(tmpdir.listdir()) == 1
    name = tmpdir.listdir()[0]
    im = Image.open(name)
    assert im.size == (200, 300)
