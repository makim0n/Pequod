#!/usr/bin/python3

from docker_analysis import *
from docker_args import *

if __name__ == "__main__":
    args=arguments_menu()
    if args.container:
        main_analysis = dockerAnalysis(args.container)
        print(main_analysis.read_config())
