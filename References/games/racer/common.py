import datetime
import math
import random
from dataclasses import dataclass

from PyQt5 import QtGui
from easygraphics import Image

from easygraphics import *



class UtilObject:
    pass


@dataclass
class Screen:
    x: int
    y: int
    w: int
    h: int


@dataclass
class Camera:
    x: int
    y: int
    z: int


@dataclass
class World:
    x: int
    y: int
    z: int


@dataclass
class Projection:
    camera: Camera
    screen: Screen
    world: World


@dataclass()
class ColorObject:
    road: str
    grass: str
    rumble: str
    lane: str



@dataclass()
class Rectangle:
    x: int
    y: int
    w: int
    h: int


class Util:
    @staticmethod
    def increase(start, increment, max):
        result = start + increment
        while result > max:
            result -= max
        while result < 0:
            result += max
        return result

    @staticmethod
    def accelerate(velocity, accel, dt):
        return velocity + (accel * dt)

    @staticmethod
    def limit(value, _min, _max):
        return max(_min, min(value, _max))

    @staticmethod
    def timestamp():
        return datetime.datetime.now()

    @staticmethod
    def percent_remaining(n, total):
        return (n % total) / total

    @staticmethod
    def interpolate(a, b, percent):
        return a + (b - a) * percent

    @staticmethod
    def ease_in(a, b, percent):
        return a + (b - a) * math.pow(percent, 2)

    @staticmethod
    def ease_out(a, b, percent):
        return a + (b - a) * (1 - math.pow(percent, 2))

    @staticmethod
    def ease_in_out(a, b, percent):
        return a + (b - a) * ((-math.cos(percent * math.pi) / 2) + 0.5)

    @staticmethod
    def exponential_fog(distance, density):
        return 1 / (math.pow(math.e, distance * distance * density))

    @staticmethod
    def project(p: Projection, camera_x, camera_y, camera_z, camera_depth, width, height, road_width):
        p.camera.x = p.world.x - camera_x
        p.camera.y = p.world.y - camera_y
        p.camera.z = p.world.z - camera_z
        if p.camera.z <= camera_depth:
            return

        p.screen.scale = camera_depth / p.camera.z
        p.screen.x = (width / 2) + (p.screen.scale * p.camera.x * width / 2)
        p.screen.y = (height / 2) - (p.screen.scale * p.camera.y * height / 2)
        p.screen.w = (p.screen.scale * road_width * width / 2)

    @staticmethod
    def overlap(x1, w1, x2, w2, percent=1):
        half = percent / 2
        min1 = x1 - (w1 * half)
        max1 = x1 + (w1 * half)
        min2 = x2 - (w2 * half)
        max2 = x2 + (w2 * half)
        return not ((max1 < min2) or (min1 > max2));


