"""All configuration comes from environment variables. Never read a .env file, never Path.home()."""
from __future__ import annotations
import os
import shutil
from dataclasses import dataclass, field


def _env(name: str, default: str | None = None) -> str | None:
    v = os.environ.get(name)
    return v if v not in (None, "") else default


def _bin(name: str, env: str) -> str:
    return _env(env) or shutil.which(name) or name


@dataclass(frozen=True)
class Settings:
    # storage
    data_dir: str = field(default_factory=lambda: _env("ADENGINE_DATA_DIR", "/var/lib/adengine") or "/var/lib/adengine")
    store_backend: str = field(default_factory=lambda: _env("ADENGINE_STORE", "local") or "local")  # local | postgres
    database_url: str | None = field(default_factory=lambda: _env("DATABASE_URL"))
    object_store_url: str | None = field(default_factory=lambda: _env("OBJECT_STORE_URL"))
    public_base_url: str = field(default_factory=lambda: _env("ADENGINE_PUBLIC_URL", "http://localhost:3000") or "http://localhost:3000")
    # packages shipped with the image
    packages_dir: str = field(default_factory=lambda: _env("ADENGINE_PACKAGES_DIR", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "..", "packages")) or "")
    # binaries
    ffmpeg: str = field(default_factory=lambda: _bin("ffmpeg", "ADENGINE_FFMPEG"))
    ffprobe: str = field(default_factory=lambda: _bin("ffprobe", "ADENGINE_FFPROBE"))
    ytdlp: str = field(default_factory=lambda: _bin("yt-dlp", "ADENGINE_YTDLP"))
    curl: str = field(default_factory=lambda: _bin("curl", "ADENGINE_CURL"))
    # auth
    dev_workspace: str | None = field(default_factory=lambda: _env("ADENGINE_DEV_WORKSPACE"))
    auth_mode: str = field(default_factory=lambda: _env("ADENGINE_AUTH", "dev") or "dev")  # dev | oauth
    # cost rates (USD per unit), overridable per deployment
    kie_credit_usd: float = field(default_factory=lambda: float(_env("ADENGINE_KIE_CREDIT_USD", "0.004") or 0.004))

    def packages_path(self, *parts: str) -> str:
        return os.path.normpath(os.path.join(self.packages_dir, *parts))


settings = Settings()
