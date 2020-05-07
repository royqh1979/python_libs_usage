"""
https:#codeincomplete.com/articles/javascript-racer-v1-straight/
https:#github.com/jakesgordon/javascript-racer/
"""


from easygraphics import *
fps           = 60                      # how many 'update' frames per second
step          = 1/fps                   # how long is each frame (in seconds)
width         = 1024                    # logical canvas width
height        = 768                     # logical canvas height
segments      = []                      # array of road segments
# stats         = Game.stats('fps')       # mr.doobs FPS counter

background    = None                    # our background image (loaded below)
sprites       = None                    # our spritesheet (loaded below)
resolution    = None                    # scaling factor to provide resolution independence (computed)
road_with     = 2000                    # actually half the roads width, easier math if the road spans from -roadWidth to +roadWidth
segment_length = 200                     # length of a single segment
rumble_length  = 3                       # number of segments per red/white rumble strip
track_length   = None                    # z length of entire track (computed)
lanes         = 3                       # number of lanes
field_of_view   = 100                     # angle (degrees) for field of view
camera_height  = 1000                    # z height of camera
camera_depth   = None                    # z distance camera is from screen (computed)
draw_distance  = 300                     # number of segments to draw
player_x       = 0                       # player x offset from center of road (-1 to 1 to stay independent of roadWidth)
player_z       = None                    # player relative z distance from camera (computed)
fogDensity    = 5                       # exponential fog density
position      = 0                       # current camera Z position (add playerZ to get player's absolute Z position)
speed         = 0                       # current speed
max_speed      = segment_length / step      # top speed (ensure we can't move more than 1 segment in a single frame to make collision detection easier)
accel         = max_speed / 5             # acceleration rate - tuned until it 'felt' right
breaking      = -max_speed               # deceleration rate when braking
decel         = -max_speed / 5             # 'natural' deceleration rate when neither accelerating, nor braking
off_road_decel  = -max_speed / 2             # off road deceleration is somewhere in between
of_road_limit  = max_speed / 4             # limit when off road deceleration no longer applies (e.g. you can always go at least this speed even when off road)
key_left       = False
key_right      = False
key_faster     = False
key_slower     = False

def main():
    
    pass

easy_run(main)