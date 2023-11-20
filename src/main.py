import csv
import networkx as nx
import matplotlib.pyplot as plt
import click


def read_graph_from_csv(file_path: str) -> nx.classes.graph.Graph:
    """
    Read a csv file that contains the edge representation of a graph, return a networkx graph object.
    The edge representation of a graph is a list of edges, each edge is a pair of connected vertices,
    where each vertex is represented by an integer. The csv file should consist of n rows, each with a pair of
    space-separated integers that represent to neighboring nodes.
    """
    graph = nx.Graph()
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        next(reader)  # Skip the first line
        for row in reader:
            vertex1, vertex2 = map(int, row)
            graph.add_edge(vertex1, vertex2)
    return graph


def plot_graph(graph: nx.classes.graph.Graph, coloring: dict[int, int]) -> None:
    """Plot the graph and color the vertices."""
    pos = nx.kamada_kawai_layout(graph)
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=[coloring.get(node, 0) for node in graph.nodes()],
        cmap=plt.cm.rainbow,
    )
    plt.show()


def find_best_strategy(graph: nx.classes.graph.Graph) -> str:
    """
    Compute nx.coloring(graph, strategy) for all posible strategies,
    return the strategy that yields the smaller number of colors
    """
    possible_strategies = [
        "largest_first",
        "random_sequential",
        "smallest_last",
        "independent_set",
        "connected_sequential_bfs",
        "connected_sequential_dfs",
        "saturation_largest_first",
    ]

    for i, strategy in enumerate(possible_strategies):
        coloring = nx.coloring.greedy_color(graph, strategy=strategy)
        num_of_colors = max(coloring.values()) + 1
        if (i == 0) or (num_of_colors < min_num_of_colors):
            best_strategy = strategy
            min_num_of_colors = num_of_colors

    return best_strategy


def write_coloring_to_csv(
    file_path: str, coloring: dict[int, int], verbose: bool = True
) -> None:
    """Write coloring to csv file"""
    sorted_coloring = dict(
        [(vertex, coloring[vertex]) for vertex in sorted(coloring)]
    )  # sort dictionary by keys
    with open(file_path, "w") as file:
        writer = csv.writer(file, delimiter=" ")
        writer.writerow(["vertex", "color"])  # column names
        for vertex, color in sorted_coloring.items():
            writer.writerow([vertex, color])

    if verbose:
        print(f"Stored coloring data at {file_path}")


@click.command()
@click.option(
    "-r",
    "--read-graph-from",
    type=str,
    help="path of the csv file that contains the graph data",
)
@click.option(
    "-w",
    "--write-colors-to",
    type=str,
    help="path where you want to store the colors",
)
@click.option(
    "--plot",
    type=bool,
    default=False,
    help="plot the colored graph",
)
@click.option(
    "--verbose",
    type=bool,
    default=False,
    help="print the number of colors to screen",
)
def main(
    read_graph_from: str,
    write_colors_to: str,
    plot: bool = False,
    verbose: bool = False,
):
    """
    Usage: python3 main.py --read-graph-from FILE --write-colors-to FILE [--plot 1] [--verbose 1]\n
    Read graph from csv, color the graph, write the color data to a csv.
    File paths should be relative to the working directory, not to this script.
    """
    graph = read_graph_from_csv(read_graph_from)
    best_strategy = find_best_strategy(graph)
    coloring = nx.coloring.greedy_color(graph, strategy=best_strategy)
    write_coloring_to_csv(write_colors_to, coloring, verbose=verbose)

    if verbose:
        num_of_colors = max(coloring.values()) + 1
        print(f"Colored graph with {num_of_colors} colors")
    if plot:
        plot_graph(graph, coloring)


if __name__ == "__main__":
    main()
