General Notes:

Items seperated by | means you must choose one of them in an input line.
Items enclosed in [] are optional.

For example, rotate is specified as:
rotate x|y|z degress [knob]

The following would be valid rotations:
rotate x 20
rotate y 23 k1

While the following would be invalid:
rotate x|y 20
rotate x y 33
rotate x 33 [k1]



Stack Commands
--------------
push
pop

Transformations
---------------
move x y z [knob]
scale x y z [knob]
rotate x|y|z degrees [knob]

Image creation
--------------
sphere [constants] x y z r [coord_system]
torus [constants] x y z r0 r1  [coord_system]
box [constants] x0 y0 z0 h w d [coord_system]
line [constants] x0 y0 z0 [coord_system0] x1 y1 z1 [coord_system1]
mesh [constants] :filename [coord_system]

Knobs/Animation
---------------
basename name
set knobname value
save_knobs knoblist
tween start_frame end_frame knoblist0 knoblist1
frames num_frames
vary knob start_frame end_frame start_val end_val
setknobs value

Lighting
--------
light r g b x y z
ambient r g b
constants name kar kdr ksr kag kdg ksg kab kdb ksb [r] [g] [b]
shading wireframe|flat|gouraud|phong|raytrace

MISC
----
//			- comment
save_coord_system name
camera eyex eyey eyez aimx aimy aimz
save filename
gereate_rayfiles
focal value
display
