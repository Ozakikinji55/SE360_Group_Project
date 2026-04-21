from core.generator import MaskGenerator

class Validator:
    def __init__(self, problem):
        self.problem = problem
        self.gen = MaskGenerator()

    def validate(self, selected_combinations):
        """
        验证结果集是否实现了 100% 覆盖
        :param selected_combinations: List[List[int]]，求解器选出的 k 组合列表
        :return: (bool, dict) 是否全覆盖，以及详细的覆盖报告
        """
        # 1. 将选出的组合转换回位掩码以便快速对比
        # 首先需要将具体的样本数值转回索引，再转为位掩码
        sample_to_idx = {val: i for i, val in enumerate(self.problem.samples)}
        selected_masks = []
        for combo in selected_combinations:
            indices = [sample_to_idx[val] for val in combo]
            selected_masks.append(self.gen.to_mask(indices))

        # 2. 生成所有需要被挑战的 j-masks
        _, j_masks = self.gen.generate_all_masks(self.problem)
        
        uncovered_j_masks = []
        
        # 3. 逐一验证
        for j_m in j_masks:
            is_covered = False
            for k_m in selected_masks:
                if self.gen.check_coverage(k_m, j_m, self.problem.s):
                    is_covered = True
                    break
            
            if not is_covered:
                uncovered_j_masks.append(j_m)

        # 4. 汇总报告
        is_success = len(uncovered_j_masks) == 0
        report = {
            "is_valid": is_success,
            "total_j_combinations": len(j_masks),
            "covered_count": len(j_masks) - len(uncovered_j_masks),
            "uncovered_count": len(uncovered_j_masks),
            "coverage_rate": (len(j_masks) - len(uncovered_j_masks)) / len(j_masks) if j_masks else 0
        }
        
        return is_success, report

    def get_uncovered_details(self, uncovered_masks):
        """将未覆盖的掩码还原为易读的样本数值，用于 Debug"""
        details = []
        for mask in uncovered_masks:
            res = []
            for i in range(self.problem.n):
                if (mask >> i) & 1:
                    res.append(self.problem.samples[i])
            details.append(res)
        return details