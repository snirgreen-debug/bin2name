import requests

url = "localhost"
port = 4532
final_url = 'http://' + url + ':' + str(port) + '/'


def main():
    files = {'bin_file': open('test_file.txt', 'rb')}
    r = requests.post(final_url, params=files)


if __name__ == "__main__":
    main()
