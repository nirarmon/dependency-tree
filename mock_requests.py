class _Codes:
    ok = 200


codes = _Codes()


def get(url, *args, **kwargs):
    raise NotImplementedError("HTTP requests are disabled in tests")
