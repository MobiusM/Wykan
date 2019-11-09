from wykan import Wykan


def main():
    api_url = "http://10.0.0.7/wekan"
    api = Wykan(api_url, {"username": "administrator", "password": "123456789"}, )

    boards = api.get_user_boards()

    boards[1].swimlanes()
    sleep()


if __name__ == '__main__':
    main()
