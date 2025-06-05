import sys
import sys
import types
import pydantic

# Stub rich.logging.RichHandler if rich is not installed
if 'rich.logging' not in sys.modules:
    class RichHandler:
        def __init__(self, *args, **kwargs):
            pass

        def setFormatter(self, *args, **kwargs):
            pass

    rich_logging = types.SimpleNamespace(RichHandler=RichHandler)
    sys.modules['rich.logging'] = rich_logging

if not hasattr(pydantic, "validate_call"):
    def validate_call(func):
        return func

    pydantic.validate_call = validate_call

fake_settings = types.SimpleNamespace(
    phi_cli_settings=types.SimpleNamespace(api_runtime="dev")
)
sys.modules.setdefault("phi.cli.settings", fake_settings)

from phi.tools.function import Function
from phi.utils.functions import get_function_call


def dummy(name: str, flag: bool, greeting: str) -> str:
    return f"{name}:{flag}:{greeting}"


def test_get_function_call_sanitization():
    func = Function(name="dummy", entrypoint=dummy)
    args = '{"name": "Truedraw", "flag": True, "greeting": "Hello True"}'
    fc = get_function_call("dummy", arguments=args, functions={"dummy": func})
    assert fc is not None
    assert fc.arguments == {
        "name": "Truedraw",
        "flag": True,
        "greeting": "Hello True",
    }