class Render:
    @staticmethod
    def background(background: Image, width, height, layer: Rectangle, offset_x=0, offset_y=0):
        """
        绘制背景

        :param background:
        :param width:
        :param height:
        :param layer:
        :param offset_x:
        :param offset_y:
        """
        # 为了产生转动的效果，背景图片在横向上放大两倍显示
        image_w = layer.w // 2
        image_h = layer.h

        source_x = layer.x + int(math.floor(layer.w * offset_x))
        source_y = layer.y
        source_w = min(image_w, layer.x + layer.w - source_x)
        source_h = image_h

        dest_x = 0
        dest_y = offset_y
        dest_w = width * source_w // image_w
        dest_h = height
        draw_image(dest_x, dest_y, background, width=dest_w, height=dest_h, src_x=source_x, src_y=source_y,
                   src_width=source_w, src_height=source_h)
        if source_w < image_w:  # 由于水平方向上的位移，导致只显示了一部分背景，补全剩下的部分
            draw_image(dest_w - 1, dest_y, background, width=width - dest_w, height=dest_h, src_x=layer.x,
                       src_y=source_y, src_width=image_w - source_w, src_height=source_h)

    @staticmethod
    def sprite(width, height, resolution, road_width, sprites: Image, sprite: Rectangle, scale, dest_x, dest_y,
               offset_x=0, offset_y=0, clip_y=0):
        """
        绘制spirite
        :param width:
        :param height:
        :param resolution:
        :param road_width:
        :param sprites:
        :param sprite:
        :param scale:
        :param dest_x:
        :param dest_y:
        :param offset_x:
        :param offset_y:
        :param clip_y:
        """
        # scale for projection and relative to road_width (for tweakUI)
        dest_w = (sprite.w * scale * width / 2) * (SPRITES.SCALE * road_width)
        dest_h = (sprite.h * scale * width / 2) * (SPRITES.SCALE * road_width)

        dest_x = dest_x + (dest_w * offset_x)
        dest_y = dest_y + (dest_h * offset_y)

        clip_h = max(0, dest_y + dest_h - clip_y) if clip_y != 0 else 0
        if clip_h < dest_h:
            draw_image(dest_x, dest_y, sprites, width=dest_w, height=dest_h - clip_h, src_x=sprite.x, src_y=sprite.y,
                       src_width=sprite.w, src_height=sprite.h)

    @staticmethod
    def player(width, height, resolution, road_width, sprites, speed_percent, scale, dest_x, dest_y, steer, updown):
        bounce = (1.5 * random.random() * speed_percent * resolution) * random.choice((-1, 1))
        if steer < 0:
            sprite = SPRITES.PLAYER_UPHILL_LEFT if updown > 0 else SPRITES.PLAYER_LEFT
        elif steer < 0:
            sprite = SPRITES.PLAYER_UPHILL_RIGHT if updown < 0 else SPRITES.PLAYER_RIGHT
        else:
            sprite = SPRITES.PLAYER_UPHILL_STRAIGHT if updown < 0 else SPRITES.PLAYER_STRAIGHT

        Render.sprite(width, height, resolution, road_width, sprites, sprite, scale, dest_x, dest_y + bounce, -0.5, -1)

    @staticmethod
    def rumble_width(projected_road_width, lanes):
        return projected_road_width / max(6, 2 * lanes)

    @staticmethod
    def lane_marker_width(projected_road_width, lanes):
        return projected_road_width / max(32, 8 * lanes)

    @staticmethod
    def segment(width, lanes, x1, y1, w1, x2, y2, w2, color: ColorObject):
        r1 = Render.rumble_width(w1, lanes)
        r2 = Render.rumble_width(w2, lanes)
        l1 = Render.lane_marker_width(w1, lanes)
        l2 = Render.lane_marker_width(w2, lanes)
        set_fill_color(color.grass)
        draw_rect(0, y1, width, y2)  # ??

        set_fill_color(color.rumble)
        draw_polygon(x1 - w1 - r1, y1, x1 - w1, y1, x2 - w2, y2, x2 - w2 - r2, y2)
        draw_polygon(x1 + w1 + r1, y1, x1 + w1, y1, x2 + w2, y2, x2 + w2 + r2, y2)
        set_fill_color(color.road)
        draw_polygon(x1 - w1, y1, x1 + w1, y1, x2 + w2, y2, x2 - w2, y2)

        if color.lane is not None:
            lane_w1 = w1 * 2 / lanes
            lane_w2 = w2 * 2 / lanes
            lane_x1 = x1 - w1 + lane_w1
            lane_x2 = x2 - w2 + lane_w2
            set_fill_color(color.lane)
            for lane in range(1, lanes):
                draw_polygon(lane_x1 - l1 / 2, y1, lane_x1 + l1 / 2, y1,
                               lane_x2 + l2 / 2, y2, lane_x2 - l2 / 2, y2)
                lane_x1 += lane_w1
                lane_x2 += lane_w2


class Game:
    @staticmethod
    def load_images(names):
        results = []
        for name in names:
            image = create_image_from_file(f"images/{name}.png")
            results.append(image)
        return results


COLORS = UtilObject()
COLORS.SKY = '#72D7EE'
COLORS.TREE = '#005108'
COLORS.FOG = '#005108'
COLORS.LIGHT = ColorObject('#6B6B6B', '#10AA10', '#555555', '#CCCCCC')
COLORS.DARK = ColorObject('#696969', '#009A00', '#BBBBBB', None)
COLORS.START = ColorObject('white', 'white', 'white', None)
COLORS.FINISH = ColorObject('black', 'black', 'black', None)

BACKGROUND = UtilObject()
BACKGROUND.HILLS = Rectangle(x=5, y=5, w=1280, h=480)
BACKGROUND.SKY = Rectangle(x=5, y=495, w=1280, h=480)
BACKGROUND.TREES = Rectangle(x=5, y=985, w=1280, h=480)

