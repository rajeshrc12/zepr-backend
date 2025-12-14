from io import BytesIO
import base64


def save_plot(plt, images: list):
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    images.append(b64_str)
