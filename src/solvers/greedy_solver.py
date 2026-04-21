from solvers.base_solver import BaseSolver
import time

class GreedySolver(BaseSolver):
    def solve(self):
        start_time = time.time()
        
        # 1. 获取所有组合的位掩码 [cite: 11, 12, 13]
        from core.generator import MaskGenerator
        gen = MaskGenerator()
        k_masks, j_masks = gen.generate_all_masks(self.problem)
        
        # 2. 预计算：每个 k 组合覆盖了哪些 j 组合
        # 使用 list of sets 存储索引，加快后续排除速度
        coverage_map = []
        for k_m in k_masks:
            covered_indices = {
                idx for idx, j_m in enumerate(j_masks) 
                if gen.check_coverage(k_m, j_m, self.problem.s)
            }
            coverage_map.append(covered_indices)
            
        uncovered_j_indices = set(range(len(j_masks)))
        selected_indices = []

        # 3. 核心贪婪循环
        while uncovered_j_indices:
            best_k_idx = -1
            max_new_coverage = -1
            
            # 寻找当前能覆盖最多“剩余 j”的 k
            for idx, covered_set in enumerate(coverage_map):
                # 计算交集大小：即该 k 能新覆盖多少个 j
                new_coverage = len(covered_set & uncovered_j_indices)
                
                if new_coverage > max_new_coverage:
                    max_new_coverage = new_coverage
                    best_k_idx = idx
                
                # 优化点：如果发现一个 k 能覆盖所有剩余，直接跳出循环
                if max_new_coverage == len(uncovered_j_indices):
                    break
            
            if best_k_idx == -1: break # 防死循环
            
            # 记录选择并更新池子
            selected_indices.append(best_k_idx)
            uncovered_j_indices -= coverage_map[best_k_idx]

        execution_time = time.time() - start_time
        
        # 将索引转换回原始样本组合 [cite: 136]
        results = [self._decode_mask(k_masks[i]) for i in selected_indices]
        
        return {
            "results": results,
            "count": len(results),
            "time": execution_time
        }

    def _decode_mask(self, mask):
        """将位掩码还原为具体的样本数值"""
        res = []
        for i in range(self.problem.n):
            if (mask >> i) & 1:
                res.append(self.problem.samples[i])
        return res
    
    print("GreedySolver 已加载，准备执行贪心算法求解。")