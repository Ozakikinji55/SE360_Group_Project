import time
from core.problem import Problem
from core.generator import MaskGenerator
from core.validator import Validator
from solvers.greedy_solver import GreedySolver
from solvers.ilp_solver import ILPSolver
from solvers.meta_solver import MetaSolver
# from solvers.meta_solver import MetaSolver # 如果还没写完可以先注释

# --- 常量配置区 ---
M = 45
N = 7
K = 6
J = 6
S = 4
RUN_ID = 1  # 对应文件名中的 x
ALGORITHM = "meta"  # 可选: "ilp", "greedy", meta
# ----------------

def main():
    print(f"--- Optimal Samples Selection System ---")
    
    # 1. 初始化问题
    # 这里可以扩展为手动输入样本，目前默认随机选择 n 个样本
    prob = Problem(m=M, n=N, k=K, j=J, s=S)
    print(f"Selected Samples ({N}/{M}): {prob.samples}")
    
    # 2. 选择并运行求解器
    print(f"Running Solver: {ALGORITHM.upper()}...")
    if N <= 12:  # 小规模问题适合 ILP 求解器
        solver = ILPSolver(prob)
    elif N <= 20:  # 中等规模问题适合贪婪求解器
        solver = GreedySolver(prob)
    else: # 大规模问题适合 MetaSolver
        solver=MetaSolver(prob) # 如果 MetaSolver 还没写完，可以先注释掉这一行，默认使用 GreedySolver
        
        
    start_wall = time.time()
    output = solver.solve()
    end_wall = time.time()
    
    results = output["results"]
    count = output["count"]
    
    # 3. 验证结果 (Validator)
    validator = Validator(prob)
    is_valid, report = validator.validate(results)
    
    # 4. 打印输出
    print("-" * 30)
    print(f"Result Count (y): {count}")
    print(f"Execution Time: {output['time']:.4f} seconds")
    if "optimal" in output:
        print(f"Mathematical Optimality: {output['optimal']}")
    
    print(f"Validation Status: {'PASS ✅' if is_valid else 'FAIL ❌'}")
    print(f"Coverage Rate: {report['coverage_rate']*100:.2f}% ({report['covered_count']}/{report['total_j_combinations']} j-sets)")
    
    # 5. 保存结果到文件
    # 命名规则: m-n-k-j-s-x-y
    file_name = f"../results/{M}-{N}-{K}-{J}-{S}-{RUN_ID}-{count}.txt"
    try:
        with open(file_name, "w") as f:
            f.write(f"Problem: m={M}, n={N}, k={K}, j={J}, s={S}\n")
            f.write(f"Samples: {prob.samples}\n")
            f.write(f"Results Count: {count}\n")
            f.write("-" * 20 + "\n")
            for i, combo in enumerate(results, 1):
                f.write(f"{i}. {','.join(map(str, combo))}\n")
        print(f"Results saved to DB file: {file_name}")
    except Exception as e:
        print(f"Failed to save file: {e}")

    # 打印前 5 个结果示例
    print("\nSample Results (First 5):")
    for combo in results[:5]:
        print(f"  - {combo}")

if __name__ == "__main__":
    main()