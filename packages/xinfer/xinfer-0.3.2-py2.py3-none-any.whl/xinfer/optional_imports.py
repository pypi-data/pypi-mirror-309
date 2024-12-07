import importlib


def soft_import(name: str):
    try:
        module = importlib.import_module(name)
        # Verify the module is actually loaded and has a real file path
        if (
            module
            and hasattr(module, "__file__")
            and module.__file__ is not None
            and (
                "site-packages" in str(module.__file__)
                or "dist-packages" in str(module.__file__)
            )
        ):
            return True
        return False
    except (ModuleNotFoundError, ImportError) as e:
        if str(e) != f"No module named '{name}'":
            raise e
        return False


# Check for available modules
timm_available = soft_import("timm")
transformers_available = soft_import("transformers")
ultralytics_available = soft_import("ultralytics")
vllm_available = soft_import("vllm")
ollama_available = soft_import("ollama")


# Create placeholder classes
def create_placeholder(name):
    return type(name, (), {})


# Import or create placeholder classes so that we can still use the class types
if timm_available:
    from .timm.timm_model import TimmModel
else:
    TimmModel = create_placeholder("TimmModel")

if transformers_available:
    from .transformers.vision2seq import Vision2SeqModel
else:
    Vision2SeqModel = create_placeholder("Vision2SeqModel")

if ultralytics_available:
    from .ultralytics.ultralytics_model import UltralyticsModel
else:
    UltralyticsModel = create_placeholder("UltralyticsModel")
