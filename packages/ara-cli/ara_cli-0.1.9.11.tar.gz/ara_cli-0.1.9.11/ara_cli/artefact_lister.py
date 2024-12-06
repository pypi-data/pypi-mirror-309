from ara_cli.file_classifier import FileClassifier
from ara_cli.template_manager import DirectoryNavigator
from ara_cli.artefact_reader import ArtefactReader
import os


class ArtefactLister:
    def __init__(self, file_system=None):
        self.file_system = file_system or os

    def list_files(self, tags=None, navigate_to_target=False):
        # make sure this function is always called from the ara top level directory
        navigator = DirectoryNavigator()
        if navigate_to_target:
            navigator.navigate_to_target()

        file_classifier = FileClassifier(self.file_system)
        classified_files = file_classifier.classify_files(tags=tags)
        file_classifier.print_classified_files(classified_files)

    def list_branch(self, classifier, artefact_name):
        file_classifier = FileClassifier(os)
        artefacts_by_classifier = {classifier: []}
        ArtefactReader.step_through_value_chain(
            artefact_name=artefact_name,
            classifier=classifier,
            artefacts_by_classifier=artefacts_by_classifier
        )
        file_classifier.print_classified_files(artefacts_by_classifier)

    def list_children(self, classifier, artefact_name):
        file_classifier = FileClassifier(os)
        child_artefacts = ArtefactReader.find_children(
                artefact_name=artefact_name,
                classifier=classifier
        )
        file_classifier.print_classified_files(
            files_by_classifier=child_artefacts
        )
