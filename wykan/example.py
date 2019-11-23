from wykan import Wykan

if __name__ == '__main__':
    wekan_url = "http://10.0.0.5/"
    username = "levinson"
    password = "123456"
    Wykan.verify_tls = False
    wekan = Wykan(wekan_url, username, password)
    print("Init wekan")

    all_users = wekan.get_all_users()
    print("got all users")
    by_id = wekan.get_user("kPEmhfAFwJYwNRCp9")
    print("got user by id")
    by_username = wekan.get_user_by_username("levinson")
    print("got user by username")

    new_user = wekan.create_new_user("bis-hanich-test2", "hanich-mail@school.notreall", "Aa123456")
    print("breakpoint")
