#!/usr/bin/env python
'''
Generate a CFG (control-flow graph) of the full pipe execution trace.
Requires pycallgraph and graphviz to be installed and full pipe to be configured correctly.
It is recommended to be executed on a sample of course data due to the significant increase in processing time.
'''

import pycallgraph
import full_pipe


def generate_cfg(out_path):
    '''
    Writes the graphviz generated CFG to out_path.
    Only includes modules from full_pipe, edx_pipe, and curation.
    '''
    config = pycallgraph.Config(max_depth=4)
    config.trace_filter = pycallgraph.GlobbingFilter(
        include=['curation.*', 'edx_pipe.*', 'full_pipe.*'])
    graphviz = pycallgraph.output.GraphvizOutput(output_file=out_path)
    with pycallgraph.PyCallGraph(output=graphviz, config=config):
        full_pipe.main()

if __name__ == '__main__':
    generate_cfg('full_pipe_cfg.png')
