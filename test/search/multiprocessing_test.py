import multiprocessing as mp
import os


class Somma:

    def __init__(self, workers_no):
        self.workers_no = workers_no
        self.shared = mp.Manager().dict()
        self.jobs = []

    def do_somma(self, a, b):
        somma = a+b
        self.shared[(a, b)] = somma
        print(os.getpid(), self.shared)

    def run(self):
        self.jobs = [mp.Process(target=self.do_somma, args=(a, a+1)) for a in range(self.workers_no)]
        [p.start() for p in self.jobs]
        [p.join() for p in self.jobs]


if __name__ == '__main__':
    o = Somma(4)
    o.run()
    print(o.shared)
    #assert shared_out.pop() == 3