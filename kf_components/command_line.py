import argparse


def multiply():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", type=float)
    parser.add_argument("--b", type=float)
    args = parser.parse_args()
    print(args.a * args.b)
