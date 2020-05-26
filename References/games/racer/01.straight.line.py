"""
https:#codeincomplete.com/articles/javascript-racer-v1-straight/
https:#github.com/jakesgordon/javascript-racer/
"""
import time
from typing import List

from PyQt5 import QtCore
from easygraphics import *
from common import *

@dataclass()
class Segment:
    index: int
    p1: Projection
    p2: Projection
    color: ColorObject
    looped:bool = False

fps = 60  # how many 'update' frames per second
step = 1 / fps  # how long is each frame (in seconds)
width = 1024  # logical canvas width
height = 768  # logical canvas height
num_segments = 500 # number of road segments
segments: List[Segment] = []  # list of road segments
# stats         = Game.stats('fps')       # mr.doobs FPS counter

background = None  # our background image (loaded below)
sprites = None  # our spritesheet (loaded below)
resolution = height/ 480  # scaling factor to provide resolution independence (computed)
road_width = 2000  # actually half the roads width, easier math if the road spans from -roadWidth to +roadWidth
segment_length = 200  # length of a single segment
rumble_length = 3  # number of segments per red/white rumble strip
track_length = None  # z length of entire track (computed)
lanes = 3  # number of lanes
field_of_view = 100  # angle (degrees) for field of view
camera_height = 1000  # z height of camera
camera_depth = 1/math.tan((field_of_view/2)*math.pi/180)  # z distance camera is from screen (computed)
draw_distance = 300  # number of segments to draw
player_x = 0  # player x offset from center of road (-1 to 1 to stay independent of roadWidth)
player_z = camera_depth*camera_height # player relative z distance from camera (computed)
fogDensity = 5  # exponential fog density
position = 0  # current camera Z position (add playerZ to get player's absolute Z position)
speed = 0  # current speed
max_speed = segment_length / step  # top speed (ensure we can't move more than 1 segment in a single frame to make collision detection easier)
accel = max_speed / 5  # acceleration rate - tuned until it 'felt' right
breaking = -max_speed  # deceleration rate when braking
decel = -max_speed / 5  # 'natural' deceleration rate when neither accelerating, nor braking
off_road_decel = -max_speed / 2  # off road deceleration is somewhere in between
off_road_limit = max_speed / 4  # limit when off road deceleration no longer applies (e.g. you can always go at least this speed even when off road)
key_left = False
key_right = False
key_faster = False
key_slower = False

def find_segments(z:float)->Segment:
    # print(z,segment_length,len(segments))
    return segments[ round(z / segment_length) % len(segments)]

def reset_road():
    global track_length
    segments.clear()
    for n in range(num_segments):
        segments.append(Segment(
            index=n,
            p1=Projection(world = World(0,0,n*segment_length),camera=Camera(0,0,0),screen=Screen(0,0,0,0)),
            p2=Projection(world = World(0,0,(n+1)*segment_length),camera=Camera(0,0,0),screen=Screen(0,0,0,0)),
            color= COLORS.DARK if round(n // rumble_length) %2!=0 else COLORS.LIGHT
        ))
    segments[find_segments(player_z).index+2].color = COLORS.START
    segments[find_segments(player_z).index+3].color  = COLORS.START
    for n in range(rumble_length):
        segments[len(segments)-1-n].color = COLORS.FINISH
    track_length = len(segments)*segment_length



def update(dt):
    """
    Update the game world
    :param dt: time delta
    """
    global position, player_x, speed
    position = Util.increase(position, dt * speed, track_length)

    dx = dt * 2 * (speed / max_speed)  # at top speed, should be able to cross from left to right (-1 to 1) in 1 second

    if key_left:
        player_x -= dx
    elif key_right:
        player_x += dx

    if key_faster:
        speed = Util.accelerate(speed, accel, dt)
    elif key_slower:
        speed = Util.accelerate(speed, decel, dt)

    if ((player_x < -1) or (player_x > 1)) and (speed > off_road_limit):
        speed = Util.accelerate(speed, off_road_decel, dt)

    player_x = Util.limit(player_x, -2, 2)  # dont ever let player go too far out of bounds
    speed = Util.limit(speed, 0, max_speed)  # or exceed maxSpeed

def render():
    base_segment = find_segments(position)
    max_y = height

    clear_device()

    Render.background(background,width,height,BACKGROUND.SKY)
    Render.background(background, width, height, BACKGROUND.HILLS)
    Render.background(background, width, height, BACKGROUND.TREES)

    for n in range(draw_distance):
        segment = segments[(base_segment.index+n)%len(segments)]
        segment.looped = segment.index < base_segment.index

        pos = position - (track_length if segment.looped else 0)
        Util.project(segment.p1, (player_x * road_width), camera_height, pos, camera_depth, width, height, road_width)
        Util.project(segment.p2, (player_x * road_width), camera_height, pos, camera_depth, width, height, road_width)

        if (segment.p1.camera.z <= camera_depth) \
                or (segment.p2.screen.y>max_y): # behind us or clip by (already rendered) segment
            continue

        Render.segment(width,lanes,
                       segment.p1.screen.x,
                       segment.p1.screen.y,
                       segment.p1.screen.w,
                       segment.p2.screen.x,
                       segment.p2.screen.y,
                       segment.p2.screen.w,
                       segment.color)
        max_y = segment.p2.screen.y

    if key_left :
        steer = -1
    elif key_right:
        steer = 1
    else:
        steer = 0
    Render.player(width,height,resolution,road_width,sprites,speed/max_speed,
                  camera_depth/player_z, width/2,height,
                  steer,0)




def main():
    global background,sprites
    global key_left,key_right,key_faster,key_slower
    init_graph(width,height)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_antialiasing(False)
    background,sprites = Game.load_images(["background","sprites"])
    set_line_style(LineStyle.NO_PEN)
    reset_road()
    last_time = time.time()
    while is_run():
        if delay_jfps(30):
            key_left=key_right=key_faster=key_slower = False
            while has_kb_msg():
                key_message = get_key()
                if key_message.key == QtCore.Qt.Key_Up:
                    key_faster = ( key_message.type == QtCore.QEvent.KeyPress )
                elif key_message.key == QtCore.Qt.Key_Down:
                    key_slower = ( key_message.type == QtCore.QEvent.KeyPress )
                elif key_message.key == QtCore.Qt.Key_Left:
                    key_left = ( key_message.type == QtCore.QEvent.KeyPress )
                elif key_message.key == QtCore.Qt.Key_Right:
                    key_right = ( key_message.type == QtCore.QEvent.KeyPress )
            now = time.time()

            update(now-last_time)
            render()
            last_time = now

easy_run(main)
