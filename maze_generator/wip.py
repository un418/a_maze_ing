class test:
    @staticmethod
    def print_close(bit: int):
        baseset = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
        newset = set(n for n in baseset if n & bit)
        print(newset)


if __name__ == "__main__":
    test.print_close(8)
