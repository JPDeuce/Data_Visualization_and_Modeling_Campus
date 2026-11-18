# Dataset: UCI Wine Quality (red + white Vinho Verde)

## Source

- **Title:** Wine Quality
- **Publisher:** UC Irvine Machine Learning Repository
- **Source link:** https://archive.ics.uci.edu/dataset/186/wine+quality
- **DOI:** https://doi.org/10.24432/C56S3T
- **Accessed:** 2026-11-18
- **Underlying publication:** P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis,
  "Modeling wine preferences by data mining from physicochemical properties,"
  *Decision Support Systems*, Elsevier, 47(4):547-553, 2009.
- **Collection context:** Physicochemical test results and expert sensory scores for red and
  white Portuguese "Vinho Verde" wine samples from the north of Portugal. The score is the
  median of at least three expert evaluations on a 0-10 scale. There is no time/date feature.

## Files in this folder

- `wine_quality_red_white.csv` — the fixed lab dataset. It combines the two UCI source files,
  `winequality-red.csv` (1,599 rows) and `winequality-white.csv` (4,898 rows), into one
  comma-separated file with 6,497 rows. A `wine_type` column (`red` or `white`) was added to
  label the source file; the 11 original measurement columns and the `quality` output are
  unchanged. The original semicolon-delimited files used quoted numeric fields; this fixed
  copy uses commas and no quotes around numbers. No rows were added, removed, sampled, or
  replaced. The 1,177 rows that exactly match an earlier row were kept because the source has
  no sample ID and identical measurements can come from different bottles. There are no
  missing values.

## Feature definitions (one row = one wine sample)

| Column | Meaning and units | Type |
| --- | --- | --- |
| `wine_type` | Wine colour added to combine the two source files: `red` or `white` | categorical |
| `fixed acidity` | Fixed acidity, g/L | quantitative |
| `volatile acidity` | Volatile acidity, g/L | quantitative |
| `citric acid` | Citric acid, g/L | quantitative |
| `residual sugar` | Residual sugar, g/L | quantitative |
| `chlorides` | Chlorides (sodium chloride), g/L | quantitative |
| `free sulfur dioxide` | Free sulfur dioxide, mg/L | quantitative |
| `total sulfur dioxide` | Total sulfur dioxide, mg/L | quantitative |
| `density` | Density, g/cm³ | quantitative |
| `pH` | Acidity (pH), unitless | quantitative |
| `sulphates` | Sulphates (potassium sulphate), g/L | quantitative |
| `alcohol` | Alcohol content, percent by volume | quantitative |
| `quality` | Median sensory score from at least 3 experts, 0-10 | quantitative (ordered score) |

Units follow the source publication; the UCI variable table lists the measurements but does
not repeat units for every feature.

## Reuse terms

The UCI Wine Quality dataset is licensed under **Creative Commons Attribution 4.0
International (CC BY 4.0)**, which permits sharing and adaptation for any purpose with
appropriate credit. This folder is shared with that attribution: the source URL, DOI, access
date, and Cortez et al. (2009) citation are recorded above and are also displayed in the
dashboard. No personal or identifying information is included.
