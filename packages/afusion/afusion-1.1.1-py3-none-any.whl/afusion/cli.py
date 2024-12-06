#!/usr/bin/env python

import os
import sys

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    
    app_path = os.path.join(root_dir, 'app.py')
    
    streamlit_command = [
        'streamlit', 'run', app_path,
        '--server.fileWatcherType=none'
    ] + sys.argv[1:]
    os.execvp('streamlit', streamlit_command)

if __name__ == '__main__':
    main()
