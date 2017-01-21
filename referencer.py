# -*- coding: utf-8 -*-
import argparse
from configparser import RawConfigParser
import os
from redmine import Redmine
from subprocess import call
from utils import prompt, prompt_yes_no


class ReferencerConfiguration(object):

    def __init__(self, path, repository):
        self.path = path
        self.repository = repository
        self._config = RawConfigParser()
        self._refresh()

    def _refresh(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as config_file:
                self._config.read_file(config_file)

    def get(self, key):
        return self._config[self.repository][key]

    def set(self, key, value):
        if self.repository not in self._config:
            self._config[self.repository] = {}
        self._config[self.repository][key] = value
        with open(self.path, 'w') as config_file:
            self._config.write(config_file)
        self._refresh()

    @property
    def repository_configuration_exists(self):
        return self.repository in self._config


class Referencer(object):

    CONFIG_FILE_PATH = os.path.expanduser('~/.referencerrc')

    def __init__(self):
        self._repository_root = self._find_repository_root(os.getcwd())
        self._config = ReferencerConfiguration(self.CONFIG_FILE_PATH,
                                               self._repository_root)

    def _find_repository_root(self, path):
        """Find the root of the git repository containing the given path."""
        git_directory = os.path.join(path, '.git')
        if os.path.isdir(git_directory):
            return path
        else:
            return self.find_repository_root(os.path.dirname(path))

    def run(self, commit_file):
        repository_root = self._find_repository_root(os.getcwd())
        if not self._config.repository_configuration_exists:
            self._configure_for_repository(repository_root)
        # Create the initial message.
        editor = os.environ['EDITOR']
        call([editor, commit_file])

    def _configure_for_repository(self, repository_root):
        """Configure referencer for the specified repository."""
        use_referencer = prompt_yes_no('Use referencer for this repo?',
                                       default=True)
        if use_referencer:
            self._config.set('installation', prompt(
                'Redmine installation URL (e.g. http://demo.redmine.org)'))
            self._config.set('key', prompt('API key', password=True))
            self._config.set('slug', prompt('Project slug'))
        else:
            self._config.set('disable', True)


def main():
    # Set up the argument parser.
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the path to a commit message file')
    args = parser.parse_args()

    referencer = Referencer()
    referencer.run(args.file)

if __name__ == '__main__':
    main()
