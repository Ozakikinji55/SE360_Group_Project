import random
import math
import time
from .base_solver import BaseSolver
from core.generator import MaskGenerator

class MetaSolver(BaseSolver):
    
    def _hamming_distance(self, mask1, mask2):
        """Calculate Hamming distance between two integer masks using bitwise XOR."""
        return bin(mask1 ^ mask2).count('1')

    def _avg_hamming_to_set(self, candidate_idx, solution_indices, k_masks):
        if not solution_indices:
            return 0
        candidate_mask = k_masks[candidate_idx]
        total_dist = sum(self._hamming_distance(candidate_mask, k_masks[idx]) for idx in solution_indices)
        return total_dist / len(solution_indices)

    def solve(self):
        start_time = time.time()
        gen = MaskGenerator()
        k_masks, j_masks = gen.generate_all_masks(self.problem)
        
        # --- 性能优化核心：惰性缓存 (Lazy Cache) ---
        # 仅缓存被实际评估过的 k_mask 的覆盖集合，避免 90 亿次无用计算
        coverage_cache = {}

        def get_covered_j(k_idx):
            if k_idx not in coverage_cache:
                k_m = k_masks[k_idx]
                covered = set()
                for j_idx, j_m in enumerate(j_masks):
                    if gen.check_coverage(k_m, j_m, self.problem.s):
                        covered.add(j_idx)
                coverage_cache[k_idx] = covered
            return coverage_cache[k_idx]

        # --- 1. 随机贪心初始化 (Stochastic Greedy) ---
        uncovered_j = set(range(len(j_masks)))
        current_solution = set()
        
        # 根据问题规模动态调整采样率：基数越大，采样数越保守以保证速度
        sample_size = 1000 if len(k_masks) < 10000 else 300

        while uncovered_j:
            best_k = -1
            best_cover_count = -1
            
            # 仅在随机采样的候选池中寻找局部最优
            candidate_pool = random.sample(range(len(k_masks)), min(sample_size, len(k_masks)))
            
            for k_idx in candidate_pool:
                k_m = k_masks[k_idx]
                cover_count = 0
                
                # 性能关键点：仅和【尚未覆盖】的 j_masks 进行判断，跳过已覆盖项
                for j_idx in uncovered_j:
                    if gen.check_coverage(k_m, j_masks[j_idx], self.problem.s):
                        cover_count += 1
                
                if cover_count > best_cover_count:
                    best_cover_count = cover_count
                    best_k = k_idx
                    
            # 选定后，加入缓存并更新未覆盖集合
            current_solution.add(best_k)
            uncovered_j -= get_covered_j(best_k)

        best_solution = current_solution.copy()
        
        # --- 2. 模拟退火优化 (Simulated Annealing + Novelty Search) ---
        temp = 100.0
        cooling_rate = 0.98
        min_temp = 0.1
        stagnation_counter = 0
        stagnation_limit = 50
        target_coverage = len(j_masks)

        def get_coverage_score(sol_indices):
            covered = set()
            for idx in sol_indices:
                covered.update(get_covered_j(idx))
            return len(covered)

        while temp > min_temp:
            new_solution = current_solution.copy()
            
            if stagnation_counter > stagnation_limit:
                # 触发汉明距离变异（逃离局部最优）
                for _ in range(random.randint(1, min(3, len(new_solution) - 1))):
                    new_solution.remove(random.choice(list(new_solution)))
                
                # 从小样本池中选择一个汉明距离最远的 mask
                pool = random.sample(range(len(k_masks)), min(100, len(k_masks)))
                novel_k = max(pool, key=lambda idx: self._avg_hamming_to_set(idx, new_solution, k_masks))
                new_solution.add(novel_k)
                stagnation_counter = 0
            else:
                # 标准替换
                if new_solution:
                    new_solution.remove(random.choice(list(new_solution)))
                new_solution.add(random.choice(range(len(k_masks))))

            current_coverage = get_coverage_score(current_solution)
            new_coverage = get_coverage_score(new_solution)
            
            # 能量函数：极度惩罚覆盖不足，轻微惩罚集合大小
            current_energy = (target_coverage - current_coverage) * 1000 + len(current_solution)
            new_energy = (target_coverage - new_coverage) * 1000 + len(new_solution)
            
            delta_e = new_energy - current_energy

            if delta_e < 0 or random.random() < math.exp(-delta_e / temp):
                current_solution = new_solution
                
                if new_coverage == target_coverage and len(current_solution) < len(best_solution):
                    best_solution = current_solution.copy()
                    stagnation_counter = 0
                else:
                    stagnation_counter += 1
            else:
                stagnation_counter += 1
                
            temp *= cooling_rate

        results = [self._decode_mask(k_masks[i]) for i in best_solution]
        return {
            "results": results,
            "count": len(results),
            "time": time.time() - start_time
        }