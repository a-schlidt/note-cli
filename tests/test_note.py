import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "note"


class NoteCliTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db = Path(self.tempdir.name) / ".notes" / "db"
        self.env = {**os.environ, "NOTE_DB_DIR": str(self.db)}

    def tearDown(self):
        self.tempdir.cleanup()

    def run_note(self, *args):
        return subprocess.run(
            [str(SCRIPT), *args],
            text=True,
            capture_output=True,
            env=self.env,
            check=False,
        )

    def test_add_stores_exact_content_named_by_sha256(self):
        content = "hello note"
        result = self.run_note("add", content)
        digest = hashlib.sha256(content.encode()).hexdigest()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), digest)
        self.assertEqual((self.db / digest).read_text(), content)
        self.assertEqual(list(self.db.iterdir()), [self.db / digest])

    def test_duplicate_add_does_not_create_another_file(self):
        self.run_note("add", "same")
        self.run_note("add", "same")
        self.assertEqual(len(list(self.db.iterdir())), 1)

    def test_delete_removes_note(self):
        added = self.run_note("add", "delete me")
        digest = added.stdout.strip()
        result = self.run_note("delete", digest)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.db / digest).exists())

    def test_delete_rejects_path_traversal(self):
        result = self.run_note("delete", "../outside")
        self.assertEqual(result.returncode, 2)
        self.assertIn("hash must be", result.stderr)

    def test_delete_missing_note_fails(self):
        digest = hashlib.sha256(b"missing").hexdigest()
        result = self.run_note("delete", digest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("note not found", result.stderr)

    def test_unknown_command_fails(self):
        self.assertEqual(self.run_note("wat").returncode, 2)


if __name__ == "__main__":
    unittest.main()
