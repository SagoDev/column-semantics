# column-semantics

Semantic inference of column meanings for data engineering workflows.

`column-semantics` is a Python library designed to help data engineers understand datasets with little or no documentation. By analyzing column names, it infers their most likely meaning, expected data type, and typical role in a data model using deterministic rules and domain knowledge.

This project is intentionally pragmatic: no black-box machine learning, no mandatory LLMs — just explainable heuristics grounded in real-world data engineering conventions.

---

## Why column-semantics exists

In real data engineering work, you often face:

* Legacy datasets with no data dictionary
* Inconsistent naming conventions across teams
* Ambiguous columns like `amt`, `flag`, `dt`, `value`
* Time pressure that prevents deep manual exploration

`column-semantics` helps you bootstrap understanding quickly and safely.

---

## What the library does

Given a column name, the library can infer:

* Possible semantic meanings
* Expected data type (e.g. integer, decimal, boolean, timestamp)
* Typical role (metric, identifier, flag, timestamp, foreign key)
* Engineering notes and best practices
* A confidence score for the inference

---

## What the library does NOT do (by design)

* It does not inspect actual data values (yet)
* It does not modify schemas or datasets
* It does not rely on probabilistic or opaque models

The goal is explainability and trust.

---

## Design principles

* **Deterministic**: same input always produces the same output
* **Explainable**: every inference has a clear reason
* **Extensible**: new rules and domains can be added easily
* **Engineering-first**: built around real data engineering practices

---

## Project status

This library is under active development.

* Stability: experimental
* API: subject to change during early versions

---

## License

MIT License

---