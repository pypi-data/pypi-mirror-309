from functools import cached_property, partial
from pathlib import Path
from typing import Optional

from iolanta.iolanta import Iolanta
from iolanta.namespaces import IOLANTA
from iolanta_jinja2.macros import template_render
from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from yarl import URL


class IolantaPlugin(BasePlugin):   # type: ignore
    """Integrate MkDocs + iolanta."""

    @cached_property
    def iolanta(self) -> Iolanta:
        return Iolanta()

    @cached_property
    def template_per_page(self) -> dict[str, str]:
        """Associate MkDocs file pages → templates assigned in graph."""
        query_path = Path(__file__).parent / 'sparql/template_per_page.sparql'
        rows = self.iolanta.query(query_path.read_text())
        return {
            URL(row['page']).path: row['template'].value
            for row in rows
        }

    def on_files(
        self,
        files: Files,
        *,
        config: MkDocsConfig,
    ) -> Optional[Files]:
        """Construct the local iolanta instance and load files."""
        self.iolanta.add(source=Path(config.docs_dir))
        return files

    def on_config(self, config: MkDocsConfig) -> Optional[MkDocsConfig]:
        """Expose configuration & template variables."""
        config.extra['iolanta'] = self.iolanta
        config.extra['render'] = partial(
            template_render,
            iolanta=self.iolanta,
            environments=[IOLANTA.html],
        )
        return config

    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files,
    ) -> Optional[str]:
        """Assign page `template` property from `mkdocs-material:template`."""
        if template := self.template_per_page.get(page.file.src_path):
            page.meta['template'] = template

        return markdown
