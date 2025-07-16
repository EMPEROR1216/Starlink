# main.py

import pandas as pd
from comparable_agent import ComparableAgent

def print_menu():
    """Prints the main menu for the CLI."""
    print("\n--- Starboard AI Agent CLI ---")
    print("1. Fetch Cook County Industrial Property Data")
    print("2. Find Comparables for a Property")
    print("3. Exit")
    print("------------------------------")

def main():
    """Main entry point for the command-line application."""
    agent = ComparableAgent()
    industrial_data = pd.DataFrame()

    while True:
        print_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            print("\n[INFO] Agent starting data extraction process...")
            industrial_data = agent.find_and_process_data()
            if not industrial_data.empty:
                print(f"[SUCCESS] Data extraction complete. Found {len(industrial_data)} properties.")
                print("Data saved to 'cook_data.csv'.")
            else:
                print("[ERROR] Could not fetch data. Check 'data_extraction.log' for details.")

        elif choice == '2':
            if industrial_data.empty:
                print("\n[WARNING] No data loaded. Please run option 1 first.")
                continue

            print("\n--- Find Comparable Properties ---")
            pin_input = input("Enter the Property Identification Number (PIN) to analyze: ").strip()
            
            # Call the agent to perform the core task
            comparables_df = agent.find_comparables(pin_input, industrial_data)

            if comparables_df.empty:
                print(f"[INFO] Could not find comparables for PIN: {pin_input}. It may not exist in the dataset.")
            else:
                print(f"\n[SUCCESS] Top 5 Comparables for PIN {pin_input}:")
                # Displaying relevant columns for clarity
                display_cols = ['property_identification_number', 'square_footage', 'year_built', 'confidence_score']
                print(comparables_df[display_cols])

        elif choice == '3':
            print("Exiting agent. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()