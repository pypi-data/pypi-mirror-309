def write_file(path, texte : str) :
    f = open(path, "wb")
    f.write(texte.encode("utf-8"))
    f.close()

def read_file(path):
    return open(path, "rb").read().decode("utf-8")