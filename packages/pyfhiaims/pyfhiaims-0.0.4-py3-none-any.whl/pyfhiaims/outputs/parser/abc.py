""" A main output file parser for FHI-aims. Realizes the Deterministic State Machine pattern
"""
from __future__ import annotations

import importlib
import random
import string
from abc import abstractmethod
import inspect
import re
from pathlib import Path
from typing import Any, IO, Type

from monty.io import zopen

from .converters import to_str
from .utils import update


def parser_classes(module) -> dict[str, Type[ChunkParser]]:
    """Returns the dict of all the file and chunk parser classes declared in
    the current module"""
    result = {}
    for _, cls in inspect.getmembers(module, inspect.isclass):
        if issubclass(cls, ChunkParser):
            result[cls.name] = cls
    return result


def _get_parser(parser_class, header_line):
    """A factory that injects the header line into the ChunkParser instance"""
    def _factory(file_descriptor: str | Path | IO,
                 parent: Parser = None) -> Parser:
        return parser_class(file_descriptor, parent, header_line)
    return _factory


class Parser:

    name: str = ""

    def __init__(self,
                 file_descriptor: str | Path | IO,
                 parent: FileParser = None) -> None:
        """ A base class for the parser. Gets the

        Parameters
        ----------
        file_descriptor: str | Path | IO
            A name or handle of the main output file
        parent: Parser
            A parent parser for the current instance
        """
        # get the module in which the actual implementation is located
        # (parsers.py) and available parsers within that module
        module = importlib.import_module(self.__module__)
        self._available_parsers = parser_classes(module)
        self.result = {}
        self.warnings = []
        self.errors = []
        # propagate metadata along inheritance line
        self.parent = parent
        if self.parent is None:
            self.run_metadata = {}
        else:
            self.run_metadata = self.parent.run_metadata
        self.next = None
        # open the file to parse
        if isinstance(file_descriptor, (str, Path)):
            self.fd = zopen(file_descriptor, "rt")
            self.is_root = True
        else:
            self.fd = file_descriptor
            self.is_root = False

    def __del__(self):
        """Close the file if it is the root parser"""
        if self.is_root:
            self.fd.close()

    @abstractmethod
    def parse(self):
        raise NotImplementedError

    @abstractmethod
    def annotate(self, annotated_file: str | Path | IO):
         raise NotImplementedError


class FileParser(Parser):

    initial_chunk: str

    def __init__(self,
                 file_descriptor: str | Path | IO,
                 parent: Parser = None,
                 header_line: str = None) -> None:
        """
        A main Parser object.

        Parameters
        ----------
        file_descriptor : str | Path | IO
            A name or handle of the main output file
        """
        super().__init__(file_descriptor, parent)
        # inject header line into the ChunkParser class
        self._initial_chunk = _get_parser(self._available_parsers[self.initial_chunk],
                                          header_line)

    def parse(self) -> dict:
        """ Parses the output file by dividing it into chunks, and then parsing them separately

        Returns
        -------
            a parsed dictionary
        """
        self.fd.seek(0)
        # instantiate ChunkParser with header line already injected
        current_chunk = self._initial_chunk(self.fd, parent=self)
        # can we create the `parse_results` structure preliminary?
        parse_results = {}
        while current_chunk:
            chunk_results = current_chunk.parse()
            if chunk_results or current_chunk.parsed_key:
                update(parse_results, chunk_results, current_chunk.parsed_key)
            if current_chunk.next is None:
                break
            current_chunk = current_chunk.next(self.fd, parent=self)
        self.result = parse_results
        return self.result

    def annotate(self, annotated_file: str | Path | IO = None) -> None:
        """Annotates the output file by adding the chunk name and ID to each line.

        Parameters
        ----------
        annotated_file: str | Path | IO
            The name of the file to write annotations to.
            If None, write the annotated file to stdout.
        """
        self.fd.seek(0)
        if isinstance(annotated_file, str | Path):
            annotated_fd = open(annotated_file, "w")
        else:
            annotated_fd = annotated_file
        current_chunk = self._initial_chunk(self.fd, parent=self)
        while current_chunk:
            current_chunk.annotate(annotated_fd)
            if current_chunk.next is None:
                break
            current_chunk = current_chunk.next(self.fd, parent=self)
        if isinstance(annotated_fd, IO):
            annotated_fd.close()


