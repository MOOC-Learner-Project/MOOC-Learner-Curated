# /usr/bin/env python
"""
(smart) Synthetic data generator
author: John Ding johnding1996@hotmail.com

The purpose of this script is to attempt to create synthetic JSON tracking logs
that are equally good to test through the apipe and qpipe of MLC.
It can also generates synthetic course files that can be used to test the extension pipes.

This synthetic data generator, in contrast to the simple one, tries to generate synthetic data
by imitating real sensitive data. It hides the sensitive fields like username, ip, grades and process the
other fields. This approach makes the data as meaningful as the real one, so it can be used to test MLQ,
MLV and MLM as well. It is also possible to use learning models to generate synthetic data that is
statistically similar to the real one.

The argument after -c is the synthetic course name
The argument after -i is the input data folder path (it contains templates which are generated from real data)
The argument after -o is the output data folder path (it must already exists)
The argument after -n is the number of independent records of each synthetic files
Switch on vismooc_extensions file generator by flag -v
Switch on newmitx_extensions file generator by flag -m
"""
import argparse

# TODO: Build this smart synthetic data generator in the future


def gen_log():
    pass


def gen_vismooc():
    pass


def gen_newmitx():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate sample synthetic data to test MLC.')
    parser.add_argument("-c", action="store", default='synthetic', dest='course_name',
                        help='synthethic course name')
    parser.add_argument('-i', action='store', dest='in_path',
                        help='path to input template folder')
    parser.add_argument('-o', action='store', default='.', dest='out_path',
                        help='path to output data folder, default: the parent folder of MLC')
    parser.add_argument('-n', action='store', default=1000, type=int, dest='num_records',
                        help='number of records of all synthetic data files, default 1000')
    parser.add_argument('-v', action='store_true', default=False, dest='shall_gen_vismooc',
                        help='switch on to generate synthetic data files for vismooc extensions')
    parser.add_argument('-m', action='store_true', default=False, dest='shall_gen_newmitx',
                        help='switch on to generate synthetic data files for newmitx extensions')
    course_name = parser.parse_args().course_name
    in_path = parser.parse_args().in_path
    out_path = parser.parse_args().out_path
    num_records = parser.parse_args().num_records
    shall_gen_vismooc = parser.parse_args().shall_gen_vismooc
    shall_gen_newmitx = parser.parse_args().shall_gen_newmitx

    gen_log()

    if shall_gen_vismooc:
        gen_vismooc()
    if shall_gen_newmitx:
        gen_newmitx()