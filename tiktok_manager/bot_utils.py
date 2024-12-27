import string, secrets, subprocess, zlib

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
      
def subprocess_jsvmp(js, user_agent, url):
	proc = subprocess.Popen(['node', js, url, user_agent], stdout=subprocess.PIPE)
	return proc.stdout.read().decode('utf-8')

def crc32(content):
	prev = 0
	prev = zlib.crc32(content, prev)
	return ("%X" % (prev & 0xFFFFFFFF)).lower().zfill(8)