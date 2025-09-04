# src/holoq_transpiler.py
# MVP para transpilar HoloQ -> Qiskit (Python)
# Uso:
#   python src/holoq_transpiler.py examples/holographic_edge.holoq
#
# Genera out_qiskit.py en el directorio raíz del repo.

import re
import sys
from math import tau

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []  # list of (u, v, weight|None)

def parse_edges(s):
    edges = []
    # matches tuples like (0,1)[0.25]
    for tup in re.findall(r"\((\d+)\s*,\s*(\d+)\)(?:\[(.*?)\])?", s):
        u, v, w = int(tup[0]), int(tup[1]), (float(tup[2]) if tup[2] else None)
        edges.append((u, v, w))
    return edges

def boundary_edges(G: Graph):
    # MVP: todas las aristas son "borde".
    return G.edges

class HoloQProgram:
    def __init__(self):
        self.N = None
        self.G = Graph()
        self.subsets = {}
        self.measure_ops = []  # names of subsets to measure
        self.holo_reg_name = "h"
        self.classical_reg_name = "c"

    def set_subset(self, name, values):
        self.subsets[name] = values

def parse_program(src: str) -> HoloQProgram:
    p = HoloQProgram()
    # const N = 8;
    m = re.search(r"const\s+N\s*=\s*(\d+)\s*;", src)
    if m:
        p.N = int(m.group(1))

    # graph G { ... }
    m = re.search(r"graph\s+G\s*{([^}]*)}", src, re.S)
    if m:
        body = m.group(1)
        nm = re.search(r"nodes:\s*(\d+)\s*\.\.\s*(\d+)\s*;", body)
        if nm:
            a, b = int(nm.group(1)), int(nm.group(2))
            p.G.nodes = list(range(a, b + 1))
        em = re.search(r"edges:\s*(.*?);", body, re.S)
        if em:
            p.G.edges = parse_edges(em.group(1))

    # reg holo h[N];
    if p.N is None:
        m = re.search(r"reg\s+holo\s+([A-Za-z_]\w*)\[(\d+)\]\s*;", src)
        if m:
            p.holo_reg_name = m.group(1)
            p.N = int(m.group(2))
    else:
        m = re.search(r"reg\s+holo\s+([A-Za-z_]\w*)\[\s*N\s*\]\s*;", src)
        if m:
            p.holo_reg_name = m.group(1)

    # const NAME = [ ... ];
    for name, arr in re.findall(r"const\s+([A-Za-z_]\w*)\s*=\s*\[([^\]]+)\]\s*;", src):
        vals = [int(x.strip()) for x in arr.split(",")]
        p.set_subset(name, vals)

    # measure h[A] -> c[A];
    for meas in re.findall(r"measure\s+\w+\[(\w+)\]\s*->\s*\w+\[\1\]\s*;", src):
        p.measure_ops.append(meas)

    return p

def phi(edge):
    # Defecto: 2π * weight si viene, si no, π/4
    _, _, w = edge
    return tau * w if w is not None else (3.141592653589793 / 4)

def to_qiskit(p: HoloQProgram) -> str:
    lines = []
    lines += [
        "from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister",
        "from qiskit.circuit.library import PhaseGate",
        f"q = QuantumRegister({p.N}, '{p.holo_reg_name}')",
        f"c = ClassicalRegister({p.N}, '{p.classical_reg_name}')",
        "qc = QuantumCircuit(q, c)",
        "",
        "# --- encoding isometry blocks (MVP: placeholder) ---",
        "# TODO: apply isometric blocks based on G substructures",
        "",
        "# --- THD over boundary edges ---",
    ]
    for (u, v, w) in boundary_edges(p.G):
        lines.append(f"qc.h(q[{u}])")
        lines.append(f"qc.cp({phi((u, v, w))}, q[{u}], q[{v}])")
    lines.append("")
    for name in p.measure_ops:
        subset = p.subsets.get(name, [])
        for i in subset:
            lines.append(f"qc.measure(q[{i}], c[{i}])")
    lines.append("")
    lines.append("# Exponer qc para importaciones")
    lines.append("globals()['qc'] = qc")
    return "\\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("Uso: python src/holoq_transpiler.py <archivo.holoq>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    prog = parse_program(src)
    py = to_qiskit(prog)
    with open("out_qiskit.py", "w", encoding="utf-8") as f:
        f.write(py)
    print("Transpilado a out_qiskit.py")

if __name__ == "__main__":
    main()
