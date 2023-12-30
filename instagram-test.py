import io
import sys
import requests
sys.path.append("~/Scripts/femboyslove/femboysloveloona")
import time
from instaloader import instaloader
import test_library
if __name__ == "__main__":
    # exit(0)
    L = instaloader.Instaloader()
    profileobj = instaloader.Profile.from_username(L.context, 'trash') # Get loonas official account posts n data

    def get_latest_post(profile_object):
        # global profilobj
        profile_object = instaloader.Profile.from_username(L.context, 'trash')
        for post in profile_object.get_posts():
            if not post.is_video:
                print("last post ->", post.shortcode)
                return post, post.shortcode
                break
    
    _, last_post_id = get_latest_post(profileobj)
    prt = None
    while True:
        time.sleep(10)
        postobj, latest_post_id = get_latest_post(profileobj)
        if latest_post_id != last_post_id:
            if not prt: prt = test_library.create_prt_object()
            response = requests.get(postobj.url)
            container = io.BytesIO(response.content)
            test_library.print_image(prt, container)
            exit()
            # ...
        else:
            print("Nothing changed.")
        last_post_id = latest_post_id