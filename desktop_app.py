import threading
import webview
from app import create_app

app = create_app()

def run_flask():
    app.run(port=5050)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    webview.create_window(
        "IsimuSense",
        "http://127.0.0.1:5050",
        width=1200,
        height=800,
        resizable=True
    )

    webview.start()