import requests

url = "www.binary2name.com"
port = 4443
final_url = 'https://' + url + ':' + str(port) + '/'


def main():
    files = {'bin_file': open('test_file.txt', 'rb')}
    r = requests.post(final_url, params=files)


if __name__ == "__main__":
    main()
