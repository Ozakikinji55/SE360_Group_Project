from ortools.sat.python import cp_model
from .base_solver import BaseSolver
import time

class ILPSolver(BaseSolver):
    def solve(self):
        start_time = time.time()
        from core.generator import MaskGenerator
        gen = MaskGenerator()
        k_masks, j_masks = gen.generate_all_masks(self.problem)
        
        model = cp_model.CpModel()
        
        # 1. 变量：每个 k-mask 选或不选 (0 或 1)
        x = [model.NewBoolVar(f'x_{i}') for i in range(len(k_masks))]
        
        # 2. 预计算覆盖关系并添加约束
        # 针对每一个 j-mask，必须至少有一个覆盖它的 k-mask 被选中
        for j_idx, j_m in enumerate(j_masks):
            covering_ks = [
                x[k_idx] for k_idx, k_m in enumerate(k_masks)
                if gen.check_coverage(k_m, j_m, self.problem.s)
            ]
            model.Add(sum(covering_ks) >= 1)
            
        # 3. 目标：最小化选中的 k-mask 总数
        model.Minimize(sum(x))
        
        # 4. 求解
        solver = cp_model.CpSolver()
        # 设置求解超时，防止在大规模参数下卡死
        solver.parameters.max_time_in_seconds = 3000.0
        status = solver.Solve(model)
        
        results = []
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for i in range(len(k_masks)):
                if solver.Value(x[i]):
                    results.append(self._decode_mask(k_masks[i]))
        
        return {
            "results": results,
            "count": len(results),
            "time": time.time() - start_time,
            "optimal": status == cp_model.OPTIMAL
        }