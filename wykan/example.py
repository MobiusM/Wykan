from wykan import Wykan

if __name__ == '__main__':
    wekan_url = "http://10.0.0.5/"
    username = "levinson"
    password = "123456"
    Wykan.verify_tls=False
    wekan = Wykan(wekan_url, username, password)

    all_users = wekan.get_all_users()
    wekan.get_user("kPEmhfAFwJYwNRCp9")
    print("breakpoint")
