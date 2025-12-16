from typing import List, Tuple, Dict, Set


def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:
    edges = [tuple(map(int, line.split(','))) for line in s.strip().split('\n')]
    nodes = sorted(set([u for u, v in edges] + [v for u, v in edges]))
    n = max(nodes)

    r1 = [[False] * n for _ in range(n)]  # непосредственное управление
    r2 = [[False] * n for _ in range(n)]  # непосредственное подчинение
    r3 = [[False] * n for _ in range(n)]  # опосредованное управление
    r4 = [[False] * n for _ in range(n)]  # опосредованное подчинение
    r5 = [[False] * n for _ in range(n)]  # соподчинение

    children: Dict[int, List[int]] = {}
    parent: Dict[int, int] = {}
    for u, v in edges:
        r1[u - 1][v - 1] = True
        r2[v - 1][u - 1] = True
        children.setdefault(u, []).append(v)
        parent[v] = u

    root = int(e)

    ancestors: Dict[int, Set[int]] = {node: set() for node in nodes}

    def dfs(node, current_ancestors):
        for child in children.get(node, []):
            ancestors[child] = current_ancestors | {node}
            dfs(child, ancestors[child])

    dfs(root, set())

    for a in nodes:
        for b in nodes:
            if a == b:
                continue
            if a in ancestors[b]:
                if not r1[a - 1][b - 1]:
                    r3[a - 1][b - 1] = True  # опосредованное управление
                    r4[b - 1][a - 1] = True  # опосредованное подчинение
            # соподчинение
            if parent.get(a) == parent.get(b) and a != b:
                r5[a - 1][b - 1] = True

    return r1, r2, r3, r4, r5


s = ""
with open(r"C:\Users\vadim\System_Analysis\task1\task2.csv", 'r', encoding='utf-8') as f:
    s = f.read().strip()
print(main(s, "1")[4])