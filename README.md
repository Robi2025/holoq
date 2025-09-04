# HoloQ 🌌⚛️

<p align="center">
  <img src="assets/holoq-logo.png" alt="HoloQ Logo" width="180"/>
</p>

<p align="center">
  <b>Lenguaje de programación holográfico para cómputo cuántico en el borde</b><br/>
  🚀 Diseñado para investigadores, desarrolladores y laboratorios de innovación.
</p>

---

## 🔰 Descripción

**HoloQ** es un lenguaje de programación experimental que combina conceptos de holografía y cómputo cuántico.  
Su objetivo es simplificar la definición de **holobits**, operaciones sobre el **borde de un grafo** y **mediciones holográficas**, compilando a **Qiskit** y en el futuro a **OpenQASM 3**.

---

## 📦 Estado del Proyecto

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Build](https://img.shields.io/github/actions/workflow/status/TU-USUARIO/holoq/ci.yml?branch=main)
![Stars](https://img.shields.io/github/stars/TU-USUARIO/holoq?style=social)

---

## 📂 Estructura

- `src/` ⚙️ núcleo y transpilador HoloQ → Qiskit
- `examples/` 🧪 programas de ejemplo en `.holoq`
- `scripts/` 🖥️ automatización y despliegue en GitHub
- `assets/` 🎨 iconos y recursos gráficos (logo, imágenes)
- `README.md` 📖 documentación principal
- `LICENSE` 📜 licencia Apache 2.0

---

## 🚀 Ejemplo rápido

Archivo: `examples/holographic_edge.holoq`

```holoq
graph G {
  nodes: 0..7;
  edges: (0,1)[0.25], (1,2)[0.5];
}
reg holo h[8];

for e in boundary(G) {
  H on h[e.u];
  CP(phi(e)) on h[e.u], h[e.v];
}

const A = [0,2,4,6];
measure h[A] -> c[A];
```

Compila a un circuito de **Qiskit** con:

```bash
python src/holoq_transpiler.py examples/holographic_edge.holoq
```

---

## ⚙️ Requisitos

- Python 3.10+
- [Qiskit](https://qiskit.org/)  
  ```bash
  pip install qiskit
  ```

---

## 🛠️ Roadmap

- [x] Parser inicial y transpiler a Qiskit  
- [x] Soporte para grafos y fases `phi(e)`  
- [ ] Bloques isométricos (`encode ISO(...)`)  
- [ ] Export a OpenQASM 3  
- [ ] Optimización topológica y backends adicionales  
- [ ] Interfaz visual en web / Jupyter  

---

## 👩‍💻 Contribuciones

Las contribuciones son bienvenidas 🙌  
Haz un **fork**, crea una rama y envía tu **pull request**.  

```bash
git checkout -b feature/nueva-funcionalidad
git commit -m "Agrega nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

---

## 📜 Licencia

Este proyecto está licenciado bajo **Apache License 2.0** – ver el archivo [LICENSE](LICENSE).

---

<p align="center">
  Hecho con 💜 por <b>Cristian Henriquez y el equipo HoloQ</b>
</p>
