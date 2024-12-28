import instaloader

def reel_download(username):
    ig = instaloader.Instaloader()
    count = 0

    try:
        id = instaloader.Profile.from_username(ig.context, username=username)
        for post in id.get_posts():
            if post.typename == "GraphVideo":
                count += 1
                ig.download_post(post, target=f"{username}_reel")
                print(f"Downloaded {post.shortcode}")
            if count >= 1 :
                break
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    username = "legendofnexus"
    reel_download(username)