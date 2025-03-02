import csv
import random

#Define bioinformatics-related supermarket items
categories = {
    "supplements_vitamins": [
        ("Probiotics", 25.99),
        ("Omega-3 Capsules", 18.49),
        ("Vitamin D", 12.99),
        ("Iron Supplement", 15.29),
        ("Magnesium Pills", 10.99),
        ("Zinc Tablets", 8.99),
        ("Calcium Tablets", 14.49),
        ("Multivitamins", 20.99),
        ("B12 Shots", 30.99),
        ("Folic Acid", 9.99),
    ],
    "food_nutrition": [
        ("Lactose-Free Milk", 4.99),
        ("Gluten-Free Bread", 5.49),
        ("Organic Spinach", 3.99),
        ("GMO-Free Corn", 2.49),
        ("Soy Milk", 3.29),
        ("Kombucha", 4.79),
        ("Probiotic Yogurt", 1.99),
        ("Tofu", 2.99),
        ("Chia Seeds", 6.49),
        ("Almond Butter", 7.99),
    ],
    "medical_health": [
        ("Blood Glucose Monitor", 39.99),
        ("Electrolyte Drink", 2.99),
        ("First Aid Kit", 14.99),
        ("Digital Thermometer", 9.99),
        ("DNA Test Kit", 59.99),
        ("Antiseptic Wipes", 4.49),
        ("N95 Mask", 5.99),
        ("Hand Santizier", 3.49),
        ("Disinfecting Spary", 6.99),
        ("Compression Sock", 12.99),
    ],
    "protein_diet": [
        ("Whey Protein Powder", 29.99),
        ("Plant-Based Protein", 27.49),
        ("Energy Bar", 1.99),
        ("Soy Protein Powder", 26.99),
        ("Meal Replacement Shake", 3.99),
        ("Collagen Peptides", 22.99),
        ("Caesin Protein", 28.49),
        ("Keto Snack", 2.49),
        ("BCAA Supplement", 19.99),
        ("Pre-Workout Powder", 32.99),
    ],
    "skincare_comestics": [
        ("Sunscreen SPF 50", 12.99),
        ("Vitamin C Serum", 24.99),
        ("Collagen Cream", 18.49),
        ("Retinol Night Cream", 29.99),
        ("Hyaluronic Acid Serum", 22.99),
        ("Moisturizer", 15.99), 
        ("Aloe Vera Gel", 6.49),
        ("Anti-Aging Eye Cream", 19.99),
        ("Face Mask", 3.99),
        ("Lip Balm", 2.49),
    ],
}

#Generate transactions for each category
def generate_transactions(category_name, items, num_transactions = 20):
    transactions = []
    for i in range(num_transactions):
        num_items = random.randint(2,5) #Each transaction has 2 to 5 items
        transaction_items = random.sample(items, num_items)
        total_price = sum(item[1] for item in transaction_items)

        item_names = [item[0] for item in transaction_items]
        while len(item_names) < 5:
            item_names.append("")

        transactions.append([i+1] + item_names + [round(total_price, 2)])

    return transactions
    
# Save transactions to CSV
def save_to_csv(category_name, transactions):
    filename = f"{category_name}_transactions.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Transaction_ID", "Item1", "Item2", "Item3", "Item4", "Item5", "Total Price"])
        for transaction in transactions:
            writer.writerow(transaction)
    print(f"Saved {filename}")

for category, items in categories.items():
    transactions=generate_transactions(category, items)
    save_to_csv(category, transactions)

