# llmadventure.web package

class WebServer:
    """
    Basic placeholder for the web server interface.
    Replace with actual implementation as needed.
    """
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.running = False

    def start(self, host=None, port=None):
        self.host = host or self.host
        self.port = port or self.port
        self.running = True
        print(f"[llmadventure.web] Web server started at http://{self.host}:{self.port}")

    def stop(self):
        self.running = False
        print("[llmadventure.web] Web server stopped.")


def start_web_server(host="0.0.0.0", port=8000):
    """
    Programmatic entry point for starting the web server.
    """
    server = WebServer(host=host, port=port)
    server.start()
    return server
