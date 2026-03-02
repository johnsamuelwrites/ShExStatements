#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Parser cache for improved performance.

This module provides a singleton parser instance to avoid the overhead
of rebuilding the lexer and parser on every request. The PLY library
generates parser tables which can be expensive to recreate.
"""

import os
import tempfile
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shexstatements.shexstatementsparser import ShExStatementLexerParser


# Set PLY output directory to a writable location (for parser.out file)
_ply_output_dir = os.path.join(tempfile.gettempdir(), "shexstatements_ply")
os.makedirs(_ply_output_dir, exist_ok=True)


class ParserCache:
    """
    Thread-safe singleton cache for the ShExStatementLexerParser.

    This class ensures that only one parser instance is created and reused
    across multiple requests, significantly improving performance.

    Usage:
        parser = ParserCache.get_parser()
        result = parser.parse(data)

    Note:
        The parser itself maintains state during parsing, so for thread safety
        in concurrent environments, consider using get_fresh_parser() which
        returns a new instance each time, or implement proper synchronization.
    """

    _parser: "ShExStatementLexerParser | None" = None
    _lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    @classmethod
    def get_parser(cls) -> "ShExStatementLexerParser":
        """
        Get the cached parser instance (singleton pattern).

        Returns a shared parser instance. This is efficient but note that
        the parser maintains internal state, so this should only be used
        in single-threaded contexts or with external synchronization.

        Returns:
            ShExStatementLexerParser: The cached parser instance.
        """
        if cls._parser is None:
            with cls._lock:
                if cls._parser is None:
                    cls._parser = cls._create_parser()
                    cls._initialized = True
        return cls._parser

    @classmethod
    def get_fresh_parser(cls) -> "ShExStatementLexerParser":
        """
        Get a fresh parser instance (not cached).

        Creates a new parser instance each time. This is thread-safe
        and suitable for concurrent use, but has more overhead than
        the cached version.

        Returns:
            ShExStatementLexerParser: A new parser instance.
        """
        return cls._create_parser()

    @classmethod
    def _create_parser(cls) -> "ShExStatementLexerParser":
        """
        Create and initialize a new parser instance.

        Returns:
            ShExStatementLexerParser: A fully initialized parser.
        """
        from shexstatements.shexstatementsparser import ShExStatementLexerParser

        parser = ShExStatementLexerParser()
        parser.build()
        # Use writable output directory for PLY's parser.out file
        parser.buildparser(outputdir=_ply_output_dir, debuglog=None, errorlog=None)
        return parser

    @classmethod
    def reset(cls) -> None:
        """
        Reset the cached parser.

        This forces the next call to get_parser() to create a new instance.
        Useful for testing or if the parser needs to be reconfigured.
        """
        with cls._lock:
            cls._parser = None
            cls._initialized = False

    @classmethod
    def is_initialized(cls) -> bool:
        """
        Check if the parser has been initialized.

        Returns:
            bool: True if the parser cache has been initialized.
        """
        return cls._initialized
