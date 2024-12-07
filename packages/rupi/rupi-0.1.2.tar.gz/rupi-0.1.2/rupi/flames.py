# flames.py inside the 'rupi' package

def flames_game(name1, name2):
    # Convert names to lowercase to make the comparison case-insensitive
    name1 = name1.lower()
    name2 = name2.lower()

    # Check if the names are "Tanujairam" or "Rupali"
    if name1 == "tanujairam" or name2 == "tanujairam" or name1 == "rupali" or name2 == "rupali":
        return "You can't play the game with my owner, lol."

    # List of FLAMES categories
    flames_categories = ['Friends', 'Love', 'Affection', 'Marriage', 'Enemy', 'Siblings']
    
    # Remove spaces and lowercase the names for calculation
    name1 = name1.replace(" ", "").lower()
    name2 = name2.replace(" ", "").lower()

    # Step 1: Calculate the number of common letters between the two names
    common_count = sum(min(name1.count(c), name2.count(c)) for c in set(name1))

    # Step 2: Subtract the common count from the total length of both names
    total_count = len(name1) + len(name2) - 2 * common_count

    # Step 3: Use the total_count to find the FLAMES category by looping through the list
    flames_index = total_count % len(flames_categories)
    result = flames_categories[flames_index]

    return result


# Main code to ask user for input
if __name__ == "__main__":
    # Get the names from the user
    name1 = input("Enter the first name: ")
    name2 = input("Enter the second name: ")

    # Call the flames_game function with the names provided by the user
    result = flames_game(name1, name2)

    # Print the result
    print(f"The relationship between {name1} and {name2} is: {result}")
