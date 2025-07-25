#!/usr/bin/env python3

import sys
from sample_data import generate_sample_data
from sales_analyzer import SalesAnalyzer
from csv_loader import CSVLoader

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [generate|load-csv|analyze]")
        print("  generate - Generate sample e-commerce data")
        print("  load-csv - Load data from CSV files")
        print("  analyze  - Analyze sales data and show report")
        return
    
    command = sys.argv[1].lower()
    
    if command == "generate":
        print("Generating sample e-commerce data...")
        generate_sample_data()
        print("Sample data generation completed!")
    
    elif command == "load-csv":
        print("Loading data from CSV files...")
        loader = CSVLoader("ecommerce_csv.db")
        loader.load_all_data()
        print("CSV data loading completed!")
    
    elif command == "analyze":
        print("Analyzing sales data...\n")
        db_file = "ecommerce_csv.db" if len(sys.argv) > 2 and sys.argv[2] == "--csv" else "ecommerce_sample.db"
        analyzer = SalesAnalyzer(db_file)
        analyzer.print_sales_report()
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: generate, load-csv, analyze")

if __name__ == "__main__":
    main()