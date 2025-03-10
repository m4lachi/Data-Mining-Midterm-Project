# Data-Mining Midterm Project

## Overview 
This Python program compares the efficiency and effectiveness of two algorithms for finding frequent itemsets and association rules in transactional datasets: the Brute Force method and the Apriori algorithm (using the `mlxtend` library). This program allows users to select a dataset, specify minimum support and confidence thresholds, and evaluate the performance of each approach.

## Features
- **Brute Force Method:** It iterates through all possible itemsets to determine frequent itemsets and generate association rules.
- **Apriori Algorithm:** Uses an efficient, iterative method to find frequent itemsets and generate association rules.
- **Performance Comparison:** Measures and compares the execution time of both methods.
- **User Input:** Allows users to select transaction datasets and define minimum support and confidence thresholds.
- **Graphical Analysis:** Visualizes execution time differences and support values of frequent itemsets.

## Requirements
The program requires the following Python libraries:
- `csv`
- `itertools`
- `time`
- `collections`
- `pandas`
- `mlxtend`

To install missing dependencies, run:
```bash
pip install pandas mlxtend
```

## Usage
1. Run the script in a Python environment.
2. Select a transaction dataset from the provided options:
   - `food_nutrition_transactions.csv`
   - `medical_health_transactions.csv`
   - `protein_diet_transactions.csv`
   - `skincare_cosmetics_transactions.csv`
   - `supplements_vitamins_transactions.csv`
3. Enter a minimum support value (e.g., `0.2` for 20%).
4. Enter a minimum confidence value (e.g., `0.6` for 60%).
5. The script will execute both the Brute Force and Apriori algorithms, measuring execution times and displaying the frequent itemsets and association rules.
6. An analysis will be displayed showing execution time differences and itemset support distributions.

## Output
The program outputs:
- Execution times for both Brute Force and Apriori algorithms.
- Frequent itemsets discovered by each method.
- Association rules generated by each method, with confidence scores.
- A visualization of execution time differences and support values of frequent itemsets.

## Example Output
```
Performance Comparison:
Brute Force Execution Time: 12.345 sec
Apriori Execution Time: 0.789 sec

Frequent Itemsets (Brute Force):
2-itemsets:
('milk', 'bread'): 15
('eggs', 'bread'): 12
...

Association Rules (Brute Force):
('milk',) -> ('bread',) (Confidence: 0.75)
...

Frequent Itemsets (Apriori):
    support        itemsets
0      0.30     (milk, bread)
...

Association Rules (Apriori):
{'milk'} -> {'bread'} (Confidence: 0.75)
...

```

## Notes
- The Brute Force method may take significantly longer on large datasets.
- If no frequent itemsets or association rules are found, try lowering the minimum support or confidence.
- The graphical output helps visualize efficiency differences and support distributions.

## License
This project is open-source and available for educational and research purposes.

## Author
Michelle Zambrano
