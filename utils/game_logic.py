def calculate_activation_time(intelligence):
    start_minutes = 15
    end_minutes = 3 * 60

    total_range = end_minutes - start_minutes

    t = total_range / 19 * (20 - intelligence)

    total = start_minutes + t

    hours = int(total // 60)
    mins = int(total % 60)

    display_hours = 12 if hours == 0 else hours

    return [display_hours, mins]

def calculate_iter_for_screamer(intelligence):
    min_iter = 4
    avaible_iter = 8

    iter_num = min_iter + int(avaible_iter / 20 * (21 - intelligence))

    return iter_num