from pytube import Search

# constant and credentials
CHANNELS = [
    "Network Chuck",
    "fireship io",
    "Kevin Powell",
    "Tech with Tim",
    "Mental Outlaw",
    "Leo's Bag Of Tricks",
    "Techno Tim",
    "Computerphile",
    "No Boilerplate",
    "ElectroBoom",
    "GreatScott",
    "Zaney",
    "DistroTube",
    "sentdex",
    "Engineer Man",
    "NoMagic"
]


#taking_input
key = input("Please enter the concept that you would like explore: ")

# scraping

for channel in CHANNELS:
    s = Search(f'{key} {channel}')
    vid = s.results[0]
    print(vid.title)
    streams = vid.streams.filter(only_audio=True)
    stream = streams[0]
    stream.download()

          