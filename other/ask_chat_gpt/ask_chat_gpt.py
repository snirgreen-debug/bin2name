import openai
import csv
from time import sleep

openai.api_key = "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"
MAX_TOKENS = 2500

def parse_asm_txt_file(file_path):
    start_func = "-----function_start-----\n"
    end_func = "-----function_end-----\n"
    data = []
    eof = False
    with open(file_path, 'r') as f:
        while not eof:
            func_name = ""
            func_data = ""
            while True:
                line = f.readline()
                if line == start_func:
                    func_name = f.readline()
                elif func_name and ':' in line:
                    continue
                elif line == end_func:
                    data.append((func_name, func_data))
                    break
                elif not line:
                    eof = True
                    break
                else:
                    func_data += line
    return data


def set_query(func_text):
    return "Name the following assembly function:\n" + func_text

def main():
    file_path = "otherfuncs.txt"
    functions = parse_asm_txt_file(file_path)
    for func_name, func_text in functions:
        csv_file = open("chat_gpt_data.csv", 'a')
        query = set_query(func_text)
        try:
            full_response = openai.Completion.create(
                model="text-davinci-003",
                prompt=query,
                temperature=0.6,
                max_tokens=MAX_TOKENS,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1,
                timeout=60  # Wait 60 seconds maximum
            )
            response = full_response.choices[0].text
        except Exception as e:
            response = "an error occurred.\n" + str(e)
        print(response)
        csv_file.write(','.join([func_name, func_text.replace('\n', '\\n'), query.replace('\n', '\\n'), response.replace('\n', '\\n')]))
        # csv_file.write(','.join(['a', 'a', 'a', 'a', '\n']))
        sleep(10)
        csv_file.close()


if __name__ == "__main__":
    main()
    # print(parse_asm_txt_file("otherfuncs - Copy.txt"))
