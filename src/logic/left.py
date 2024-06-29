def need_notify(total_seconds: int | float):
    hours = int(total_seconds / 3600)
    # return hours < 24 * 35
    return hours in (0, 1, 2, 8, 24, 24 * 2, 24 * 3, 24 * 4, 24 * 6, 24 * 8, 24 * 10, 24 * 14)
