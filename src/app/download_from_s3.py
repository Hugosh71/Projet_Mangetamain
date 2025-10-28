from __future__ import annotations

from pathlib import Path


DEFAULT_S3_URL = "s3://mangetamain/recipes_merged.csv.gz"


def download_from_s3_stub(
    key: str = "recipes_merged.csv.gz", *, dest_dir: str | Path = "data/clustering"
) -> Path:
    """Stub to download recipes_merged.csv.gz from S3 into local dest.

    If the destination file doesn't exist locally, create it to simulate a
    download. The remote is assumed to be s3://mangetamain/<key>.
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    local = dest / key
    s3_url = f"s3://mangetamain/{key}"
    if local.exists():
        print(f"[stub] file already local: {local}")
        return local
    print(f"[stub] download from S3: {s3_url} -> {local}")
    local.touch(exist_ok=True)
    return local


