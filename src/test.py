import itertools

def get_combinations(elements, r):
    return list(itertools.combinations(elements, r))

if __name__ == "__main__":
    m = 5
    n = 4
    k = 3
    j = 2
    s = 1
    
    # 1. 先确定我们要研究的“池子” (n个元素)
    # 假设我们从 1-5 中选了前 4 个作为样本池
    all_elements = list(range(1, m + 1))
    sample_pool = all_elements[:n]  # 结果是 [1, 2, 3, 4]
    print(f"Sample Pool (n={n}): {sample_pool}")
    
    # 2. 生成所有可能的 k 组合 (候选武器)
    # 这些是我们要挑出来的结果
    all_k_options = get_combinations(sample_pool, k)
    
    # 3. 生成所有可能的 j 组合 (挑战者池)
    # 挑战者必须是这个池子里的数字组合
    comparison_pool = [set(c) for c in get_combinations(sample_pool, j)]
    print(f"Initial Challenger Count (j={j}): {len(comparison_pool)}")
    
    results = []
    
    # 4. 开始比对
    # 我们从所有可能的 k 组合里选
    for cand in all_k_options:
        if not comparison_pool:
            break
        
        cand_set = set(cand)
        covered_this_round = []
        
        for challenger in comparison_pool:
            # 现在的 cand_set 是 {1,2,3}，challenger 是 {1,2}
            # 它们都是数字集合，可以正常计算交集
            if len(cand_set.intersection(challenger)) >= s:
                covered_this_round.append(challenger)
        
        if covered_this_round:
            results.append(cand)
            for covered in covered_this_round:
                comparison_pool.remove(covered)
            
            print(f"Selected Combination {cand}, Remaining Challengers: {len(comparison_pool)}")
    
    print(f"\nFinal Selected Optimal (Preliminary) Combinations: {results}")