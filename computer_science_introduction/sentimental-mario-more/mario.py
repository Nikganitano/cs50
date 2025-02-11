# Pyramid of hashtags with a height of the user's choice - Problem set 6 (2/5)

def print_row(length, height):
    # Left half of the pyramid
    left_half = " " * (height - length) + "#" * length
    # Gap of 2 spaces
    gap = "  "
    # Right half of the pyramid (same as the left half without leading spaces)
    right_half = "#" * length
    # Combine all parts and print
    print(left_half + gap + right_half)

def main():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                break
            else:
                print("Please enter a positive integer no greater than 8.")
        except ValueError:
            print("Please enter a valid integer.")

    for i in range(height):
        print_row(i + 1, height)

if __name__ == "__main__":
    main()