class ChunkParser(Parser):
    """ An abstract class for the output file chunks

    Attributes
    ----------
    name : str
        the name of the section in the parse results
    values : dict[str, Any]
        the dict of the names and regular expressions that may be found in the
        chunk
    next_chunks : list[str | dict]
        the collection of lines and runtime choices that define the next chunk

    Parameters
    ----------
    file_descriptor : str | Path | IO
        an open output file descriptor
    """
    title_line: str = ""
    parsed_key: str = ""
    values: dict[str, Any] = {}
    metadata: dict[str, Any] = {}
    next_chunks: list[str | dict[str, Any]] = []

    def __init__(self,
                 file_descriptor: str | Path | IO,
                 parent: Parser  = None,
                 header_line: str = None) -> None:

        super().__init__(file_descriptor, parent)
        self.header_line = header_line
        self.uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        self._next_parsers = ParsersList(
            self.next_chunks,
            self._available_parsers,
            self.run_metadata
        )

    def _check_for_next(self, line):
        """ Decides on the chunk which a given line of the output should
        belong to.

        Parameters
        ----------
        line : str
            a line of the output file
        Returns
        -------
            None if the line belongs to this chunk; a FileChunk class if it belongs
            to another chunk
        """

        # find the next parser by comparing the line with the given regex
        next_parsers = self._next_parsers.process_line(line)
        for parser_meta in next_parsers:
            line_regex = parser_meta["line"]
            if re.search(line_regex, line):
                return _get_parser(parser_meta.get("parser", None), header_line=line)
        return None

    def collect(self):
        """ Collects all lines belonging to this chunk
        """
        lines = [self.header_line] if self.header_line is not None else []
        while line := self.fd.readline():
            next_chunk = self._check_for_next(line)
            if next_chunk is not None:
                self.next = next_chunk
                break
            lines.append(line)

        # TODO: Here check if the output file is actually complete!
        return "".join(lines)

    def parse(self) -> dict:
        """Generic parsing of the output file chunk"""
        line = self.collect()
        parse_result = {}
        # 1. values parsing
        for k, v in self.values.items():
            if not inspect.isfunction(v):
                v = to_str(v)
            # bring metadata to converter function; useful for parser variables
            match = v(line, self.run_metadata)
            if match is not None:
                parse_result[k] = match  # the first parenthesized subgroup
        # 2. metadata parsing
        for k, v in self.metadata.items():
            if not inspect.isfunction(v):
                v = to_str(v)
            match = v(line, self.run_metadata)
            if match is not None:
                self.parent.run_metadata[k] = match  # the first parenthesized subgroup
        # 3. warnings and errors parsing (ones that begin with optional space and asterisk)
        self.parent.errors += re.findall(r"^(?: ?\*.*\n)+[\s\n]*\Z", line, re.MULTILINE)
        self.parent.warnings += re.findall(r"^(?: ?\*.*\n)+", line, re.MULTILINE)
        self.result = parse_result
        return self.result

    def annotate(self, annotated_file: IO) -> None:
        """Annotates the given chunk"""
        line = self.collect()
        # metadata parsing
        for k, v in self.metadata.items():
            if not inspect.isfunction(v):
                v = to_str(v)
            match = v(line, self.run_metadata)
            if match is not None:
                self.parent.run_metadata[k] = match  # the first parenthesized subgroup
        # get annotation and annotate
        truncated_name = self.name if len(self.name) < 15 else self.name[:12] + "..."
        annotation = f"{truncated_name:>15s}:{self.uuid}"
        annotated_lines = [f"{annotation} -> {el}" for el in line.split("\n")]
        if isinstance(annotated_file, IO):
            annotated_file.write("\n".join(annotated_lines))
        else:
            print("\n".join(annotated_lines), end="")


class ParsersList:
    def __init__(
            self,
            parsers_meta: list[str | dict[str, Any]],
            available_parsers: dict[str, Type[ChunkParser]],
            runtime_choices: dict[str, str]):
        """ A class representing a list of parser metadata

        Parameters
        ----------
        parsers_meta:
            a list of next chunk parsers' metadata
        available_parsers:
            a dictionary of all available parsers
        runtime_choices:

        """
        self._all_parsers = []
        for parser_meta in parsers_meta:
            # parser_meta is just a parser name
            if not isinstance(parser_meta, dict):
                parser_meta = {"chunk": parser_meta}

            parser_name = parser_meta["chunk"]
            if "line_present" in parser_meta:
                # the first string in `chunk` entry is the parser name to be used
                # when the line is present in the chunk; the second is used in the opposite case
                assert isinstance(parser_name, (list, tuple)) and len(parser_name) == 2
                yes_parser, no_parser = parser_name
                next_parser: dict[str, str | bool | dict] = {
                    "line_present": parser_meta["line_present"],
                    "found": False,
                    "parsers": {
                        True: {
                            "line": available_parsers[yes_parser].title_line,
                            "parser": available_parsers[yes_parser],
                        },
                        False: {
                            "line": available_parsers[no_parser].title_line,
                            "parser": available_parsers[no_parser],
                        }
                    }
                }
            else:
                next_parser: dict[str, str | bool | dict] = {
                    "line": available_parsers[parser_name].title_line,
                    "parser": available_parsers[parser_name],
                }
                if "runtime_choices" in parser_meta:
                    next_parser["runtime_choices"] = parser_meta["runtime_choices"]
            self._all_parsers.append(next_parser)
        self._on_parsers = self.process_runtime_choices(runtime_choices)

    def process_runtime_choices(self, runtime_choices):
        """Remove the parsers from the list based on runtime choices of the calculation"""
        # First, throw away all the parsers from all parsers' list based on the runtime choices
        # Second, turn off all the `line_present` parsers
        all_parsers = []
        on_parsers = []
        for parser in self._all_parsers:
            if "line_present" in parser:
                all_parsers.append(parser)
                on_parsers.append(parser["parsers"][False])
                continue

            parser_choices = parser.get("runtime_choices", {})
            on_parser = True
            for choice, value in parser_choices.items():
                # boolean: check only for the existence of the key
                if isinstance(value, bool) and ((choice in runtime_choices) != value):
                    on_parser = False
                elif not isinstance(value, bool) and runtime_choices.get(choice, None) != value:
                    on_parser = False
            if on_parser:
                all_parsers.append(parser)
                on_parsers.append(parser)
        self._all_parsers = all_parsers
        return on_parsers

    def process_line(self, line):
        """Change parsers set based on the line from the output file"""
        on_parsers = []
        for parser in self._all_parsers:
            if "line_present" in parser:
                if not parser["found"]:
                    line_regex = parser["line_present"]
                    parser["found"] = bool(re.search(line_regex, line))
                on_parsers.append(parser["parsers"][parser["found"]])
                continue
            on_parsers.append(parser)
        return on_parsers

    def __iter__(self):
        for parser in self._on_parsers:
            yield parser
