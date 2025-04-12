def print_row(spaces, bricks1, bricks2, height):
    print(" " * (height - spaces) + "#" * bricks1 + "  " + "#" * bricks2)

def main():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                break
        except ValueError:
            pass

    for i in range(1, height + 1):
        print_row(i, i, i, height)

if __name__ == "__main__":
    main()
