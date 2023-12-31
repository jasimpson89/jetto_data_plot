import json
import os
def read_data(input_file):

    """
    :param input_file: string with path to input file to be used
    :return: dictionary from JSON plus a notes fiels

    This read a text file made up of JSON + notes field which comprises of MARKDOWN

    Frist we read the file, strip out the notes

    Because the json is ordered we write back to a file to be read as that was the easiest thing to do
    """

    file = open(input_file,'r')
    json_string =''
    mardown_string = ''
    lines = file.readlines()
    markdown_flag = False
    try:
        path = './temp_json.json'
        temp_json_file = open(path,'w')
    except PermissionError:
        # the debugger needs whole path to work
        path = '/home/jsimpson/work/jetto/python_script/jetto_datadashboard/temp_json.json'
        temp_json_file = open(path,'w')
    for line in lines:
        if markdown_flag:
            mardown_string = mardown_string + line

        if line.startswith("%#"):
            # Markdown data:
            markdown_flag = True
        if markdown_flag == False:
            #Write out pure JSON
            temp_json_file.write(line)

    # must close for write to happen
    temp_json_file.close()


    with open(path) as f:
        input_data = json.load(f)

    input_data["notes"] = mardown_string

    # Clean up temp json file
    os.remove(path)
    return input_data