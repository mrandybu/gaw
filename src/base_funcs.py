import os
from subprocess import Popen, PIPE
import re

try:
    from src import BASE_REPO
except:
    from __init__ import BASE_REPO


class BaseFuncs(object):
    def __init__(self, args):
        self.path = args['path']
        self.action = args['action']
        self.args = args['args']

    def set_args(self):
        allow_args = {
            'clone': self.clone_repo,
            'rebuild': self.rebuild
        }
        try:
            return allow_args[self.action](self.path, self.args)
        except:
            return False

    def rebuild(self, **kwargs):
        return kwargs

    @staticmethod
    def clone_repo(path, param):
        if not os.path.exists(path):
            return 'Path to file not exist!'
        pac_list = []
        try:
            with open(path) as plf:
                for pac_name in plf:
                    pac_list.append(
                        (pac_name.split('\n'))[0]
                    )
        except:
            return 'Open file error!'
        clone_command = [['git clone'.split()], ['ssh git.alt clone'.split()]]
        params = {
            'local': clone_command[0],
            'remote': clone_command[1],
            'all': clone_command
        }
        try:
            clone_command = params[param]
        except:
            return False
        for pac_name in pac_list:
            pac_name_git = pac_name + '.git'
            full_repo_path = os.path.join(BASE_REPO, pac_name[0], pac_name_git)
            for command in clone_command:
                if len(command) < 2:
                    command = command[0]
                command.append(full_repo_path)
                clone_repo = Popen(command, stdout=PIPE)
                command.remove(full_repo_path)
                clone_repo.stdout.read()

    def _find_in_git_dir(self, dir_pac):
        def read_spec(spec_file):
            try:
                spec_path = (spec_file.stdout.read().decode('utf-8').split('\n'))[0]
                changelog = self.get_changelog(spec_path)
                return changelog
            except:
                pass

        gear_dir = os.path.join(dir_pac, '.gear')
        if os.path.exists(gear_dir):
            gear_spec = Popen(['find', gear_dir, '-name', '*.spec'], stdout=PIPE)
            changelog_line = read_spec(gear_spec)
            if changelog_line is not None:
                return changelog_line
        dir_spec = Popen(['find', dir_pac, '-name', '*.spec'], stdout=PIPE)
        changelog_line = read_spec(dir_spec)
        if changelog_line is not None:
            return changelog_line

    def find_spec(self, dir_):
        dir_list = Popen(['ls', '-a', dir_], stdout=PIPE)
        grep_dir = Popen(['grep', '.git'], stdin=dir_list.stdout, stdout=PIPE)
        git = grep_dir.stdout.read().decode('utf-8')
        if len(git) != 0:
            get_spec = self._find_in_git_dir(dir_)
            return get_spec

        dir_list = Popen(['ls', dir_], stdout=PIPE) \
            .stdout.read().decode('utf-8').split('\n')
        spec_list = []
        for _dir in dir_list:
            if len(_dir) != 0:
                get_spec = self._find_in_git_dir(
                    os.path.join(dir_, _dir)
                )
                if (get_spec is not None) & (get_spec is not False):
                    spec_list.append([_dir, get_spec])

        return spec_list

    @staticmethod
    def get_changelog(spec):
        with open(spec) as spec:
            spec_content = spec.read()
        changelog = re.split('%changelog', spec_content)
        changelog_list = changelog[1].split()
        if len(changelog) == 0:
            return 'Parse changelog error!'
        del changelog_list[0]
        delimiters = []
        for sym in changelog_list:
            if sym == '-':
                delimiters.append(changelog_list.index(sym))
            if sym == '*':
                delimiters.append(changelog_list.index(sym))
                break
        if len(delimiters) != 2:
            return False
        return ' '.join(changelog_list[delimiters[0]:delimiters[1]])
