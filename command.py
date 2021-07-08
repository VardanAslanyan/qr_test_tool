import argparse
from modules import final


parser = argparse.ArgumentParser(prog='QR Test', usage='command.py [-h] sub',
                                 add_help=True)

parser.add_argument('-t', '--test', type=int)
args = parser.parse_args()

if __name__ == '__main__':
    direct = "http://192.168.7.112:6090"
    proxy = "http://192.168.7.145:6010"
    final(proxy, stop_func=args.test)


