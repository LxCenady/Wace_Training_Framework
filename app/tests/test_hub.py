"""WTF Hub: the index, verified downloads and installing a pack into an empty data root (network replaced by the
repository's packs/ folder; never the owner's data)."""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "app")]
import hub, hub_index  # noqa: E402

BASE = "https://hub.example/packs"


class Hub(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hub-", dir=ROOT / "evidence" / "runtime")
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.index = hub_index.build(ROOT / "packs", BASE, {"CAIE9709": "experimental"})

        def fake_get(url, limit, timeout=30):  # the Hub's files, from this repository
            data = json.dumps(self.index).encode() if url.endswith("index.json") else \
                (ROOT / "packs" / url.rsplit("/", 1)[1]).read_bytes()
            if len(data) > limit:
                raise hub.HubError("download larger than allowed")
            return data
        patcher = mock.patch.object(hub, "get", fake_get)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_index_and_verified_download(self):
        index = hub.load("https://hub.example/index.json")
        ids = [e["id"] for e in index["packs"]]
        self.assertTrue({"MAM", "MAS", "MAA", "CHE", "PHY", "ACF"} <= set(ids))
        mam = next(e for e in index["packs"] if e["id"] == "MAM")
        path = hub.download(mam, self.dir / "dl")
        self.assertEqual(path.stat().st_size, mam["size"])
        with self.assertRaises(hub.HubError):  # a tampered or swapped file is never kept
            hub.download(dict(mam, sha256="0" * 64), self.dir / "dl2")
        self.assertFalse(any((self.dir / "dl2").glob("*.wtfpack")))
        with self.assertRaises(hub.HubError):
            hub.check(dict(mam, url="http://insecure.example/MAM.wtfpack"))

    def test_install_a_data_pack_into_an_empty_root(self):
        from tests import safe_runtime
        safe_runtime.isolate()
        from kernel import Kernel
        data = self.dir / "data"
        data.mkdir()
        with mock.patch.dict(os.environ, {"WACE_MATHS_ROOT": str(data)}):
            k = Kernel(str(data))
            k.load(["config", "edition", "compiler", "hub_install"])
            k.get("config")["hub_url"] = "https://hub.example/index.json"
            listed = {e["id"]: e for e in k.get("hub.index")()["packs"]}
            self.assertIsNone(listed["MAM"]["installed"])
            self.assertTrue(listed["MAM"]["compatible"])
            result = k.get("hub.install")("MAM")
            self.assertEqual(result, dict(kind="data", subject="MAM", next="papers"))
            self.assertTrue((data / "MAM" / "pack.json").exists())
            self.assertIn("MAM", k.get("config")["subjects"])
            self.assertEqual(k.get("hub.index")()["packs"][[e["id"] for e in self.index["packs"]].index("MAM")]["installed"],
                             "2026.10.2")


if __name__ == "__main__":
    unittest.main()
