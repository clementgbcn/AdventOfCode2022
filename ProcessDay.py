import importlib

from DayFactory import DayFactory

NB_MAX_DAY = 7
LAST_DAY = True
SECOND_STAR = True

# Get the number of Day implemented
for d in range(1, NB_MAX_DAY + 1):
    day_name = "Day%.2d" % d
    try:
        getattr(importlib.import_module(day_name), day_name)
        nb_day = d
    except ModuleNotFoundError:
        break

# Print Header
result_title = "Result"
time_title = "Elapsed Time"
print(f"Day\t\tStar\tTest Type\t{result_title:>16}\t|\t{time_title:>6}")
separator = "-" * 70


dayFactory = DayFactory(nb_day)
if LAST_DAY:
    day = dayFactory.get_day(nb_day)
    day.process_first_star()
    if SECOND_STAR:
        day = dayFactory.get_day(nb_day)
        day.process_second_star()
else:
    for i in range(1, nb_day + 1):
        print(separator)
        day = dayFactory.get_day(i)
        day.process_first_star()
        if SECOND_STAR:
            day = dayFactory.get_day(i)
            day.process_second_star()
    print(separator)
