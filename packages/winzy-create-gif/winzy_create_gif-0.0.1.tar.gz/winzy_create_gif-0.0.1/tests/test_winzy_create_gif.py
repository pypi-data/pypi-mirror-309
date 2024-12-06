import pytest
import winzy_create_gif as w

from argparse import Namespace, ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(['*.png'])
    assert result.pattern == "*.png"
    assert result.output_file == "animation.gif"
    assert result.fps == 10


def test_plugin(capsys):
    w.gif_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
