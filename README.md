# HoloQ 🌌

**HoloQ** es un lenguaje de programación experimental para cómputo cuántico holográfico.
Permite definir **holobits**, aplicar **isometrías de codificación**, operar sobre el **borde de un grafo** y realizar **mediciones holográficas**.

> MVP: Transpila a **Qiskit** (Python) u OpenQASM (en futuras versiones).

## Características del MVP
- `reg holo h[n]` para declarar holobits.
- `graph G { nodes; edges; }` con pesos de aristas.
- Bucle sobre el bordo: `for e in boundary(G) { H on ...; CP(phi(e)) on ... }`.
- Medición parcial: `measure h[A] -> c[A]`.
- Función `phi(e)` que usa el peso de la arista (fase = `2π * weight`).

## Ejemplo

```holoq
// 0) Parámetros y grafo
const N = 8;

graph G {
  nodes: 0..7;
  edges: (0,1)[0.25], (1,2)[0.5], (2,3)[0.125], (3,4)[0.75],
         (4,5)[0.33], (5,6)[0.66], (6,7)[0.1], (7,0)[0.9];
}

// 1) Registrar holobits (borde)
reg holo h[N];

// 2) Codificador holográfico (bloques isométricos) — placeholder MVP
isometry IsoBlock(g, h) {
  // TODO: implementar bloques isométricos reales
}
encode G with ISO(IsoBlock, h);

// 3) THD sobre el borde (H y CP con fase por arista)
for e in boundary(G) {
  H on h[e.u];
  CP(phi(e)) on h[e.u], h[e.v];
}

// 4) Medición de un observable holográfico
const A = [0,2,4,6];
measure h[A] -> c[A];
```

## Requisitos
- Python 3.10+
- [Qiskit](https://qiskit.org/): `pip install qiskit`

## Uso rápido
1. Guarda tu programa en `examples/holographic_edge.holoq` o crea otro `.holoq`.
2. Ejecuta el transpilador para generar `out_qiskit.py`:
   ```bash
   python src/holoq_transpiler.py examples/holographic_edge.holoq
   ```
3. (Opcional) Ejecuta el circuito de salida en Python/Qiskit:
   ```python
   import out_qiskit  # construye qc
   print(out_qiskit.qc)
   ```

## Estructura
```
holoq/
 ├─ examples/
 │   └─ holographic_edge.holoq
 ├─ src/
 │   └─ holoq_transpiler.py
 ├─ LICENSE
 ├─ README.md
 └─ .gitignore
```

## Licencia
[Apache License 2.0](LICENSE)

---

¡Contribuciones bienvenidas! PRs con mejoras al parser, semántica de `boundary`, y backends son especialmente útiles.

## Publicar en GitHub

**Opción A — con GitHub CLI (`gh`)**  
1. Instala [Git](https://git-scm.com/) y [GitHub CLI](https://cli.github.com/).
2. Autentícate: `gh auth login`
3. Desde la carpeta del proyecto, ejecuta:
   ```bash
   ./scripts/publish_github.sh holoq public
   ```
   > Para publicar en una organización, usa `ORG/REPO` como primer argumento.

**Opción B — sin `gh` (manual)**  
```bash
git init
git add .
git commit -m "Initial commit: HoloQ MVP"
git branch -M main
git remote add origin https://github.com/<USUARIO>/holoq.git
git push -u origin main
```
