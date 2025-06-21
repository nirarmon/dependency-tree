import pytest

class SimpleSpy:
    def __init__(self, func):
        self._func = func
        self.call_count = 0
        self.call_args = None
        self.call_kwargs = None
    def __call__(self, *args, **kwargs):
        self.call_count += 1
        self.call_args = args
        self.call_kwargs = kwargs
        return self._func(*args, **kwargs)
    def assert_called_with(self, *args, **kwargs):
        assert self.call_args == args and self.call_kwargs == kwargs

class Mocker:
    def spy(self, obj, method_name):
        original = getattr(obj, method_name)
        spy = SimpleSpy(original)
        setattr(obj, method_name, spy)
        return spy

@pytest.fixture
def mocker():
    return Mocker()
