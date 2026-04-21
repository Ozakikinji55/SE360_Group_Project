import itertools

def get_combinations(elements, r):
    return list(itertools.combinations(elements, r))

def verify_completeness(n, k, j, s, result_set):
    # 1. 生成所有必须覆盖的 j 组合 (比较库)
    target_library = set(itertools.combinations(range(1, n + 1), j))
    total_to_cover = len(target_library)
    
    # 2. 遍历你的结果集 (每一个 k 组)
    for k_group in result_set:
        # 找出这个 k 组里所有可能的 s 阶子集
        # (注意：当 j=s 时，就是找出 k 组里所有的 j 组合)
        current_subsets = set(itertools.combinations(sorted(k_group), s))
        
        # 3. 从比较库中移除已覆盖的组合
        # 只要 k 组里的 s 子集出现在库里，就消掉它
        target_library -= current_subsets
    
    # 4. 核心判定
    is_valid = len(target_library) == 0
    return is_valid, len(target_library)








##请在最终使用之前删除这一部分

"""
if __name__ == "__main__":
    m = 45
    n = 13
    k = 6
    j = 5
    s = 5
    count=0
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
            count+=1
            for covered in covered_this_round:
                comparison_pool.remove(covered)
            
            print(f"Selected Combination {cand}, Remaining Challengers: {len(comparison_pool)}")
    
    print(f"\nFinal Selected Optimal (Preliminary) Combinations: {results}")
    print(f"Total Selected Combinations: {count}")
    
    # 5. 最后验证我们的结果是否覆盖了所有的 j 组合
    is_valid = verify_solution(m, n, k, j, s, results)
    print(f"Does our solution cover all j combinations? {'Yes' if is_valid else 'No'}")"""
