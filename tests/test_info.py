from _pytest.capture import CaptureFixture

import decorative_parts


def test_info(capsys: CaptureFixture) -> None:
    decorative_parts.info()
    output = capsys.readouterr().out
    assert decorative_parts.info_dump in output
