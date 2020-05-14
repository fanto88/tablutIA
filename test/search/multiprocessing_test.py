import multiprocessing as mp
import os
from tablut.search.search import ParallelSearchMetric

metric = ParallelSearchMetric()

def run():
    metric.node_expandend += 1


if __name__ == '__main__':
    p = mp.Pool(4)

    p.apply(func=run)
    #assert shared_out.pop() == 3