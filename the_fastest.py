def get_best_time(times):
    seconds = []
    for time in times:
        h, m, s = time.split(":")
        seconds.append(int(h) * 3600 + int(m) * 60 + int(s))
    return times[seconds.index(min(seconds))]

print(get_best_time([input() for _ in range(int(input()))]))