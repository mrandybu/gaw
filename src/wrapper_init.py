import sys

try:
    from src.base_func import BaseFunc
except:
    from base_func import BaseFunc


class Wrapper(object):
    def __init__(self):
        self.action, self.flags = self.parse_params()

    @staticmethod
    def parse_params():
        if len(sys.argv) < 3:
            return None, None
        return sys.argv[1], sys.argv[2:]

    def run(self):
        bs = BaseFunc(self.action, self.flags)
        return bs.set_args()


if __name__ == '__main__':
    print(Wrapper().run())
