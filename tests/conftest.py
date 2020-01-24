from dial import __version__

collect_ignore = ["setup.py"]


def pytest_report_header(config):
    return f"Dial {__version__}"
