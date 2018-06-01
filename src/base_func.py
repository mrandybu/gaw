import os
from __init__ import BASE_REPO
from subprocess import Popen, PIPE


class BaseFunc(object):
    def __init__(self, action, flags):
        self.action = action
        self.flags = flags

    def set_args(self):
        allow_args = {
            'clone': self.clone_repo,
            'rebuild': self.rebuild
        }
        # try:
        return allow_args[self.action](self.flags)
        # except:
        #   return 'args not allow'

    def clone(self, *args):
        return args[0]

    def rebuild(self, **kwargs):
        return kwargs

    @staticmethod
    def clone_repo(*args):
        pac_list_file = args[0][0]
        if not os.path.exists(pac_list_file):
            return 'err of exist'
        pac_list = []
        clone_param = args[0][1]
        try:
            with open(pac_list_file) as plf:
                for pac_name in plf:
                    pac_list.append(
                        (pac_name.split('\n'))[0]
                    )
        except IOError as err:
            print(err)
        clone_command = [['git clone'.split()], ['ssh git.alt clone'.split()]]
        if clone_param == '--local':
            clone_command = clone_command[0]
        elif clone_param == '--remote':
            clone_command = clone_command[1]
        for pac_name in pac_list:
            pac_name_git = pac_name + '.git'
            full_repo_path = os.path.join(BASE_REPO, pac_name[0], pac_name_git)
            for command in clone_command:
                command.append(full_repo_path)
                clone_repo = Popen(command, stdout=PIPE)
                command.remove(full_repo_path)
                print(clone_repo.stdout.read())
