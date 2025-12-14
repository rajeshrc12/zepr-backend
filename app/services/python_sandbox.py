# fmt: off

import traceback
import builtins
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from app.utils.matplotlib_capture import save_plot


def execute_code(code: str):
    outputs = []

    original_show = plt.show
    original_print = builtins.print  # ✅ SAFE

    def capture_show():
        buf_images = []
        save_plot(plt, buf_images)
        outputs.append({"image": buf_images[0]})

    def capture_print(*args, **kwargs):
        if len(args) == 1 and isinstance(args[0], (dict, list)):
            outputs.append({"text": args[0]})
        else:
            outputs.append({"text": " ".join(map(str, args))})

    plt.show = capture_show
    builtins.print = capture_print  # ✅ override globally

    exec_globals = {
        "pd": pd,
        "plt": plt,
        "__builtins__": builtins,
    }

    try:
        exec(code, exec_globals)

        if plt.get_fignums():
            capture_show()

        return {
            "outputs": outputs,
            "error": None,
        }

    except Exception:
        return {
            "outputs": outputs,
            "error": traceback.format_exc(),
        }

    finally:
        plt.show = original_show
        builtins.print = original_print  # 🔁 restore
