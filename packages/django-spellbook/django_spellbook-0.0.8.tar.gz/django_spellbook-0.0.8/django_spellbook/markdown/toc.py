# django_spellbook/markdown/toc.py
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

from django_spellbook.utils import remove_leading_dash


@dataclass
class TOCEntry:
    title: str
    url: str
    children: Dict[str, 'TOCEntry'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = {}


class TOCGenerator:
    def __init__(self):
        self.root = TOCEntry(title="root", url="", children={})

    def add_entry(self, file_path: Path, title: str, url: str):
        """Add a file to the TOC structure"""
        parts = file_path.parent.parts
        current = self.root

        # Handle root-level files
        if not parts:
            current.children[file_path.stem] = TOCEntry(
                title=remove_leading_dash(title),
                url=remove_leading_dash(url),
            )
            return

        # Handle nested files
        for part in parts:
            if part not in current.children:
                current.children[part] = TOCEntry(
                    title=remove_leading_dash(part.replace('-', ' ').title()),
                    # Just use the directory name
                    url=remove_leading_dash(part),
                )
            current = current.children[part]

        # Add the actual file
        filename = file_path.stem
        current.children[filename] = TOCEntry(
            title=remove_leading_dash(title),
            # Use the full provided URL for files
            url=remove_leading_dash(url),
        )

    def get_toc(self) -> Dict:
        """Get the complete TOC structure"""
        def _convert_to_dict(entry: TOCEntry) -> Dict:
            result = {
                'title': remove_leading_dash(entry.title),
                'url': remove_leading_dash(entry.url),
            }
            if entry.children:
                result['children'] = {
                    k: _convert_to_dict(v)
                    for k, v in sorted(entry.children.items())
                }
            return result

        return _convert_to_dict(self.root)
