import argparse
from modules import final
import threading


parser = argparse.ArgumentParser(prog='QR Test', usage='command.py [-h] sub',
                                 add_help=True)

parser.add_argument('-t', '--test', type=int)
args = parser.parse_args()

if __name__ == '__main__':
    first_part = ("01924939", "19032625", "01362152", "14828203", "03284023", "90173073")
    direct = "http://192.168.7.112:6090"
    proxy = "http://192.168.7.145:6010"
    first = threading.Thread(target=final, args=(first_part, proxy,), kwargs={'stop_func': args.test})
    second_part = ('90301498', '90301501', '90301530', '90301540', '90301543', '90301614')
    second = threading.Thread(target=final, args=(second_part, proxy,), kwargs={'stop_func': args.test})
    first.start()
    second.start()


