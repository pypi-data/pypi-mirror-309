import pytest
import winzy_win_geometry as w

from argparse import Namespace, ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(['-t', 'hello'])
    assert result.title == "hello"

    result = parser.parse_args([])
    assert result.title is None

def test_plugin(capsys):
    w.wingeo_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
