from dial import __version__


def pytest_report_header(config):
    return f"Dial {__version__}"
