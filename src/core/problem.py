class Problem:
    def __init__(self, m, n, k, j, s, user_samples=None):
        """
        :param m: 总样本数 (45-54) [cite: 150]
        :param n: 随机选择或输入的样本数 (7-25) [cite: 152]
        :param k: 每个输出组包含的样本数 (4-7) [cite: 154]
        :param j: 逻辑子集的大小 (s <= j <= k) [cite: 16]
        :param s: 必须覆盖的元素个数 (3-7) [cite: 16]
        :param user_samples: 用户手动输入的 n 个样本列表 [cite: 130]
        """
        self.m = m
        self.n = n
        self.k = k
        self.j = j
        self.s = s
        
        # 如果用户没提供样本，则按照需求 4 自动生成 [cite: 130]
        if user_samples:
            self.samples = sorted(user_samples)
        else:
            import random
            self.samples = sorted(random.sample(range(1, m + 1), n))

    def __repr__(self):
        return f"Problem(m={self.m}, n={self.n}, k={self.k}, j={self.j}, s={self.s})"