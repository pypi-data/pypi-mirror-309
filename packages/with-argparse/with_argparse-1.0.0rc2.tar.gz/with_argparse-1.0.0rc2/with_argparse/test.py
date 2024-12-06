from argparse import ArgumentParser

args = ArgumentParser()
args.add_argument("--test", type=bool, action="store_true")

print(args.parse_args())