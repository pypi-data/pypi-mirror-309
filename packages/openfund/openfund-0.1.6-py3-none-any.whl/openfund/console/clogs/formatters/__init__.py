from __future__ import annotations

from openfund.console.clogs.formatters.builder_formatter import (
    BuilderLogFormatter,
)


FORMATTERS = {
    "poetry.core.masonry.builders.builder": BuilderLogFormatter(),
    "poetry.core.masonry.builders.sdist": BuilderLogFormatter(),
    "poetry.core.masonry.builders.wheel": BuilderLogFormatter(),
}
