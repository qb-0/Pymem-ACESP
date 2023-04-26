import ctypes
from ctypes import wintypes
from pyray import get_screen_height, get_screen_width

class Pointer:
    player_count = 0x18AC0C
    entity_list = 0x18AC04
    local_player = 0x18AC00
    view_matrix = 0x17DFD0


class Vec2(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float)
    ]


class Vec2_int(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int)
    ]


class Vec3(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float)
    ]

class Entity(ctypes.Structure):
    _fields_ = [
        ("", 0x4 * ctypes.c_byte),
        ("pos", Vec3),
        ("", 0xDC * ctypes.c_byte),
        ("health", ctypes.c_int),
        ("", 0x115 * ctypes.c_byte),
        ("name", 0x50 * ctypes.c_char),
        ("", 0xB7 * ctypes.c_byte),
        ("team", ctypes.c_int)
    ]

class WINDOWINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('rcWindow', wintypes.RECT),
        ('rcClient', wintypes.RECT),
        ('dwStyle', wintypes.DWORD),
        ('dwExStyle', wintypes.DWORD),
        ('dwWindowStatus', wintypes.DWORD),
        ('cxWindowBorders', wintypes.UINT),
        ('cyWindowBorders', wintypes.UINT),
        ('atomWindowType', wintypes.ATOM),
        ('wCreatorVersion', wintypes.WORD),
    ]


def get_window_info(title):
    hwnd = ctypes.windll.user32.FindWindowA(0, ctypes.c_char_p(title.encode()))
    win_info = WINDOWINFO()
    rect = wintypes.RECT()
    ctypes.windll.user32.GetWindowInfo(hwnd, ctypes.byref(win_info))
    ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect))
    return (win_info.rcClient.left, win_info.rcClient.top, rect.right, rect.bottom)


def world_to_screen(matrix, pos):
    clip = Vec3()
    ndc = Vec2()
    result = Vec2_int()

    clip.z = pos.x * matrix[3] + pos.y * matrix[7] + pos.z * matrix[11] + matrix[15]
    if clip.z < 0.2:
        raise IOError("WTS: Out of bounds")
    clip.x = pos.x * matrix[0] + pos.y * matrix[4] + pos.z * matrix[8] + matrix[12]
    clip.y = pos.x * matrix[1] + pos.y * matrix[5] + pos.z * matrix[9] + matrix[13]
    ndc.x = clip.x / clip.z
    ndc.y = clip.y / clip.z
    try:
        result.x = int((get_screen_width() / 2 * ndc.x) + (ndc.x + get_screen_width() / 2))
        result.y = int(-(get_screen_height() / 2 * ndc.y) + (ndc.y + get_screen_height() / 2))
    except Exception as e:
        raise IOError(f"WTS: {e}")
    return result