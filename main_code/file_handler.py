def save_to_file(path_to_file, data):
    open(path_to_file, "w").write(data)


def load_from_file(path_to_file):
    return open(path_to_file).read()

if __name__ == "__main__":
    p = get_filename()

    print(p)

    save_to_file(p, input())
    print(load_from_file(p))

