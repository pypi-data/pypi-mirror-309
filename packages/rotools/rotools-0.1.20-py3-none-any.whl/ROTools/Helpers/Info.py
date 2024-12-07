import os
import humanize
from datetime import datetime, timezone

def print_info():
    print()
    build_ver = os.getenv("RR_BUILD_VERSION")
    print(f"Build version    \t: {build_ver}")
    build_time = os.getenv("RR_BUILD_TIME")
    print(f"Build time UTC   \t: {build_time}")
    print(f"Current time UTC \t: {datetime.now(timezone.utc)}")
    if build_time is not None:
        build_time = datetime.fromisoformat(build_time)
        build_old = humanize.naturaltime(datetime.now(timezone.utc) - build_time)
        print(f"Build old\t\t: {build_old}")
    print()