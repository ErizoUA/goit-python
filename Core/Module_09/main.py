from parsers import parser_user_input


def main():

    while True:
        user_input = input('Enter Command: ').lower().strip()
        try:
            result = parser_user_input(user_input)
            print(result)
        except SystemExit as error:
            print(error)
            break


if __name__ == '__main__':
    main()
