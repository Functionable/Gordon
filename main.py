##
##  Main file of the 'Gordon' project.
##

import sys
import gordon.core as gordon

def start_gordon_cli():
    # This will most likely end up being the output for the help option.
    print("gordon.py")
    print(" - A command line discord bot, sample description.")
    
    gordon.start_bot()
    
    pass

if __name__ == '__main__':
    start_gordon_cli()