#!/usr/bin/env python

import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='afusion',
        description='Afusion command line tool'
    )
    subparsers = parser.add_subparsers(
        dest='command',
        help='Sub-commands'
    )

    # Add the 'install' sub-command
    install_parser = subparsers.add_parser(
        'install', 
        help='Launch the installation GUI'
    )

    # Add the 'run' sub-command
    run_parser = subparsers.add_parser(
        'run', 
        help='Run the main application (Alphafold3 GUI)'
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.command == 'install':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..'))
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)

        app_path = os.path.join(root_dir, 'afusion/install.py')

        streamlit_command = [
            'streamlit', 'run', app_path,
            '--server.fileWatcherType=none'
        ] + sys.argv[2:]  # Skip the first two arguments ('afusion', 'install')
        os.execvp('streamlit', streamlit_command)

    elif args.command == 'run':
        # Run the main application (Alphafold3 GUI)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..'))
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)

        app_path = os.path.join('app.py')

        streamlit_command = [
            'streamlit', 'run', app_path,
            '--server.fileWatcherType=none'
        ] + sys.argv[2:]  # Skip the first two arguments ('afusion', 'run')
        os.execvp('streamlit', streamlit_command)

    else:
        # Handle other commands or display help information
        parser.print_help()

if __name__ == '__main__':
    main()

