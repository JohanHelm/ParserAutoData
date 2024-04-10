from utils import mark_duration


def test_mark_duration():
    assert mark_duration.duration(4229, 8867) == "01:17:18"


