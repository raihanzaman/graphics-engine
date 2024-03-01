import mdl
import os
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1]
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    step_3d = 20
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    basename = None
    framecount = 1
    shading = 'flat'
    
    #PASS 0
    for command in commands:
        print(command)
        c = command['op']
        args = command['args']

        if c == 'basename':
            basename = args[0]
        if c == 'frames':
            framecount = int(args[0])
            if 'basename' not in [command['op'] for command in commands]:
                print("No basename detected. Using basename 'goat'.")
                commands.append({'op' : 'basename', 'args' : ['goat']})
        if c == 'vary':
            if 'frames' not in [command['op'] for command in commands]:
                print("Compiler Error: frames not found.")
                return
        if c == 'shading':
                shading = command['shade_type']
        if c == 'ambient':
            ambient = [int(args[0]), int(args[1]), int(args[2])]
            
    #PASS 1

    frames = [{} for i in range(framecount)]

    for command in commands:
        c = command['op']
        args = command['args']

        if c == 'vary':
            knobname = command['knob']
            start_frame = int(args[0])
            end_frame = int(args[1])
            start_val = int(args[2])
            end_val = int(args[3])
            change = float((end_val - start_val)) / (end_frame - start_frame - 1) 
            value = start_val
            for i in range(start_frame, end_frame):
                frames[i][knobname] = value

                value += change

    #PASS 2
    for frame in range(framecount):
        tmp = new_matrix()
        ident( tmp )
        stack = [ [x[:] for x in tmp] ]
        tmp = []
        screen = new_screen()
        zbuffer = new_zbuffer()
        for knob in frames[frame]:
            symbols[knob][1] = frames[frame][knob]
        for command in commands:
            c = command['op']
            args = command['args']
            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                        args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                    add_torus(tmp,args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                        args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                if framecount > 1:
                    knob = command['knob']
                    mult = 1
                    if knob:
                        mult = symbols[knob][1]
                else: 
                    mult = 1
                tmp = make_translate(args[0] * mult, args[1] * mult, args[2] * mult)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                if framecount > 1:
                    knob = command['knob']
                    mult = 1
                    if knob:
                        mult = symbols[knob][1]
                else: 
                    mult = 1
                tmp = make_scale(args[0] * mult, args[1] * mult, args[2] * mult)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                if framecount > 1:
                    knob = command['knob']
                    mult = 1
                    if knob:
                        mult = symbols[knob][1]
                else: 
                    mult = 1
                theta = args[1] * (math.pi/180) * mult
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
        if basename:
            if not os.path.exists('images'):
                os.makedirs('images')
            save_extension(screen, 'images/' + basename + str(frame).zfill(3) + ".png")
        elif c == 'display':
            display(screen)
        elif c == 'save':
            save_extension(screen, args[0])