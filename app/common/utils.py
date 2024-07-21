from pyinstrument import Profiler


def profile_timer(func):
    async def wrapper(*args, **kwargs):
        profiler = Profiler(interval=0.0001, async_mode="enabled")
        profiler.start()
        result = await func(*args, **kwargs)
        profiler.stop()
        profiler.print()
        return result

    return wrapper
