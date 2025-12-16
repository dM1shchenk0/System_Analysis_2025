from typing import List, Tuple, Dict, Set
import math

def task(s: str, e: str) -> Tuple[float, float]:
    def build_relations(s: str, e: str):
        edges = [tuple(map(int, line.split(','))) for line in s.strip().split('\n')]
        nodes = sorted(set([u for u, v in edges] + [v for u, v in edges]))
        n = max(nodes)
        
        r1 = [[False]*n for _ in range(n)]  # непосредственное управление
        r2 = [[False]*n for _ in range(n)]  # непосредственное подчинение
        r3 = [[False]*n for _ in range(n)]  # опосредованное управление
        r4 = [[False]*n for _ in range(n)]  # опосредованное подчинение
        r5 = [[False]*n for _ in range(n)]  # соподчинение
        
        children: Dict[int, List[int]] = {}
        parent: Dict[int, int] = {}
        for u, v in edges:
            r1[u-1][v-1] = True
            r2[v-1][u-1] = True
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
                    if not r1[a-1][b-1]:
                        r3[a-1][b-1] = True  # опосредованное управление
                        r4[b-1][a-1] = True  # опосредованное подчинение
                # соподчинение
                if parent.get(a) == parent.get(b) and a != b:
                    r5[a-1][b-1] = True
        
        return r1, r2, r3, r4, r5, nodes
    
    r1, r2, r3, r4, r5, nodes = build_relations(s, e)
    n = len(nodes)
    max_connections = n - 1
    total_entropy = 0.0
    
    for element in nodes:
        element_entropy = 0.0
        relations = [r1, r2, r3, r4, r5]
        for relation in relations:
            l_ij = sum(1 for j in range(len(relation[element-1])) if relation[element-1][j])
            
            if l_ij > 0:
                P = l_ij / max_connections
                H = -P * math.log2(P)
                element_entropy += H
        
        total_entropy += element_entropy
    # H_ref(n, k) = c * n * k
    c = 1 / (math.e * math.log(2))
    k = 5  # количество типов отношений
    H_ref = c * n * k
    
    normalized_complexity = total_entropy / H_ref if H_ref > 0 else 0.0
    
    entropy_rounded = round(total_entropy, 1)
    complexity_rounded = round(normalized_complexity, 1)
    
    return entropy_rounded, complexity_rounded


if __name__ == "__main__":
    test_data = """1,2
1,3
3,4
3,5"""
    
    result = task(test_data, "1")
    print("Результат для тестовых данных:")
    print(f"Энтропия: {result[0]}")
    print(f"Структурная сложность: {result[1]}")
