import sys

try:
    from src.base_funcs import BaseFuncs
except:
    from base_funcs import BaseFuncs


class Wrapper(object):
    def __init__(self):
        self.action, self.flags = self.parse_params()

    def parse_params(self):
        if len(sys.argv) < 4:
            return None, None
        return sys.argv[1], sys.argv[2:]

    def run(self):
        func = BaseFuncs(self.action, self.flags)
        set_args = func.set_args()
        if set_args is False:
            self.how_use()
            return
        print(set_args)

    @staticmethod
    def how_use():
        print('Usage:')
        print('    $ gaw /action:/ [clone|rebuild|test|build] \n\
         /flags:/   [--all|--local|--remote] \n\
                    [--setall|--setlocal|--setremote]')


if __name__ == '__main__':
    Wrapper().run()
