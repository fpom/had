import argparse, sys

from . import getopt, HadError

parser = argparse.ArgumentParser(prog="had",
                                 description="generate C compiler options from headers")
parser.add_argument("-a", "--actual", default=False, action="store_true",
                    help="extract only actually used headers")
parser.add_argument("-c", "--cc", type=str, default="gcc",
                    choices=("gcc", "clang"),
                    help="C compiler (default 'gcc')")
parser.add_argument("-D", metavar="MACRO", dest="macro", default=[], action="append",
                    help="define macro for the C preprocessor (useful with -a)")
parser.add_argument("-p", "--platform", type=str, default=None,
                    help="platform for which options are generated (default autodetect)")
parser.add_argument("--cflags", default=False, action="store_true",
                    help="output preprocessor and compiler options")
parser.add_argument("--lflags", default=False, action="store_true",
                    help="output linker options")
parser.add_argument("sources", metavar="FILE", type=str, nargs="+",
                    help="C files to be parsed for '#include's")

def main (argv=None) :
    args = parser.parse_args(argv)
    if args.platform is None :
        args.platform = sys.platform
    if not (args.lflags or args.cflags) :
        args.lflags = True
    try :
        lflags, cflags = getopt(args.sources, args.platform.lower(),
                                args.cc.lower(), args.macro, args.actual)
        print(" ".join((lflags if args.lflags else set())
                       | (cflags if args.cflags else set())))
    except HadError as err :
        parser.exit(1, f"{parser.prog}: {err}\n")

if __name__ == "__main__" :
    main()

