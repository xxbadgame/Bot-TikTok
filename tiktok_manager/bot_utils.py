import string, secrets, subprocess, zlib, re

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

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

	def text_extra_block(start, end, type, hashtag_name, user_id, tag_id):
		return {
			"end": end,
			"hashtag_name": hashtag_name,
			"start": start,
			"tag_id": tag_id,
			"type": type,
			"user_id": user_id
		}

	def convert(match):
		nonlocal i, end, text_extra
		i += 1
		if match.group(1):
			text_extra.append(text_extra_block(end, end + len(match.group(1)) + 1, 1, match.group(1), "", str(i)))
			end += len(match.group(1)) + 1
			return "<h id=\"" + str(i) + "\">#" + match.group(1) + "</h>"
		elif match.group(2):
			url = "https://www.tiktok.com/@" + match.group(2)
			headers = {
				'authority': 'www.tiktok.com',
				'accept': '*/*',
				'accept-language': 'q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5,vi;q=0.4',
				'user-agent': user_agent
			}

			r = session.request("GET", url, headers=headers)
			user_id = r.text.split('webapp.user-detail":{"userInfo":{"user":{"id":"')[1].split('"')[0]
			text_extra.append(text_extra_block(end, end + len(match.group(2)) + 1, 0, "", user_id, str(i)))
			end += len(match.group(2)) + 1
			return "<m id=\"" + str(i) + "\">@" + match.group(2) + "</m>"
		else:
			end += len(match.group(3))
			return match.group(3)

	result = re.sub(r'#(\w+)|@([\w.-]+)|([^#@]+)', convert, text)
	return result, text_extra
      
def subprocess_jsvmp(js, user_agent, url):
	proc = subprocess.Popen(['node', js, url, user_agent], stdout=subprocess.PIPE)
	return proc.stdout.read().decode('utf-8')

def crc32(content):
	prev = 0
	prev = zlib.crc32(content, prev)
	return ("%X" % (prev & 0xFFFFFFFF)).lower().zfill(8)