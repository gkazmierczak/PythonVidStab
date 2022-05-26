def durationFromMs(ms):
    s = ms // 1000
    mm = s // 60
    s = s % 60
    return f"{mm:02d}:{s:02d}"
