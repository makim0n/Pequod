#!/usr/bin/python3

from docker_analysis import *
from docker_args import *

if __name__ == "__main__":
    args=arguments_menu()
    main_analysis = dockerAnalysis(args.container)
    if args.item:
        #print(main_analysis.read_config())
        main_analysis.search_items(args.item)
    if args.extract:
        main_analysis.extract_file(args.extract)
