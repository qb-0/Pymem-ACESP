from pymem import Pymem
from pyray import *
from helper import *
from ctypes import *


def init():
    win = get_window_info("AssaultCube")
    set_trace_log_level(5)
    set_target_fps(0)
    set_config_flags(ConfigFlags.FLAG_WINDOW_UNDECORATED)
    set_config_flags(ConfigFlags.FLAG_WINDOW_MOUSE_PASSTHROUGH)
    set_config_flags(ConfigFlags.FLAG_WINDOW_TRANSPARENT)
    set_config_flags(ConfigFlags.FLAG_WINDOW_TOPMOST)
    init_window(win[2], win[3], "AssaultCube ESP")
    set_window_position(win[0], win[1])


def main():
    proc = Pymem("ac_client.exe")
    base = proc.base_address

    while not window_should_close():
        matrix = proc.read_ctype(base + Pointer.view_matrix, (16 * c_float)())[:]
        player_count = proc.read_int(base + Pointer.player_count)

        begin_drawing()
        clear_background(BLANK)
        draw_fps(0, 0)
        
        if player_count > 1:
            ents = proc.read_ctype(
                proc.read_int(base + Pointer.entity_list), 
                (player_count * c_int)(), 
                get_py_value=False
            )[1:]
            for ent_addr in ents:
                ent_obj = proc.read_ctype(ent_addr, Entity())
                if ent_obj.health > 0:
                    try:
                        wts = world_to_screen(matrix, ent_obj.pos)
                    except:
                        continue
                    draw_line(get_screen_width() // 2, get_screen_height() // 2, wts.x, wts.y, BLUE if ent_obj.team else RED)
                    draw_text(ent_obj.name, wts.x, wts.y, 12, WHITE)

        end_drawing()

    

if __name__ == '__main__':
    init()
    main()