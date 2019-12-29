from dial import __version__, __requirements__

def pytest_report_header(config):
    return f"Dial {__version__}"

