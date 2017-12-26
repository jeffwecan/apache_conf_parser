#!/usr/bin/env python


class ParserError(Exception):
    pass


class InvalidLineError(ParserError):
    pass


class NodeCompleteError(InvalidLineError):
    pass


class DirectiveError(ParserError):
    pass


class NestingLimitError(ParserError):
    pass


class NodeMatchError(ParserError):
    pass
