import ast
import os
import random


class Seed:
    def __init__(self, args):
        self._seed = args.get("seed")
        self._output_seed = args.get("output_seed", False)
        self._filepath = args["filepath"]

        if self._seed and os.path.isfile(self._seed):
            filename = self._seed
            with open(filename, encoding="UTF-8") as fd:
                state = fd.read()
            state = ast.literal_eval(state)
            random.setstate(state)
        else:
            random.seed(self._seed)
        self._saved_state = random.getstate()

    def __del__(self):
        if not self._output_seed:
            return
        filename = self._filepath + ".seed"
        with open(filename, mode="w", encoding="UTF-8") as fd:
            fd.write(str(self._saved_state))
