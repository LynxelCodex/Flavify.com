import urllib.request, json, urllib.parse, re

songs = [
  ('Musika', 'Dionela'),
  ('Oksihina', 'Dionela'),
  ('153', 'Dionela'),
  ('Suyo', 'Dionela'),
  ('Bahaghari', 'Dionela'),
  ('Bakit Pa Ba', 'Jay R'),
  ('Design', 'Jay R'),
  ('Ngayoy Naririto', 'Jay R'),
  ('Kung Mahal Mo Siya', 'Jay R'),
  ('Alam Mo Ba Girl', 'Hev Abi'),
  ('Walang Alam', 'Hev Abi'),
  ('Welcome2DTQ', 'Hev Abi'),
  ('LK', 'Hev Abi'),
  ('B.A.D.', 'Denise Julia feat. P-Lo'),
  ('NVMD', 'Denise Julia'),
  ('Sugar n Spice', 'Denise Julia'),
  ('Give Me Your Forever', 'Zack Tabudlo'),
  ('Fallin', 'Zack Tabudlo'),
  ('Pahinga', 'Al James'),
  ('Ngayon Lang', 'Al James'),
  ('Dilaw', 'Maki'),
  ('Saan?', 'Maki'),
  ('Namumula', 'Maki'),
  ('Na Na Na', 'BINI'),
  ('Tingin', 'Cup of Joe & Janine Teñoso'),
  ('Misteryoso', 'Cup of Joe'),
  ('Sagada', 'Cup of Joe'),
  ('Pelikula', 'Janine Teñoso feat. Arthur Nery'),
  ('White Toyota', 'SunKissed Lola'),
  ('RomCom', 'Rob Deniel')
]

for title, artist in songs:
    query = f'{title} {artist} audio'
    url = 'https://www.youtube.com/results?search_query=' + urllib.parse.quote(query)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode()
        match = re.search(r'"videoId":"([^"]+)"', html)
        if match:
            print(f'{title}: {match.group(1)}')
        else:
            print(f'{title}: NOT FOUND')
    except Exception as e:
        print(f'{title}: ERROR {e}')
