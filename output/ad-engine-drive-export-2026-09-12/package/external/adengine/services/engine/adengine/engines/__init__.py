"""Provider adapters. Pure request construction + provider gotchas; no registry writes.

Every adapter takes its API key explicitly (from adengine.engines.credentials) and
resolves binaries (ffmpeg/ffprobe/yt-dlp/curl) through adengine.core.settings.
Nothing here reads a home directory, a vault, or an env file.
"""
