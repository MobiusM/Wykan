from wykan import Wykan

if __name__ == '__main__':
    wekan_url = "http://10.0.0.5/"
    username = "levinson"
    password = "123456"
    Wykan.verify_tls = False
    wekan = Wykan(wekan_url, username, password)
    print("Init wekan")

    levinson = wekan.get_user_by_username("levinson")
    # test_user = wekan.get_user_by_username("test_user")
    print("got levinson by username")
    # new_user = wekan.create_new_user("test_user", "test_user@schooll.dommm", "Aa12345")
    # print("created new user")
    # new_board = wekan.create_board("my new test board", test_user.id)

    # test_user_boards = wekan.get_user_boards(test_user.id)
    # target_board = test_user_boards[2]

    # target_board.add_board_member(levinson.id, True, False, False)
    # target_board.change_member_permissions(levinson.id, True, False, False)

    levinson_boards = wekan.get_user_boards(levinson.id)
    board_lists = levinson_boards[3].get_lists()
    print("breakpoint")
