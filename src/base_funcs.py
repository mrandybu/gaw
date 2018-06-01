import os
from subprocess import Popen, PIPE
import re

try:
    from src import BASE_REPO
except:
    from __init__ import BASE_REPO


class BaseFuncs(object):
    def __init__(self, action, flags):
        self.action = action
        self.flags = flags

    def set_args(self):
        allow_args = {
            'clone': self.clone_repo,
            'rebuild': self.rebuild
        }
        try:
            return allow_args[self.action](self.flags)
        except:
            return False

    def rebuild(self, **kwargs):
        return kwargs

    @staticmethod
    def clone_repo(*args):
        pac_list_file = args[0][0]
        if not os.path.exists(pac_list_file):
            return 'Path to file not exist!'
        pac_list = []
        clone_param = args[0][1]
        try:
            with open(pac_list_file) as plf:
                for pac_name in plf:
                    pac_list.append(
                        (pac_name.split('\n'))[0]
                    )
        except:
            return 'Open file error!'
        clone_command = [['git clone'.split()], ['ssh git.alt clone'.split()]]
        if clone_param == '--local':
            clone_command = clone_command[0]
        elif clone_param == '--remote':
            clone_command = clone_command[1]
        elif clone_param == '--all':
            clone_command = clone_command
        else:
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

    def find_spec(self, dir_):
        dir_list = Popen(['ls', '-a', dir_], stdout=PIPE)
        grep_dir = Popen(['grep', '.git'], stdin=dir_list.stdout, stdout=PIPE)
        git = grep_dir.stdout.read().decode('utf-8')
        if len(git) != 0:
            def read_spec(spec_file):
                try:
                    spec_path = (spec_file.stdout.read().decode('utf-8').split('\n'))[0]
                    changelog = self.get_changelog(spec_path)
                    return changelog
                except:
                    pass

            gear_dir = os.path.join(dir_, '.gear')
            if os.path.exists(gear_dir):
                gear_spec = Popen(['find', gear_dir, '-name', '*.spec'], stdout=PIPE)
                changelog_line = read_spec(gear_spec)
                if changelog_line is not None:
                    return changelog_line
            dir_spec = Popen(['find', dir_, '-name', '*.spec'], stdout=PIPE)
            changelog_line = read_spec(dir_spec)
            if changelog_line is not None:
                return changelog_line
        dir_list = Popen(['ls', dir_], stdout=PIPE) \
            .stdout.read().decode('utf-8').split('\n')

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
            return 'Parse changelog error!'
        return ' '.join(changelog_list[delimiters[0]:delimiters[1]])


if __name__ == '__main__':
    bs = BaseFuncs('qwe', 'asd')
    print(bs.find_spec('/home/mrdrew/git_clone'))
