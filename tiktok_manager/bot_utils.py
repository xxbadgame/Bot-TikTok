import string, secrets

def generate_random_string(length, underline):
    characters = (
        string.ascii_letters + string.digits + "_"
        if underline
        else string.ascii_letters + string.digits
    )
    random_string = "".join(secrets.choice(characters) for _ in range(length))
    return random_string

def print_response(r):
	print(f"{r.status_code}")
	print(f"{r.content}")

def print_error(url, r):
	print(f"[-] An error occured while reaching {url}")
	print_response(r)

def assert_success(url, r):
    if r.status_code != 200:
        print_error(url, r)
    return r.status_code == 200

def convert_tags(text, session):
	end = 0
	i = -1
	text_extra = []