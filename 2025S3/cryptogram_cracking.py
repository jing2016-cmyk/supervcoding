def find_cipher_character(s, c):
    """
    Find the c-th character in an infinitely repeating RLE-encoded pattern.
    
    The pattern is encoded using Run-Length Encoding (RLE), where consecutive
    repeated characters are replaced with the character followed by its count.
    For example, "aaaabccdddd" becomes "a4b1c2d4".
    
    Args:
        s: RLE-encoded pattern string (e.g., "a4b1c2d10")
        c: Index of the character to find (0-indexed)
    
    Returns:
        The character at index c in the infinitely repeating pattern
    """
    # Parse the RLE string into (character, count) pairs
    pattern = []
    i = 0
    while i < len(s):
        char = s[i]
        i += 1
        num_str = ""
        while i < len(s) and s[i].isdigit():
            num_str += s[i]
            i += 1
        count = int(num_str)
        pattern.append((char, count))
    
    # Calculate the total length of one pattern cycle
    pattern_length = sum(count for char, count in pattern)
    
    # Find the position within a single pattern using modulo
    position_in_pattern = c % pattern_length
    
    # Find the character at that position
    current_pos = 0
    for char, count in pattern:
        if current_pos + count > position_in_pattern:
            return char
        current_pos += count
    
    return None


if __name__ == "__main__":
    # Read input
    s = input().strip()
    c = int(input().strip())
    
    # Find and output the character
    result = find_cipher_character(s, c)
    print(result)
