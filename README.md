# 📦 Data Version Control (DVC) — Project Documentation

This documentation provides a complete overview of **DVC (Data Version Control)**, how it integrates with Git, manages data pipelines, tracks metrics, and leverages `dvclive` for real-time experiment tracking.

---

## 📌 What is DVC?

**DVC (Data Version Control)** is an open-source tool that enables **data and model versioning, experiment reproducibility, and ML pipeline management**.  

It fills the gaps left by Git when working with large datasets and machine learning models that cannot or should not be stored directly in Git repositories.

**Key Features:**
- Track versions of datasets, model binaries, and intermediate outputs.
- Reproduce end-to-end experiments from raw data to final model.
- Share ML projects without large files, using lightweight metafiles and external storage.
- Track and visualize experiments, metrics, and plots.

---

## ⚙️ How DVC Works Alongside Git

DVC integrates seamlessly with Git, managing large files and data pipelines without bloating your Git history.

| 📌 **Git**                       | 📌 **DVC**                          |
|:--------------------------------|:------------------------------------|
| Tracks source code and small files. | Tracks large data files, models, and pipeline stages. |
| Stores files directly in the Git repository. | Stores large files externally and replaces them with lightweight `.dvc` metafiles tracked by Git. |
| Handles code versioning and collaboration. | Manages data, intermediate results, metrics, and experiments alongside code versions. |

**How They Work Together:**
1. **Initialize Git and DVC** in your project.
2. Use `dvc add` to track large files — this creates a `.dvc` metafile for each tracked file.
3. Use Git to track code and `.dvc` metafiles.
4. Store large files in remote storage (e.g., AWS S3, GDrive) using `dvc push`.
5. Retrieve necessary data files using `dvc pull`.
6. Automate and track ML pipelines via `dvc.yaml` and `dvc repro`.

This collaboration allows for a clean, version-controlled codebase and efficient data and model management.

---

## 🔗 What is a DVC Pipeline?

A **DVC pipeline** organizes your ML workflow into reproducible, modular stages — like data preparation, training, evaluation — each with clear input dependencies and output results.

**Benefits of Pipelines:**
- Ensures reproducibility of experiments.
- Only re-runs stages when inputs or code have changed.
- Defines clear dependencies and data flow.
- Enables automation of the entire workflow.

**How to Create a Pipeline Stage:**

```bash
dvc run -n preprocess \
        -d data/raw \
        -o data/processed \
        python preprocess.py
```

**Explanation:**

* `-n preprocess` : Names the pipeline stage.
* `-d data/raw`   : Specifies the dependency (input directory or file).
* `-o data/processed` : Specifies the output directory.
* `python preprocess.py` : The command to run in this stage.

Pipelines can be executed end-to-end using:

```bash
dvc repro
```

---

## 📑 What is `dvc.yaml` and Its Role in Pipelines?

The **`dvc.yaml`** file is the central configuration file for your DVC pipeline.
It defines:

* Each stage in your workflow.
* Commands to run for each stage.
* Dependencies (input files/directories/scripts).
* Outputs (generated files like processed data, trained models, metrics).
* Metrics and plots for experiment evaluation.

**Sample `dvc.yaml`:**

```yaml
stages:
  preprocess:
    cmd: python preprocess.py
    deps:
      - data/raw
      - preprocess.py
    outs:
      - data/processed

  train:
    cmd: python train.py
    deps:
      - data/processed
      - train.py
    outs:
      - model.pkl
    metrics:
      - metrics.json
```

**Why `dvc.yaml` Is Useful:**

* Documents and automates your workflow.
* Ensures reproducibility by recording exact commands and dependencies.
* Lets you reproduce, resume, or re-run pipelines efficiently with `dvc repro`.
* Makes collaboration easier by standardizing workflows across team members.

---

## 📊 What is `dvclive` and How Is It Used?

**`dvclive`** is a lightweight logging and experiment tracking library built for integrating live metrics tracking into your ML training loops.
It allows you to:

* Log scalar values like accuracy, loss, precision, etc.
* Automatically track and version these metrics within your DVC pipeline.
* View and compare results across different experiment runs.

**Key Advantages:**

* Simple integration with your Python training scripts.
* Works natively with DVC experiments.
* Automatically logs metrics to a file (e.g., `metrics.json`).
* Enables experiment comparison via `dvc exp show` and `dvc plots`.

**Example Usage in Python:**

```python
import dvclive

dvclive.log("loss", 0.356)
dvclive.log("accuracy", 0.91)
dvclive.next_step()
```

**Workflow with `dvclive`:**

1. Install:

   ```bash
   pip install dvclive
   ```
2. Integrate metric logging inside your training loop.
3. Run pipeline stages using `dvc repro` or `dvc exp run`.
4. Review logged metrics and compare experiments:

   ```bash
   dvc exp show
   dvc plots diff
   ```

**Why `dvclive` Is Valuable:**

* Keeps experiment logs consistent and versioned.
* Simplifies metric tracking and visualization.
* Integrates seamlessly with DVC pipelines and experiments.

---

## 📌 Summary

| Tool / Concept   | Purpose and Usage                                                      |
| :--------------- | :--------------------------------------------------------------------- |
| **DVC**          | Version control for datasets, models, and pipelines.                   |
| **Git**          | Version control for source code and lightweight text files.            |
| **DVC Pipeline** | Automates ML workflows with reproducible, dependency-aware stages.     |
| **`dvc.yaml`**   | Defines pipeline stages, their commands, dependencies, and outputs.    |
| **`dvclive`**    | Logs metrics during training; integrates with DVC experiment tracking. |

---

## 📚 Useful Resources

* 📖 [DVC Documentation](https://dvc.org/doc)
* 📖 [dvclive Documentation](https://dvc.org/doc/dvclive)
* 📖 [DVC Pipelines Overview](https://dvc.org/doc/start/data-management/pipelines)
* 📖 [DVC Experiments and Metrics](https://dvc.org/doc/user-guide/experiment-management)
