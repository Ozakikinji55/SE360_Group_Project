from itertools import combinations

class MaskGenerator:
    @staticmethod
    def to_mask(indices):
        """将一组索引转换为位掩码"""
        mask = 0
        for i in indices:
            mask |= (1 << i)
        return mask

    @staticmethod
    def count_set_bits(n):
        """计算二进制中 1 的个数 (用于验证覆盖了多少个元素)"""
        return bin(n).count('1')

    def generate_all_masks(self, problem):
        """
        生成 Candidate Pool (k-masks) 和 Challenger Pool (j-masks)
        """
        # n 是我们实际处理的样本总数
        indices = list(range(problem.n))
        
        # 1. 生成所有可能的 k 组合 (候选集) [cite: 12]
        # 每一个元素是一个整数，其二进制表示中有 k 个 1
        k_masks = [self.to_mask(c) for c in combinations(indices, problem.k)]
        
        # 2. 生成所有可能的 j 组合 (挑战集) [cite: 19, 37]
        # 每一个元素是一个整数，其二进制表示中有 j 个 1
        j_masks = [self.to_mask(c) for c in combinations(indices, problem.j)]
        
        return k_masks, j_masks

    def check_coverage(self, k_mask, j_mask, s_requirement):
        """
        核心逻辑：验证一个 k 组合是否覆盖了一个 j 组合
        规则：如果 k_mask 与 j_mask 的交集中 1 的个数 >= s，则视为覆盖 [cite: 16]
        """
        intersection = k_mask & j_mask
        return self.count_set_bits(intersection) >= s_requirement
    
    
print("MaskGenerator 已加载，准备生成掩码并验证覆盖关系。")