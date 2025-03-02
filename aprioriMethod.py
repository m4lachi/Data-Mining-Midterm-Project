import csv
import itertools
import time
from collections import defaultdict
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

# Load transactions from CSV, excluding empty strings
def loadTransactions(filename):
    transactions = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            transaction = {item.strip() for item in row[1:-1] if item.strip()}  # Exclude empty strings
            if transaction:  # Ensure non-empty transactions
                transactions.append(transaction)
    return transactions

# Generate k-itemsets
def generateItemsets(items, k):
    return set(itertools.combinations(items, k))

# Count frequent itemsets
def countFreqItemset(transactions, candidates, minSupport):
    counts = defaultdict(int)
    for transaction in transactions:
        for itemset in candidates:
            if set(itemset).issubset(transaction):
                counts[itemset] += 1
    numTransactions = len(transactions)
    return {itemset: count for itemset, count in counts.items() if count / numTransactions >= minSupport}

# Brute Force Method
def bruteForce(transactions, minSupport):
    items = set(item for transaction in transactions for item in transaction)
    k = 1
    freqItemset = {}

    while True:
        if k == 1:
            candidates = {(item,) for item in sorted(items)}  # Sorting is unnecessary but adds time
        else:
            prevFreq = list(freqItemset[k - 1].keys())
            candidates = generateItemsets(set(itertools.chain(*prevFreq)), k)

        transaction_list = [set(transaction) for transaction in transactions]  
        counts = defaultdict(int)
        for transaction in transaction_list:
            for itemset in candidates:
                if all(elem in transaction for elem in itemset):  
                    counts[itemset] += 1

        numTransactions = len(transactions)

        valid_itemsets = {}
        for itemset, count in counts.items():
            support = count / numTransactions
            if support >= minSupport:
                valid_itemsets[itemset] = count  

        freqItemset[k] = valid_itemsets

        if not freqItemset[k]:
            del freqItemset[k]
            break
        k += 1
    return freqItemset

# Generate Association Rules
def generateAssociationRules(freqItemset, minConfidence):
    rules = []
    for k, itemsets in freqItemset.items():
        if k < 2:
            continue
        for itemset, supportCount in itemsets.items():
            for i in range(1, k):
                for left in itertools.combinations(itemset, i):
                    right = set(itemset) - set(left)
                    left = tuple(left)
                    if len(right) == 0:
                        continue
                    leftSupport = freqItemset[len(left)].get(left, 0)
                    confidence = supportCount / leftSupport if leftSupport > 0 else 0
                    if confidence >= minConfidence:
                        rules.append((left, tuple(right), confidence))
    return rules

# Apriori Algorithm using mlxtend
def aprioriAlgorithm(transactions, minSupport, minConfidence):
    unique_items = sorted({item for transaction in transactions for item in transaction})
    encoded_data = [{item: (item in transaction) for item in unique_items} for transaction in transactions]
    df = pd.DataFrame(encoded_data)

    print(f"\nTotal Transactions: {len(transactions)}")
    print(f"Unique Items: {len(unique_items)}")

    frequent_itemsets = apriori(df, min_support=minSupport, use_colnames=True)

    if frequent_itemsets.empty:
        print("No frequent itemsets found. Try lowering minSupport.")
        return frequent_itemsets, pd.DataFrame()

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=minConfidence)

    return frequent_itemsets, rules

# Measure execution time
def measureTime(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start

# Main Execution
files = [
    "food_nutrition_transactions.csv",
    "medical_health_transactions.csv",
    "protein_diet_transactions.csv",
    "skincare_comestics_transactions.csv",
    "supplements_vitamins_transactions.csv"
]

# Handle file selection
while True:
    print("\nSelect a transaction file to analyze:")
    for i, file in enumerate(files, 1):
        print(f"{i}: {file}")

    try:
        file_choice = int(input("Enter the number corresponding to the file: ")) - 1
        if 0 <= file_choice < len(files):
            break
        else:
            print("Invalid selection. Please choose a valid file number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

while True:
    try:
        minSupport = float(input("Enter minimum support (e.g., 0.2 for 20%): "))
        if 0 < minSupport < 1:
            break
        print("Please enter a value between 0 and 1.")
    except ValueError:
        print("Invalid input. Please enter a decimal number.")

while True:
    try:
        minConfidence = float(input("Enter minimum confidence (e.g., 0.6 for 60%): "))
        if 0 < minConfidence < 1:
            break
        print("Please enter a value between 0 and 1.")
    except ValueError:
        print("Invalid input. Please enter a decimal number.")


selected_file = files[file_choice]
transactions = loadTransactions(selected_file)

# Run and time each algorithm
frequentItemsetBF, timeBF = measureTime(bruteForce, transactions, minSupport)
associationRulesBF, timeRulesBF = measureTime(generateAssociationRules, frequentItemsetBF, minConfidence)
frequentItemsetApriori, timeApriori = measureTime(aprioriAlgorithm, transactions, minSupport, minConfidence)

# Print Results
print("\nPerformance Comparison:")
print(f"Brute Force Execution Time: {timeBF:.3f} sec")
print(f"Apriori Execution Time: {timeApriori:.3f} sec")

# Print Frequent Itemsets (Brute Force)
print("\nFrequent Itemsets (Brute Force):")
if not frequentItemsetBF:
    print("No frequent itemsets found. Try lowering the minimum support.")
else:
    for k, itemsets in sorted(frequentItemsetBF.items()):
        print(f"\n{k}-itemsets:")
        for itemset, count in sorted(itemsets.items(), key=lambda x: -x[1]):
            print(f"{itemset}: {count}")

# Print Association Rules (Brute Force)
print("\nAssociation Rules (Brute Force):")
if not associationRulesBF:
    print("No association rules generated. Try adjusting minSupport or minConfidence.")
else:
    for rule in sorted(associationRulesBF, key=lambda x: -x[2]):
        print(f"{rule[0]} -> {rule[1]} (Confidence: {rule[2]:.2f})")

# Print Frequent Itemsets (Apriori)
print("\nFrequent Itemsets (Apriori):")
if frequentItemsetApriori[0].empty:
    print("No frequent itemsets found using Apriori.")
else:
    print(frequentItemsetApriori[0])

# Print Association Rules (Apriori)
print("\nAssociation Rules (Apriori):")
if frequentItemsetApriori[1].empty:
    print("No association rules generated using Apriori.")
else:
    for _, row in frequentItemsetApriori[1].iterrows():
        print(f"{set(row['antecedents'])} -> {set(row['consequents'])} (Confidence: {row['confidence']:.2f})")
