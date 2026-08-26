"""Small, explicit data models used by the documentation pipeline."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    path: str
    title: str
    section: str = "Documentation"


@dataclass(frozen=True)
class SiteConfig:
    name: str
    description: str
    repository_url: str | None
    site_url: str | None
    accent: str
    accent_secondary: str
    banner: str | None
    banner_alt: str | None
    footer: str | None
    project_links: tuple[tuple[str, str], ...]
    pages: tuple[Page, ...]
    legacy: bool
    home_document: str
