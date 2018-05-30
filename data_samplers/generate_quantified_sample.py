# /usr/bin/env python
import argparse
import json
import os
import sys
import random

# The purpose of this script is to attempt to create a representative sample
# JSON tracking log sample.

# First argument is the name of the tracking log JSON file to read
# Second (optional) argument is the name of the output file to write
# the generated sample.
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate tracking log samples for testing MLQ by selecting '
                                     'all events of a group of sample users.')
    parser.add_argument("-s", action="store", default=10, type=int, dest="num_sample_user",
                        help='number of sample users, default is 10')
    parser.add_argument('-f', action='store', dest='filename', help='path of original tracking log file')
    parser.add_argument('-o', action='store', default='outfile.json', dest='outfile_name',
                        help='path to store tracking log sample, default is outfile.json')
    num_sample_users = parser.parse_args().num_sample_user
    filename = parser.parse_args().filename
    outfile_name = parser.parse_args().outfile_name
    if num_sample_users <= 0:
        print('Number of samples cannot be non-positive.')
    if filename is None or filename == '':
        print('No filename supplied.')
        exit(1)
    if not os.path.isfile(filename):
        print('File %s does not exist.' % filename)
        exit(1)

    # collect sample users list
    sample_users = []
    with open(filename) as f:
        for line in f:
            # Use a random filter to avoid always
            # select the same group of sample users
            if random.random() > 0.02:
                continue
            json_line = json.loads(line)
            if len(sample_users) >= num_sample_users:
                break
            if (json_line[u'username'] not in sample_users
                and
                json_line[u'username'] != u''):
                sample_users.append(json_line[u'username'])

    print('Sample user list: %s' % str(sample_users))
    num_lines = sum(1 for line in open(filename))

    sample = []
    progress = 0.0
    print('')
    with open(filename) as f:
        for l, line in enumerate(f):
            json_line = json.loads(line)
            if json_line[u'username'] in sample_users:
                if float(l)/num_lines - progress > 0.01:
                    print('Progress:%d / %d = %.4f%%' % (l, num_lines, float(l)/num_lines))
                    sys.stdout.write("\033[F")
                    progress = float(l)/num_lines
                sample.append(json_line)
    print('\n')
    print("Generated sample has %d lines" % len(sample))

    with os.fdopen(
            os.open(outfile_name, os.O_CREAT | os.O_TRUNC | os.O_WRONLY),
            'w') as outfile:
        for line in sample:
            encoded_json_line = "%s\n" % json.dumps(line)
            outfile.write(encoded_json_line)