from __future__ import annotations

from pathlib import Path


def upload_to_s3_stub(file_path: str | Path, *, bucket: str | None = None) -> None:
    """Stub for uploading a file to S3.

    Args:
        file_path: Local path to file to upload
        bucket: Optional bucket name (unused stub)
    """
    path = Path(file_path)
    print(f"[stub] upload to S3: {path} (bucket={bucket or 'default'})")
