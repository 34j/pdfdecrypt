from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

import pikepdf

from pdfdecrypt import decrypt_pdf


class TestMain(TestCase):
    def test_decrypt(self):
        with TemporaryDirectory() as dirname:
            filename = Path(dirname, "test.pdf")
            filename_out = Path(dirname, "test.pdf")
            pikepdf.new().save(
                filename,
                encryption=pikepdf.Encryption(
                    owner="owner_password", user="user_password"
                ),
            )
            decrypt_pdf(filename, filename_out, "user_password")
            pdf = pikepdf.open(filename_out)
            self.assertFalse(pdf.is_encrypted)
            pdf.close()

    def test_not_encrypted(self):
        with TemporaryDirectory() as dirname:
            filename = Path(dirname, "test.pdf")
            pikepdf.new().save(filename)
            with self.assertRaises(ValueError):
                decrypt_pdf(filename, filename, "user_password")
