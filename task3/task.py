import json
import re
from typing import List, Set, Dict


def flatten_ranking(ranking: List) -> List[int]:
    result = []
    for item in ranking:
        if isinstance(item, int):
            result.append(item)
        elif isinstance(item, list):
            result.extend(flatten_ranking(item))
    return result


def get_clusters(ranking: List) -> Dict[int, Set[int]]:
    clusters = {}
    all_elements = set(flatten_ranking(ranking))
    
    for elem in all_elements:
        clusters[elem] = {elem}
    
    for item in ranking:
        if isinstance(item, list):
            cluster_elems = set(flatten_ranking([item]))
            for elem in cluster_elems:
                clusters[elem] = clusters[elem] | cluster_elems
    
    return clusters


def get_positions(ranking: List) -> Dict[int, int]:
    positions = {}
    pos = 0
    for item in ranking:
        if isinstance(item, int):
            positions[item] = pos
            pos += 1
        elif isinstance(item, list):
            elems = flatten_ranking([item])
            for elem in elems:
                positions[elem] = pos
            pos += 1
    return positions


def build_consensus_ranking(ranking_a: List, ranking_b: List) -> List:
    all_elements = set(flatten_ranking(ranking_a)) | set(flatten_ranking(ranking_b))
    
    clusters_a = get_clusters(ranking_a)
    clusters_b = get_clusters(ranking_b)
    
    positions_a = get_positions(ranking_a)
    positions_b = get_positions(ranking_b)
    
    precedence = {}
    for elem in all_elements:
        precedence[elem] = set()
    
    for elem1 in all_elements:
        for elem2 in all_elements:
            if elem1 == elem2:
                continue
            pos1_a = positions_a.get(elem1, len(all_elements))
            pos2_a = positions_a.get(elem2, len(all_elements))
            pos1_b = positions_b.get(elem1, len(all_elements))
            pos2_b = positions_b.get(elem2, len(all_elements))
            
            if pos1_a < pos2_a and pos1_b < pos2_b:
                precedence[elem1].add(elem2)
    
    def topological_sort():
        in_degree = {elem: 0 for elem in all_elements}
        for elem in all_elements:
            for successor in precedence[elem]:
                in_degree[successor] += 1
        
        queue = [elem for elem in all_elements if in_degree[elem] == 0]
        result_order = []
        
        while queue:
            queue.sort(key=lambda e: (positions_a.get(e, len(all_elements)) + 
                                     positions_b.get(e, len(all_elements))) / 2)
            elem = queue.pop(0)
            result_order.append(elem)
            
            for successor in precedence[elem]:
                in_degree[successor] -= 1
                if in_degree[successor] == 0:
                    queue.append(successor)
        
        return result_order
    
    ordered_elements = topological_sort()
    
    result = []
    i = 0
    while i < len(ordered_elements):
        current_cluster = [ordered_elements[i]]
        j = i + 1
        
        while j < len(ordered_elements):
            candidate = ordered_elements[j]
            can_cluster = False
            
            cluster_a_i = clusters_a.get(current_cluster[0], {current_cluster[0]})
            cluster_b_i = clusters_b.get(current_cluster[0], {current_cluster[0]})
            cluster_a_j = clusters_a.get(candidate, {candidate})
            cluster_b_j = clusters_b.get(candidate, {candidate})
        
            if (candidate in cluster_a_i and candidate in cluster_b_i and
                current_cluster[0] in cluster_a_j and current_cluster[0] in cluster_b_j):
                can_cluster = True
            else:
                pos_prev_a = positions_a.get(current_cluster[-1], len(all_elements))
                pos_cand_a = positions_a.get(candidate, len(all_elements))
                pos_prev_b = positions_b.get(current_cluster[-1], len(all_elements))
                pos_cand_b = positions_b.get(candidate, len(all_elements))
                
                if (pos_prev_a < pos_cand_a and pos_prev_b > pos_cand_b) or \
                   (pos_prev_a > pos_cand_a and pos_prev_b < pos_cand_b):
                    can_cluster = True
            
            if can_cluster:
                current_cluster.append(candidate)
                j += 1
            else:
                break
        
        if len(current_cluster) == 1:
            result.append(current_cluster[0])
        else:
            result.append(sorted(current_cluster))
        i = j
    
    return result


def find_contradiction_core(ranking_a: List, ranking_b: List, 
                           consensus: List) -> List:
    clusters_a = get_clusters(ranking_a)
    clusters_b = get_clusters(ranking_b)
    
    contradiction_clusters = []
    
    for item in consensus:
        if isinstance(item, list):
            cluster_elems = set(item)
            was_together_in_a = False
            was_together_in_b = False

            for elem in cluster_elems:
                cluster_a = clusters_a.get(elem, {elem})
                if cluster_elems.issubset(cluster_a):
                    was_together_in_a = True
                    break
            
            for elem in cluster_elems:
                cluster_b = clusters_b.get(elem, {elem})
                if cluster_elems.issubset(cluster_b):
                    was_together_in_b = True
                    break
            
            if not (was_together_in_a and was_together_in_b):
                contradiction_clusters.append(sorted(list(cluster_elems)))
    
    if contradiction_clusters:
        return contradiction_clusters
    
    return []


def main(s: str, e: str) -> str:
    def clean_json(json_str: str) -> str:
        json_str = re.sub(r',\s*\]', ']', json_str)
        json_str = re.sub(r',\s*\}', '}', json_str)
        return json_str
    

    ranking_a = json.loads(clean_json(s))
    ranking_b = json.loads(clean_json(e))
    

    consensus = build_consensus_ranking(ranking_a, ranking_b)

    contradiction_core = find_contradiction_core(ranking_a, ranking_b, consensus)
    

    return [json.dumps(contradiction_core, ensure_ascii=False),consensus]

with open('Ранжировка  A.json', 'r', encoding='utf-8') as f:
    ranking_a = f.read()

with open('Ранжировка  B.json', 'r', encoding='utf-8') as f:
    ranking_b = f.read()

print("Ранжировка A:", ranking_a)
print("Ранжировка B:", ranking_b)
print()

result = main(ranking_a, ranking_b)

print("Результат (ядро противоречий):", result[0])
print("Результат (консенсус):", result[1])
