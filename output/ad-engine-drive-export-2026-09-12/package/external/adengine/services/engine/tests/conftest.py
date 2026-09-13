"""Make the adengine package importable when pytest runs from the repo root."""
import os, sys
import tempfile

# Settings are loaded once at import time; pin test defaults before any test module
# imports the engine rather than depending on collection order.
_data = tempfile.TemporaryDirectory(prefix="adengine-tests-")
os.environ["ADENGINE_DATA_DIR"] = _data.name
os.environ["ADENGINE_DEV_WORKSPACE"] = "ws_test"
os.environ["ADENGINE_AUTH"] = "dev"


def pytest_unconfigure(config):
    _data.cleanup()
ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ENGINE not in sys.path:
    sys.path.insert(0, ENGINE)
