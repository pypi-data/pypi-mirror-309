import pytest
from unittest.mock import patch

from ara_cli.ara_command_action import read_action


class MockArgs:
    def __init__(self, classifier, parameter, read_mode):
        self.classifier = classifier
        self.parameter = parameter
        self.read_mode = read_mode


@pytest.fixture
def mock_classifier():
    with patch('ara_cli.classifier.Classifier') as mock:
        yield mock


@pytest.fixture
def mock_file_classifier():
    with patch('ara_cli.file_classifier.FileClassifier') as mock:
        yield mock


@pytest.fixture
def mock_artefact_reader():
    with patch('ara_cli.artefact_reader.ArtefactReader') as mock:
        yield mock


@pytest.mark.parametrize("content, file_path, expected_exception", [
    ("content", "/path/to/file", None),  # No exception expected
    (None, None, ValueError),  # Expect ValueError when content is None
])
def test_read_action_no_branch(mock_artefact_reader, mock_classifier, content, file_path, expected_exception, capsys):
    mock_artefact_reader.read_artefact.return_value = (content, file_path)
    mock_classifier.get_artefact_title.return_value = "TestTitle"

    args = MockArgs(classifier='test_classifier', parameter='test_parameter', read_mode=None)

    if expected_exception:
        with pytest.raises(expected_exception):
            read_action(args)
    else:
        read_action(args)
        captured = capsys.readouterr()
        assert "    Content:\n      content\n" in captured.out
