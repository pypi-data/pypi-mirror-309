from . import constants as C
from .dungeon import IDungeon


class Tree(IDungeon):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)

        self._output_tree = self.args.get("output_tree", C.DEFAULT_OUTPUT_TREE)

    def save(self):
        if not self._output_tree:
            return

        # The following imports are slow, so move them here in case
        # graph is not to be created
        # pylint: disable=import-outside-toplevel
        import matplotlib.pyplot as plt
        import networkx as nx

        filename = self.args["filepath"] + ".tree.png"

        graph = nx.from_edgelist(self.room_tree)
        layout = nx.spring_layout(graph, seed=0)
        nx.draw(graph, pos=layout, with_labels=True, font_weight="bold")
        plt.savefig(filename)
