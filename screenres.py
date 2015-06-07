import ctypes
user32 = ctypes.windll.user32
W,H = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
