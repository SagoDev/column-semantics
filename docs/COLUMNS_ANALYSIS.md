# Column Analysis Documentation

The column semantics library provides an easy-to-use interface for analyzing multiple columns with rich, object-oriented results.

## 🚀 Quick Start

### Main Function: `analyze_columns()` ⭐ **SIMPLE & POWERFUL**
```python
from column_semantics import analyze_columns

columns = ["user_id", "created_at", "amount_usd", "is_active"]
results = analyze_columns(columns, include_summary=True)

# Quick stats - no dictionary navigation needed!
print(f"Analyzed {results.count} columns")
print(f"Top hypothesis: {results.top_hypothesis.label}")
print(f"Average confidence: {results.average_confidence:.2f}")

# Easy iteration over columns
for col in results:
    best = results.get_best_for_column(col)
    if best:
        print(f"{col}: {best.label} ({best.confidence:.2f})")

# Formatted summary text
print(results.get_summary_text())
```

## 📊 Available Functions

### `analyze_columns(columns, **kwargs)` ⭐ **PRIMARY FUNCTION**
**Returns user-friendly ColumnAnalysisResults object**

**Parameters:**
- `columns` (list[str]): List of column names to analyze
- `include_summary` (bool, default=False): Include summary statistics
- `confidence_threshold` (float, default=0.0): Filter hypotheses by minimum confidence

**Returns:** `ColumnAnalysisResults` - Object with convenient methods and properties

## 🎯 ColumnAnalysisResults API

### Properties
```python
results = analyze_columns_easily(columns, include_summary=True)

# Basic statistics
results.count                    # Number of columns analyzed
results.total_hypotheses          # Total hypotheses generated
results.semantic_types             # List of semantic types found
results.semantic_distribution       # Dict: {semantic_type: count}
results.average_confidence         # Average confidence score
results.has_summary              # Whether summary data is available

# Key hypotheses
results.top_hypothesis            # Hypothesis with highest confidence
results.high_confidence_hypotheses # List of hypotheses with confidence >= 0.7
```

### Column-Specific Methods
```python
# Get best hypothesis for a specific column
best = results.get_best_for_column("user_id")

# Get all hypotheses for a specific column
all_hyps = results.get_all_for_column("user_id")

# Find all columns with a specific semantic type
identifier_columns = results.get_columns_with_type("identifier")
monetary_columns = results.get_columns_with_type("monetary_amount")
```

### Utility Methods
```python
# Filter results by confidence threshold
high_conf_results = results.filter_by_confidence(0.8)

# Get formatted summary text
summary_text = results.get_summary_text()
print(summary_text)

# Dictionary-like access
for col_name in results:                    # Iterate over columns
for col_name, result in results.items():     # Get column-result pairs
if "user_id" in results:                  # Check if column exists
    analysis = results["user_id"]           # Access by column name
```

## 📋 Return Formats

### Traditional Dictionary Format
```python
{
    "columns": {
        "column_name_1": InferenceResult,
        "column_name_2": InferenceResult,
    },
    "total_columns": int,
    "summary": {  # Only if include_summary=True
        "total_hypotheses": int,
        "semantic_types_found": list[str],
        "semantic_distribution": dict[str, int],
        "average_confidence": float,
    }
}
```

### Object-Oriented Format
```python
ColumnAnalysisResults(
    count=4,
    total_hypotheses=7,
    semantic_types=['identifier', 'date', 'monetary_amount'],
    semantic_distribution={'identifier': 1, 'date': 3, 'monetary_amount': 1},
    average_confidence=0.52,
    top_hypothesis=SemanticHypothesis(...),
    high_confidence_hypotheses=[...]
)
```

## 🔍 Real-World Examples

### Basic Dataset Analysis
```python
from column_semantics import analyze_columns_easily

# Sample database columns
db_columns = [
    "user_id", "created_at", "updated_at",
    "amount_usd", "price_eur", "is_active",
    "customer_email", "product_count", "deleted_flag"
]

results = analyze_columns_easily(db_columns, include_summary=True)

print(f"Dataset Analysis Summary:")
print(f"Columns analyzed: {results.count}")
print(f"Semantic types found: {len(results.semantic_types)}")
print(f"Average confidence: {results.average_confidence:.2f}")

# Show semantic distribution
print(f"\nSemantic Type Distribution:")
for sem_type, count in results.semantic_distribution.items():
    percentage = (count / results.total_hypotheses) * 100
    print(f"  {sem_type}: {count} columns ({percentage:.1f}%)")

# Show high-confidence results
if results.high_confidence_hypotheses:
    print(f"\nHigh-Confidence Hypotheses (>= 0.7):")
    for hyp in results.high_confidence_hypotheses:
        print(f"  {hyp.label}: {hyp.confidence:.2f}")
```

### Column Classification
```python
results = analyze_columns_easily(db_columns, include_summary=True)

# Identify different semantic categories
identifiers = results.get_columns_with_type("identifier")
timestamps = results.get_columns_with_type("date")
monetary = results.get_columns_with_type("monetary_amount")
flags = results.get_columns_with_type("boolean_flag")

print(f"Identifiers: {identifiers}")
print(f"Timestamps: {timestamps}")
print(f"Monetary fields: {monetary}")
print(f"Boolean flags: {flags}")
```