SPRITES = UtilObject()
SPRITES.PALM_TREE = Rectangle(x=5, y=5, w=215, h=540)
SPRITES.BILLBOARD08 = Rectangle(x=230, y=5, w=385, h=265)
SPRITES.TREE1 = Rectangle(x=625, y=5, w=360, h=360)
SPRITES.DEAD_TREE1 = Rectangle(x=5, y=555, w=135, h=332)
SPRITES.BILLBOARD09 = Rectangle(x=150, y=555, w=328, h=282)
SPRITES.BOULDER3 = Rectangle(x=230, y=280, w=320, h=220)
SPRITES.COLUMN = Rectangle(x=995, y=5, w=200, h=315)
SPRITES.BILLBOARD01 = Rectangle(x=625, y=375, w=300, h=170)
SPRITES.BILLBOARD06 = Rectangle(x=488, y=555, w=298, h=190)
SPRITES.BILLBOARD05 = Rectangle(x=5, y=897, w=298, h=190)
SPRITES.BILLBOARD07 = Rectangle(x=313, y=897, w=298, h=190)
SPRITES.BOULDER2 = Rectangle(x=621, y=897, w=298, h=140)
SPRITES.TREE2 = Rectangle(x=1205, y=5, w=282, h=295)
SPRITES.BILLBOARD04 = Rectangle(x=1205, y=310, w=268, h=170)
SPRITES.DEAD_TREE2 = Rectangle(x=1205, y=490, w=150, h=260)
SPRITES.BOULDER1 = Rectangle(x=1205, y=760, w=168, h=248)
SPRITES.BUSH1 = Rectangle(x=5, y=1097, w=240, h=155)
SPRITES.CACTUS = Rectangle(x=929, y=897, w=235, h=118)
SPRITES.BUSH2 = Rectangle(x=255, y=1097, w=232, h=152)
SPRITES.BILLBOARD03 = Rectangle(x=5, y=1262, w=230, h=220)
SPRITES.BILLBOARD02 = Rectangle(x=245, y=1262, w=215, h=220)
SPRITES.STUMP = Rectangle(x=995, y=330, w=195, h=140)
SPRITES.SEMI = Rectangle(x=1365, y=490, w=122, h=144)
SPRITES.TRUCK = Rectangle(x=1365, y=644, w=100, h=78)
SPRITES.CAR03 = Rectangle(x=1383, y=760, w=88, h=55)
SPRITES.CAR02 = Rectangle(x=1383, y=825, w=80, h=59)
SPRITES.CAR04 = Rectangle(x=1383, y=894, w=80, h=57)
SPRITES.CAR01 = Rectangle(x=1205, y=1018, w=80, h=56)
SPRITES.PLAYER_UPHILL_LEFT = Rectangle(x=1383, y=961, w=80, h=45)
SPRITES.PLAYER_UPHILL_STRAIGHT = Rectangle(x=1295, y=1018, w=80, h=45)
SPRITES.PLAYER_UPHILL_RIGHT = Rectangle(x=1385, y=1018, w=80, h=45)
SPRITES.PLAYER_LEFT = Rectangle(x=995, y=480, w=80, h=41)
SPRITES.PLAYER_STRAIGHT = Rectangle(x=1085, y=480, w=80, h=41)
SPRITES.PLAYER_RIGHT = Rectangle(x=995, y=531, w=80, h=41)

SPRITES.SCALE = 0.3 * (1 / SPRITES.PLAYER_STRAIGHT.w)  # the reference sprite width should be 1/3rd the (half-)roadWidth

SPRITES.BILLBOARDS = [SPRITES.BILLBOARD01, SPRITES.BILLBOARD02, SPRITES.BILLBOARD03, SPRITES.BILLBOARD04,
                      SPRITES.BILLBOARD05, SPRITES.BILLBOARD06, SPRITES.BILLBOARD07, SPRITES.BILLBOARD08,
                      SPRITES.BILLBOARD09]
SPRITES.PLANTS = [SPRITES.TREE1, SPRITES.TREE2, SPRITES.DEAD_TREE1, SPRITES.DEAD_TREE2, SPRITES.PALM_TREE,
                  SPRITES.BUSH1, SPRITES.BUSH2, SPRITES.CACTUS, SPRITES.STUMP, SPRITES.BOULDER1, SPRITES.BOULDER2,
                  SPRITES.BOULDER3]
SPRITES.CARS = [SPRITES.CAR01, SPRITES.CAR02, SPRITES.CAR03, SPRITES.CAR04, SPRITES.SEMI, SPRITES.TRUCK]
