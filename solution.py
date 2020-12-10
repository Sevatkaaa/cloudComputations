from Pyro4 import expose


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        n = self.read_input()
        step = int(len(n) / len(self.workers))

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            print("map %d" % i)
            if i == len(self.workers) - 1:
                mapped.append(self.workers[i].mymap(n, i * step, len(n)))
            else:
                mapped.append(self.workers[i].mymap(n, i * step, (i + 1) * step))

        # reduce
        pals = self.reduce_files(mapped)

        # output
        self.write_output(pals)

        print(len(pals))

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(x, f, t):
        affed = []
        for i in range(f, t):
            affed.append(chr(((5 * (ord(x[i]) - (ord('a'))) + 8) % 26) + ord('a')))
        return affed

    @staticmethod
    @expose
    def reduce_files(mapped):
        print("reduce")
        output = []

        for val in mapped:
            print("reduce loop")
            output = output + val.value
        print("reduce done")
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        n = str(f.readline())
        f.close()
        return n

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output.__len__()))
        f.write('\n')
        f.write(''.join(output))
        f.write('\n')
        f.close()
        print("output done")
