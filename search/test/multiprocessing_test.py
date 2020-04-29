import multiprocessing as mp

class Somma:

    def do_somma(self, a, b, out):
        somma = a+b
        out.append(somma)
        return somma

    def run(self, a, b, out):
        p = mp.Process(target=self.do_somma, args=(1, 2, out))
        p.start()
        p.join()

if __name__ == '__main__':
    o = Somma()
    manager = mp.Manager()
    shared_out = manager.list()
    o.run(1,2, shared_out)

    assert shared_out.pop() == 3