### Quality Assessment
```python
results = analyze_columns_easily(db_columns, include_summary=True)

# Assess overall analysis quality
if results.average_confidence < 0.3:
    print("⚠️ Low confidence - consider improving rules or adding more patterns")
elif results.average_confidence > 0.7:
    print("✅ High confidence - good quality semantic analysis")
else:
    print("📊 Moderate confidence - reasonable results")

# Check for columns without hypotheses
unidentified = []
for col in results:
    if not results.get_best_for_column(col):
        unidentified.append(col)

if unidentified:
    print(f"⚠️ Unidentified columns: {unidentified}")
    print("Consider adding patterns or rules for these columns")
```

## 🎛️ Advanced Usage

### Confidence Filtering
```python
# Get only high-confidence results
high_conf_results = results.filter_by_confidence(0.8)

# Progressive analysis
confidence_levels = [0.5, 0.6, 0.7, 0.8, 0.9]
for threshold in confidence_levels:
    filtered = results.filter_by_confidence(threshold)
    print(f"Confidence >= {threshold}: {filtered.total_hypotheses} hypotheses")
```

### Integration with DataFrames
```python
import pandas as pd
from column_semantics import analyze_columns_easily

# Analyze DataFrame columns
df = pd.read_csv("data.csv")
results = analyze_columns_easily(df.columns.tolist(), include_summary=True)

# Create summary DataFrame
summary_data = []
for col in df.columns:
    best = results.get_best_for_column(col)
    if best:
        summary_data.append({
            'column': col,
            'semantic_type': best.label,
            'confidence': best.confidence,
            'priority': best.rule.priority if best.rule else None
        })

summary_df = pd.DataFrame(summary_data)
print(summary_df)
```

## 🔧 Performance Considerations

### Large Datasets
```python
# For large datasets, process in batches
large_column_list = [...]  # Hundreds or thousands of columns

batch_size = 100
all_results = None

for i in range(0, len(large_column_list), batch_size):
    batch = large_column_list[i:i + batch_size]
    batch_results = analyze_columns_easily(batch, include_summary=True)
    
    if all_results is None:
        all_results = batch_results
    else:
        # Merge results (implementation needed for combining)
        pass

print(f"Processed {all_results.count} columns in batches")
```

### Caching Results
```python
import pickle
from pathlib import Path

# Cache analysis results
cache_file = Path("column_analysis_cache.pkl")
if cache_file.exists():
    with open(cache_file, 'rb') as f:
        results = pickle.load(f)
else:
    results = analyze_columns_easily(columns, include_summary=True)
    with open(cache_file, 'wb') as f:
        pickle.dump(results, f)
```

## 🚨 Best Practices

1. **Use `analyze_columns_easily()` for new code** - More convenient API
2. **Enable summary** for better insights (`include_summary=True`)
3. **Set appropriate confidence thresholds** based on your needs
4. **Cache results** for repeated analyses of the same columns
5. **Validate results** before making decisions based on them
6. **Consider expanding knowledge base** if many columns lack hypotheses

## 📚 API Reference

### Complete Method List

#### Properties
- `count`: Number of analyzed columns
- `total_hypotheses`: Total hypotheses generated
- `semantic_types`: List of unique semantic types
- `semantic_distribution`: Dictionary with type counts
- `average_confidence`: Average confidence score
- `has_summary`: Whether summary statistics exist
- `top_hypothesis`: Highest confidence hypothesis
- `high_confidence_hypotheses`: Hypotheses with confidence ≥ 0.7

#### Methods
- `get_best_for_column(column_name: str)`: Best hypothesis for specific column
- `get_all_for_column(column_name: str)`: All hypotheses for specific column
- `get_columns_with_type(semantic_type: str)`: Columns matching semantic type
- `filter_by_confidence(min_confidence: float)`: Filtered results
- `get_summary_text()`: Formatted summary text

#### Dictionary-like Interface
- `__getitem__(column_name)`: Access column by name
- `__contains__(column_name)`: Check if column exists
- `__iter__()`: Iterate over column names
- `items()`: Get column-result pairs
- `keys()`: Get all column names
- `values()`: Get all column results

## 🆘 Troubleshooting

### Common Issues

1. **No hypotheses generated**
   ```python
   if results.total_hypotheses == 0:
       print("No semantic patterns detected")
       print("Check: column names, knowledge base, rules")
   ```

2. **Low confidence scores**
   ```python
   if results.average_confidence < 0.3:
       print("Low confidence scores detected")
       print("Consider: adding patterns, improving rules")
   ```

3. **Memory usage with large datasets**
   ```python
   # Process in smaller batches
   for batch in column_batches:
       analyze_columns_easily(batch)
   ```

### Debug Information
```python
# Access raw results for debugging
raw_data = results._raw_results
print(f"Raw structure keys: {raw_data.keys()}")

# Check individual column analysis
for col in results:
    all_hyps = results.get_all_for_column(col)
    print(f"{col}: {len(all_hyps)} hypotheses")
    for h in all_hyps:
        print(f"  {h.label}: {h.confidence:.3f}")
```

---

**Tip:** Start with `analyze_columns_easily()` for the best developer experience. Use `analyze_columns()` only if you need the raw dictionary format for specific integrations.