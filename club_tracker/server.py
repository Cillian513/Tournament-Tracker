"""The little web server and its request handler."""
import secrets
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .actions import POST_ROUTES
from .config import DB_PATH, LOGO_PATH, LOG_PATH, PORT, TOKEN, TROPHY_PATH, SPONGEBOB_PATH
from .database import connect
from .export import export_csv
from .helpers import back
from .pages import PAGES
from .templates import layout


def log_error(text):
    print(text, file=sys.stderr)
    try:
        LOG_PATH.write_text(text, encoding="utf-8")
    except OSError:
        pass


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # no request spam in the terminal
        pass

    def send(self, status, body, ctype="text/html; charset=utf-8", extra=None):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def redirect(self, location):
        self.send(303, "", extra={"Location": location})

    def host_ok(self):
        # only answer if the browser asked for localhost
        return self.headers.get("Host", "").rsplit(":", 1)[0] in ("127.0.0.1", "localhost")

    def do_GET(self):
        if not self.host_ok():
            return self.send(403, "Forbidden")
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        conn = connect()
        try:
            key = url.path.strip("/")
            if key == "":
                return self.redirect("/record")
            if key in PAGES:
                title, subtitle, body = PAGES[key](conn, q)
                kind = q.get("kind") if q.get("kind") in ("ok", "err") else "ok"
                return self.send(200, layout(key, title, subtitle, body, q.get("msg"), kind))
            if key == "logo" and LOGO_PATH.exists():
                return self.send(200, LOGO_PATH.read_bytes(), "image/jpeg")
            if key == "trophy" and TROPHY_PATH.exists():
                            return self.send(200, TROPHY_PATH.read_bytes(), "image/jpeg")
            if key == "spongebob" and SPONGEBOB_PATH.exists():
                return self.send(200, SPONGEBOB_PATH.read_bytes(), "image/gif")
            if key == "export":
                filename, data = export_csv(conn, q)
                if not filename:
                    return self.redirect(back("/tournaments", msg="Create a tournament first.", kind="err"))
                return self.send(200, data, "text/csv; charset=utf-8",
                                 {"Content-Disposition": f'attachment; filename="{filename}"'})
            self.send(404, layout("", "Not found", "That page doesn't exist.",
                                  '<div class="card"><a class="btn" href="/record">Back to the tracker</a></div>'))
        except Exception:
            self.fail()
        finally:
            conn.close()

    def do_POST(self):
        if not self.host_ok():
            return self.send(403, "Forbidden")
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length > 100_000:
            return self.send(413, "Too large")
        form = {k: v[0] for k, v in parse_qs(self.rfile.read(length).decode("utf-8", "replace"),
                                             keep_blank_values=True).items()}
        if not secrets.compare_digest(form.get("token", ""), TOKEN):
            return self.send(403, "Session expired - go back and reload the page.")
        path = urlparse(self.path).path
        if path == "/quit":
            self.send(200, "<!doctype html><title>Stopped</title><body style='font-family:sans-serif;"
                           "padding:40px'><h2>Club Tracker has stopped.</h2>"
                           "<p>Your data is saved. You can close this tab.</p></body>")
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        action = POST_ROUTES.get(path)
        if not action:
            return self.send(404, "Not found")
        conn = connect()
        try:
            self.redirect(action(conn, form))
        except Exception:
            self.fail()
        finally:
            conn.close()

    def fail(self):
        log_error(traceback.format_exc())
        self.send(500, layout("", "Something went wrong", "The details were saved to crash_log.txt.",
                              '<div class="card"><a class="btn" href="/record">Back to the tracker</a></div>'))


def main():
    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:  # port taken (already running?) so let the OS choose
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"Club Tracker is running at {url}")
    print("It should open in your browser. To stop it, click Quit in the sidebar or press Ctrl+C here.")
    threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Stopped. Your data is saved in", DB_PATH)
