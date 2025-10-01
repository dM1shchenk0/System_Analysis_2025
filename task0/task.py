import csv
import sys


def solve(file_path):
    edges = []
    max_vertex_label = 0

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2:
                continue
            try:
                u, v = int(row[0]), int(row[1])
            except ValueError:
                continue
            edges.append((u, v))
            max_vertex_label = max(max_vertex_label, u, v)

    size = max_vertex_label
    matrix = [[0] * size for _ in range(size)]

    for u, v in edges:
        matrix[u - 1][v - 1] = 1

    return matrix


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task.py graph.csv")
    else:
        result = solve(sys.argv[1])

        for row in result:
            print(" ".join(map(str, row)))
