from __future__ import annotations

import logging
from pathlib import Path

DEFAULT_S3_URL = "s3://mangetamain/recipes_merged.csv.gz"


def download_from_s3(
    *,
    bucket: str = "mangetamain",
    key: str = "recipes_merged.csv.gz",
    dest_dir: str | Path = "data/clustering",
    logger: logging.Logger | None = None,
) -> Path:
    """Download from S3 using boto3 when available; fallback to stub.

    Environment:
      - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
    """
    log = logger or logging.getLogger("app.download_s3")
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    local = dest / key

    try:
        import boto3  # type: ignore
    except Exception:
        # Fallback to stub
        return download_from_s3_stub(key=key, dest_dir=dest)

    try:
        session = boto3.session.Session()
        s3 = session.client("s3")
        s3.download_file(bucket, key, str(local))
        log.info("Downloaded s3://%s/%s -> %s", bucket, key, local)
        return local
    except Exception as exc:  # pragma: no cover - network dependent
        log.warning("S3 download failed (%s), using stub", exc)
        return download_from_s3_stub(key=key, dest_dir=dest)


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
