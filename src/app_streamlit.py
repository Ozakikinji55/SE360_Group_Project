import streamlit as st
import time

from core.problem import Problem
from solvers.greedy_solver import GreedySolver
from solvers.ilp_solver import ILPSolver
from solvers.meta_solver import MetaSolver

st.title("Optimal Sample Selection System")

m = st.number_input("M", value=45)
n = st.number_input("N", value=12)
k = st.number_input("K", value=6)
j = st.number_input("J", value=5)
s = st.number_input("S", value=5)

if st.button("Run Solver"):
    with st.spinner("Running..."):

        prob = Problem(m, n, k, j, s)
        if n <=12:
            solver = ILPSolver(prob)
        elif n <= 20:
            solver = GreedySolver(prob)
        else:
            solver = MetaSolver(prob)

        output = solver.solve()

        st.success("Done!")

        st.write("Count:", output["count"])
        st.write("Time:", f"{output['time']:.2f}s")

        st.write("Results (first 50):")
        for combo in output["results"][:50]:
            st.write(combo)