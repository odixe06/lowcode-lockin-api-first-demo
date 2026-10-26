import json, tempfile, threading, unittest
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from api.server import make_handler

class PortabilityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.tmp.name) / "tickets.db")
        self.start_server()
    def start_server(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.db))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"
    def stop_server(self):
        self.server.shutdown(); self.thread.join(); self.server.server_close()
    def tearDown(self):
        self.stop_server(); self.tmp.cleanup()
    def post(self, data):
        request = Request(self.url+"/tickets", json.dumps(data).encode(), {"Content-Type":"application/json"})
        with urlopen(request) as response:
            return response.status, json.load(response)
    def get(self, path):
        with urlopen(self.url+path) as response:
            return json.load(response)
    def test_data_survives_api_restart(self):
        status, row = self.post({"title":"  Yêu cầu tiếng Việt  "})
        self.assertEqual(status,201)
        self.assertEqual(row["title"],"Yêu cầu tiếng Việt")
        self.stop_server(); self.start_server()
        self.assertEqual(self.get("/tickets"), [row])
        self.assertEqual(self.get("/export"), [row])
    def test_validation_and_contract(self):
        for bad in [{"title":" "}, {"title":"x"*121}, {"title":None}, []]:
            with self.assertRaises(HTTPError) as context: self.post(bad)
            self.assertEqual(context.exception.code,400)
        self.assertEqual(self.get("/tickets"),[])
        self.assertEqual(self.get("/openapi.json")["openapi"],"3.0.3")
if __name__ == "__main__": unittest.main()
