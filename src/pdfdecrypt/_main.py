import warnings
from pathlib import Path

import pikepdf


def decrypt_pdf(input_path: Path, output_path: Path, password: str) -> None:
    """Decrypts a PDF file."""
    with warnings.catch_warnings(record=True) as w:
        pdf = pikepdf.open(input_path, password=password)

    # UserWarning: A password was provided, but no password was needed to open this PDF.
    if any(
        [
            w_.category == UserWarning
            and "A password was provided, but no password was needed to open this PDF."
            in str(w_.message)
            for w_ in w
        ]
    ):
        raise ValueError(f"File {input_path} is not encrypted.")

    pdf.save(output_path)
    pdf.close()
