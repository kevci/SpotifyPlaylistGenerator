import argparse

parser = argparse.ArgumentParser(description='Generate a Spotify playlist for today')
parser.add_argument('-artists', action='append')
parser.add_argument('-albums', action='append')
parser.add_argument('-tracks', action='append')

args = parser.parse_args()

