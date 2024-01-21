from .api import CheckIn


def try_check_in(check_in: CheckIn, retry: int = 0):
    return any(
        (check_in.done or check_in.now()) and not check_in.reset() for _ in range(0, retry + 1)
    )
