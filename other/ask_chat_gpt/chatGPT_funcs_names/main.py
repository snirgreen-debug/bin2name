import openai, os
from time import sleep
from csv import writer

openai.api_key = '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'
FUNC_DIR = './functions'
RESULTS_FILE = './results.csv'


class Message:
    def __init__(self, func=''):
        self.msg = "what is the best name of the following asm function:\n" + func + '\n The answer should be 1-7 words'

    def send_msg(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": self.msg},
            ]
        )

        result = ''
        for choice in response.choices:
            result += choice.message.content
        return result


def get_all_funcs(funcs_dir):
    for filename in os.listdir(funcs_dir):
        with open(os.path.join(funcs_dir, filename), 'r') as f:
            yield '\n'.join(f.readlines())
            f.close()

def save_result(chatGPT_result, orig_func_name='BinarySearch', model_func_name='BinarySearch'):
    with open(RESULTS_FILE, 'a') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow([orig_func_name, model_func_name, chatGPT_result])
        csv_file.close()

def main():
    for func in get_all_funcs(FUNC_DIR):
        msg = Message(func)
        result = msg.send_msg()
        print(result)
        save_result(result)
        # sleep(3)


if __name__ == '__main__':
    main()
