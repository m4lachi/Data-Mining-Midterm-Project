import csv
import itertools
from collections import defaultdict

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

def main():
    files = {
        "1": "food_nutrition_transactions.csv",
        "2": "medical_health_transactions.csv",
        "3": "protein_diet_transactions.csv",
        "4": "skincare_comestics_transactions.csv",
        "5": "supplements_vitamins_transactions2"
    }
    
    print("Select a transaction file to analyze:")
    for key, value in files.items():
        print(f"{key}: {value}")
    
    choice = input("Enter the number corresponding to the file: ")
    filename = files.get(choice)
    
    if not filename:
        print("Invalid choice. Exiting...")
        return
    
    try:
        minSupport = float(input("Enter minimum support (e.g., 0.2 for 20%): "))
        minConfidence = float(input("Enter minimum confidence (e.g., 0.5 for 50%): "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return
    
    transactions = loadTransactions(filename)
    frequentItemset = bruteForce(transactions, minSupport)
    associationRules = generateAssociationRules(frequentItemset, minConfidence)
    
    print("\nFrequent Itemsets:")
    for k, itemsets in frequentItemset.items():
        print(f"\n{k}-itemsets:")
        for itemset, count in itemsets.items():
            print(f"{itemset}: {count}")
    
    print("\nAssociation Rules:")
    if not associationRules:
        print("No association rules were generated. Try lowering the minimum confidence or support to find more relationships. \n")
    else:
        for rule in associationRules:
            print(f"{rule[0]} -> {rule[1]} (Confidence: {rule[2]:.2f})")

if __name__ == "__main__":
    main()
