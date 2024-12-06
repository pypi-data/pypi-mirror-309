#!python
# -*- mode: python ; coding: utf-8 -*-

import win32api
import subprocess
import sys
import os
import platform
import psutil
import math
import getpass
import datetime
import time
import calendar

__version__ = "1.2.7"

"""
# old windows only code
def format_date(_: tuple[int]) -> str:
    year = _[0]
    month = _[1]
    weekday = _[2]
    day = _[3]

    weekdict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    monthdict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    daysufd = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th', 5: 'th', 6: 'th', 7: 'th', 8: 'th', 9: 'th', 10: 'th', 11: 'th', 12: 'th', 13: 'th', 14: 'th', 15: 'th', 16: 'th', 17: 'th', 18: 'th', 19: 'th', 20: 'th', 21: 'st', 22: 'nd', 23: 'rd', 24: 'th', 25: 'th', 26: 'th', 27: 'th', 28: 'th', 29: 'th', 30: 'th', 31: 'st'}

    fmtd = f"{weekdict[weekday]}, {monthdict[month]} {day}{daysufd[day]} {year}"

    return fmtd

def format_time_win(_: tuple[int]) -> str:
    hour = _[4]
    minute = _[5]

    if hour < 10:
        hour = f"0{hour}"

    if minute < 10:
        minute = f"0{minute}"

    return f"{hour}:{minute}"
"""

def get_process(pid: int) -> str:
    return f"{psutil.Process(pid).name()} (PID {pid})"

def current_process() -> str:
    curp = get_process(os.getpid())
    return curp

def get_archi() -> str:
    archi = platform.architecture()[0]
    archi = archi.replace('64bit', 'x64')
    archi = archi.replace('32bit', 'x32')

    sparc = platform.machine()
    return f"{archi} ({sparc})"

"""
# might re-add later
def python_version() -> str:
    fmt = f"{platform.python_implementation()}-{platform.python_version()}:{platform.python_revision()}"
    return fmt
"""

def battery() -> str:
    """
    # old windows-only version
    return f"{dict(win32api.GetSystemPowerStatus())['BatteryLifePercent']}%"
    """

    info = psutil.sensors_battery()
    percent = info[0]
    plugged = info[2]

    if plugged:
        if int(percent) == 100:
            info = f"{percent}% (Plugged in)"

        else:
            info = f"{percent}% (Charging)"

    else:
        info = f"{percent}%"

    return info

def computer_name() -> str:
    return platform.node()

def platform_type() -> str:
    return platform.system()

def fmt_weekday(wd) -> str:
    d = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    return d[wd]

def get_weekday() -> str:
    return fmt_weekday(int(datetime.datetime.now().weekday()))

def fmt_month(mn) -> str:
    d = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    return d[mn]

def get_month() -> str:
    return fmt_month(datetime.datetime.now().month)

def get_day() -> str:
    return datetime.datetime.now().day

def day_suff(day) -> str:
    d = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th', 5: 'th', 6: 'th', 7: 'th', 8: 'th', 9: 'th', 10: 'th', 11: 'th', 12: 'th', 13: 'th', 14: 'th', 15: 'th', 16: 'th', 17: 'th', 18: 'th', 19: 'th', 20: 'th', 21: 'st', 22: 'nd', 23: 'rd', 24: 'th', 25: 'th', 26: 'th', 27: 'th', 28: 'th', 29: 'th', 30: 'th', 31: 'st'}
    return d[day]

def get_day_suff(d) -> str:
    return day_suff(int(datetime.datetime.now().day))

def get_year() -> str:
    return f"{datetime.datetime.now().year}"

def get_date() -> str:
    """
    # old windows only version
    return f"{format_date(tuple(win32api.GetLocalTime()))}"
    """
    
    return f"{get_weekday()}, {get_month()} {get_day()}{get_day_suff(get_day())} {get_year()}"
    
def get_time() -> str:
    """
    # old windows only version
    return f"{format_time_win(tuple(win32api.GetLocalTime()))}"
    """

    return datetime.datetime.now().strftime("%H:%M")
    
def username() -> str:
    return f"{getpass.getuser()}"

def get_cpu() -> str:
    return f"{psutil.cpu_count(logical=True)}"

def get_phy_cpu() -> str:
    return f"{psutil.cpu_count(logical=False)}"

def mono_cpu_usg() -> str:
    return f"{psutil.cpu_percent(interval=1)}%"

def percpu() -> str:
    orig = psutil.cpu_percent(interval=1, percpu=True)

    for i in range(len(orig)):
        orig[i] = str(f"{orig[i]}%")

    return ', '.join(orig)

def avpercpu() -> str:
    usg = 0
    cnt = 0

    for i in list(psutil.cpu_percent(interval=1, percpu=True)):
        usg += i
        cnt += 1

    return f"{round(usg / cnt, 1)}%"

def freqcpu() -> str:
    orig = psutil.cpu_freq(percpu=False)[0]

    if float(int(float(orig))) == float(orig):
        orig = int(orig)

    return f"{orig}Mhz"

def cpu_dist() -> str:
    return f"({int(get_phy_cpu())} physical, {int(get_cpu()) - int(get_phy_cpu())} other)"

def main() -> str:
    res: str = ""
    res += f"Hostname: {computer_name()}\n"
    res += f"Platform: {platform_type()}\n"
    res += f"Current User: {username()}\n"
    res += f"Date: {get_date()}\n"
    res += f"Time: {get_time()}\n"
    res += f"Battery: {battery()}\n"
    res += f"CPUs: {get_cpu()} {cpu_dist()}\n"
    res += f"Architecture: {get_archi()}\n"
    res += f"CPU Usage (Total): {mono_cpu_usg()}\n"
    res += f"CPU Usage (Per CPU): {percpu()}\n"
    res += f"Mean CPU Usage (Per CPU): {avpercpu()}\n"
    res += f"CPU Frequency: {freqcpu()}\n"
    # res += f"Current Process: {current_process()}"
    print(res)


if __name__ == "__main__":
    main()