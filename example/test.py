import instapy
import database
import gender
from time import sleep

instapy.start("username", "password", True)
g = gender.GenderDetector()

skip_male = False
expand_todo = True

while True:
    try:
        user = database.get_next_todo_and_remove()
        if user is None:
            break

        if database.user_in_database(user):
            break

        gender = g.get_gender(user).gender
        if skip_male and gender == "m":
            print("skipping " + user)
            print("--------")
            continue

        print("goto_user: " + str(instapy.goto_user(user)))

        username = instapy.get_username()
        print("username: " + username)
        database.add_user(username)

        verified = instapy.is_verified()
        print("verified: " + str(verified))
        database.add_verified(username, verified)

        path = "Images/" + username + ".png"
        print("profile_image: " + str(instapy.download_profile_image(path)))
        database.add_profile_image(username, path)

        subscriber_amount = instapy.get_subscriber_amount()
        print("sub_amount: " + str(subscriber_amount))
        database.add_subscriber(username, subscriber_amount)

        subscribed_to_amount = instapy.get_subscribed_to_amount()
        print("sub_to_amount: " + str(subscribed_to_amount))
        database.add_subscribed_to(username, subscribed_to_amount)

        post_amount = instapy.get_post_amount()
        print("post_amount: " + str(post_amount))
        database.add_post_amount(username, post_amount)

        is_private = instapy.is_profile_private()
        print("private: " + str(is_private))
        database.add_is_private(username, is_private)

        bio_info = instapy.get_profile_bio_info()
        print("bio_info: " + bio_info)
        database.add_bio_info(username, bio_info)

        database.add_gender_guess(username, gender)

        if expand_todo:
            following_list = instapy.get_following_list()
            print("following_list_len: " + str(len(following_list)))
            database.add_list_to_todo(following_list)

        instapy.follow_profile()

        print("--------")
    except Exception as ex:
        print("error: " + str(ex))
