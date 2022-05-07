from tinytag import TinyTag

media_file = ["10MB.wav", "2o6MB.wav"]

for j in media_file :
    i = TinyTag.get(j)
    print(type(i))
    print("Title : " + i.title)
    print("Artist : " + i.artist)
    print("Filesize: " + str(i.filesize) + " bytes")
    
