#!/usr/bin/env python3
"""Turn compiler claim tags in generated review HTML into static anchors.

Static links work in both a browser and WeasyPrint's PDF output. This runs after
Pandoc, so it does not alter the source manuscript or the compiler tags.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
text = text.replace('src="figures/', 'src="../figures/')
pattern = re.compile(r"\[(C-[A-Z0-9-]+)\]")
text = pattern.sub(
    lambda match: f'<a class="claim-link" href="#{match.group(1)}" title="Open source and review card">{match.group(0)}</a>',
    text,
)
path.write_text(text, encoding="utf-8")
