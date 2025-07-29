from django.utils.timezone import now, localtime


def get_saved_timestamp(request):
    """
    Checks for ?saved=1 in the URL and returns formatted time/date.

    Returns:
        (saved: bool, saved_time: str, saved_date: str)
    """
    if request.GET.get("saved") != "1":
        return False, "", ""

    dt = localtime(now())
    return True, dt.strftime("%H:%M"), dt.strftime("%A, %B %d")
