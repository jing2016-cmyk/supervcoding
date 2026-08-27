from collections import Counter


def main():
    number_of_strings, string_length = map(int, input().split())

    for _ in range(number_of_strings):
        text = input().strip()
        frequency = Counter(text)
        alternating = True

        for index in range(1, string_length):
            previous_is_heavy = frequency[text[index - 1]] > 1
            current_is_heavy = frequency[text[index]] > 1

            if previous_is_heavy == current_is_heavy:
                alternating = False
                break

        print("T" if alternating else "F")


if __name__ == "__main__":
    main()
