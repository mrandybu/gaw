import argparse

try:
    from src.base_funcs import BaseFuncs
except:
    from base_funcs import BaseFuncs


class Wrapper(object):
    def __init__(self):
        self.args = self.get_args()

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--path', action='store', help='path to file or dir')
        parser.add_argument('-a', '--action', action='store', help='[clone|rebuild|test]')
        parser.add_argument('args', action='store', help='parameters for action')

        args = parser.parse_args()
        return args

    def run(self):
        func = BaseFuncs(self.args.__dict__)
        set_args = func.set_args()
        if set_args is False:
            self.how_use()
            return
        print(set_args)

    @staticmethod
    def how_use():
        print('Use "--help"')


if __name__ == '__main__':
    Wrapper().run()
