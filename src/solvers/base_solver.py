from abc import ABC, abstractmethod

class BaseSolver(ABC):
    """
    所有求解器的抽象基类
    """
    def __init__(self, problem):
        """
        初始化时注入 Problem 实例
        """
        self.problem = problem

    @abstractmethod
    def solve(self):
        """
        子类必须实现此方法。
        返回格式约定为:
        {
            "results": [[...], [...]], # 选出的 k-combinations 列表
            "count": int,              # 选出的数量
            "time": float              # 运行耗时
        }
        """
        pass

    def _decode_mask(self, mask):
        """
        通用工具：将位掩码还原为具体的样本数值。
        既然每个算法都要用，直接放在基类里复用。
        """
        res = []
        for i in range(self.problem.n):
            if (mask >> i) & 1:
                res.append(self.problem.samples[i])
        return res