def flames_game(name1, name2):
    """
    Determine the relationship between two names using the FLAMES method.
    :param name1: First person's name
    :param name2: Second person's name
    :return: The relationship as a string
    """
    # Remove spaces and convert names to lowercase
    name1 = name1.replace(" ", "").lower()
    name2 = name2.replace(" ", "").lower()
    if name1 == "tanujairam" or name2 == "tanujairam" or name1 == "rupali" or name2 == "rupali":
        return "You can't play the game with my owner, lol.😜"
    
    # Remove common letters
    for letter in name1[:]:
        if letter in name2:
            name1 = name1.replace(letter, "", 1)
            name2 = name2.replace(letter, "", 1)
    
    # Total remaining letters
    total = len(name1) + len(name2)
    
    # FLAMES mapping
    flames = ["F", "L", "A", "M", "E", "S"]
    while len(flames) > 1:
        index = (total % len(flames)) - 1
        if index >= 0:
            flames = flames[index + 1:] + flames[:index]
        else:
            flames.pop()
    
    # Final result
    relationships = {
        "F": "Friends",
        "L": "Love",
        "A": "Affection",
        "M": "Marriage",
        "E": "Enemies",
        "S": "Siblings"
    }
    return relationships[flames[0]]


# Optional interactive CLI interface
if __name__ == "__main__":
    print("Welcome to the FLAMES Game!")
    name1 = input("Enter the first name: ").strip()
    name2 = input("Enter the second name: ").strip()
    result = flames_game(name1, name2)
    print(f"The relationship between {name1} and {name2} is: {result}")
