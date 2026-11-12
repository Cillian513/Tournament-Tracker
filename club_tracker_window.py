import sys
#Attempt to import the server module from the club_tracker package 
try:
    from club_tracker.server import main
except ImportError as err:
    sys.exit(f"Couldn't load the club_tracker folder ({err})")
if __name__ == "__main__":
    main()
