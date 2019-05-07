import urllib.request

for i in range(1697):
    avatarpath = "https://sguru.org/wp-content/uploads/2017/06/steam-avatar-profile-picture-" + str(i).zfill(4) + ".jpg"
    # Write data to file
    filename = "./media/steam-avatar-profile-picture-" + str(i).zfill(4) + ".jpg"
    print(avatarpath)
    urllib.request.urlretrieve(avatarpath, filename)