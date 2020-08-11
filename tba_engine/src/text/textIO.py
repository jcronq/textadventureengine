from termcolor import colored, cprint
import time
import re
import readline
from src.text.textUtils import removeNewline

colorMap = {
    'color_nar':"green",
    'color_env':"blue",
    'color_item':"magenta",
    'color_loc': 'red',
    'color_util':"red"
}

ansiMap = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37',
    'reset': '0'
}

def addColor(txt, color_name):
    return f'\u001b[{ansiMap[color_name]}m{txt}\u001b[0m'

def cPrint(color_name, txt):
    cprint(txt, color_name)

def setColor(color_name, value):
    colorMap[color_name] = value

def getInput(startChar= "> "):
    print(startChar, end="")
    inStr = input().strip()
    return inStr

def getYesNo(prompt = "> "):
    inStr = getInput(startChar = prompt).lower()
    while(inStr != "yes" and inStr != "y" and inStr != "no" and inStr != "n"):
        if inStr == 'quit' or inStr == ':q':
            quit()
        printGameBlock("...I was really just looking for a 'yes' or a 'no'.")
        inStr = getInput()
    return inStr == "yes" or inStr == 'y'

def getStr(prompt, prompt_end=":", default=None):
    if default is not None:
        prompt += colored(f" ({default}){prompt_end} ", "blue")
    else:
        prompt += f"{prompt_end} "
    inStr = getInput(startChar = prompt)
    if inStr == 'quit' or inStr == ':q':
        quit()
    if default is not None and len(inStr) == 0:
        inStr = default
    confirmed = False
    # while not confirmed:
    while len(inStr) <= 0:
        printGameBlock("No input was entered.")
        inStr = getInput()
        if inStr == 'quit' or inStr == ':q':
            quit()
        if default is not None and len(inStr) == 0:
            inStr = default
        # printGameBlock(inStr)
        # confirmed = getYesNo("Is this OK?\n> ")
        # if not confirmed:
        #     inStr = ""
    return inStr

def utilPrint(msg):
    cprint(msg, colorMap['color_util'])

def colorize(txt, noMatchColor, colored_words):
    indexes = [];
    for colored_word in colored_words:
        searchWord = colored_word['word']
        color = colored_word['color']
        reg_ex = re.compile(r'(([ .,!?\n\t]|^){1}'+searchWord+'([ .,!?\n\t]|$){1})')
        res = reg_ex.findall(txt)
        index = -1
        if len(res) > 0:
            pattern = res[0][0]
            index = txt.find(pattern)
            word_len = len(pattern)
        if index >= 0:
            indexes.append({'end': index + word_len, 'start': index, 'color': color})
    indexes.sort(key=lambda i: i['start'])
    colorized_words = []
    for i, index in enumerate(indexes):
        if i == 0 and index['start'] != 0:
            colorized_words.append(colored(txt[0:index['start']],noMatchColor))
        colorized_words.append(colored(txt[index['start']:index['end']], index['color']))
        if i == len(indexes) - 1 and index['end'] != len(txt):
            colorized_words.append(colored(txt[index['end']:], noMatchColor))

    return ''.join(colorized_words)

def addColorsFromBlocks(txt, searchChar, noMatchColor, matchColor):
    charIndex = txt.find(searchChar)
    eolIndex = txt.find("\n")
    if(eolIndex < 0):
        eolIndex = len(txt)
    lines = []
    inBlock = False
    while charIndex >= 0 or eolIndex != len(txt):
        index = min(charIndex, eolIndex)
        if(index < 0):
            index = eolIndex
        line = txt[0:index]
        if inBlock:
            line = colored(line, matchColor)
        else:
            line = colored(line, noMatchColor)

        if(txt[index] == '\n'):
            addtext="\n"
        else:
            addtext=" "
            inBlock = not inBlock
        lines.append(line+addtext)
        txt = txt[index+1:len(txt)]
        charIndex = txt.find(searchChar)
        eolIndex = txt.find("\n")
        if(eolIndex < 0):
            eolIndex = len(txt)
    if(len(txt) > 0):
        lines.append(colored(txt, noMatchColor))
    return "".join(lines)

def wrapInBlock(txt, blockSize):
    blockLine = "_" * blockSize
    tailBlockLine = "=" * blockSize
    blockPrefix = "| "
    blockPostfix = " |"
    blockFixSize = len(blockPostfix) + len(blockPrefix)

    colorBlock = addColorsFromBlocks(txt, "*", colorMap['color_nar'], colorMap['color_env'])
    blockedColorBlock = colored(blockLine + "\n| ", 'white') + colorBlock.replace("\n", colored(" |\n| ", 'white')) + colored(" |\n", 'white') + tailBlockLine
    return blockedColorBlock

def fauxTypePrint(txt, wordsPerMinute):
    for ch in txt:
        print(ch, end = "")
        time.sleep((1/wordsPerMinute)/60)
    print("")

def wrapText(txt, blockSize = 40, offset = 0):
    words = txt.split(' ')
    lines = []
    line = " "*offset

    for word in words:
        if(len(line) + 1 + len(word) > blockSize+offset):
            spacer = " " * ((blockSize+offset)-len(line))
            line = line + spacer
            lines.append(line)
            line = (" " * offset) + word
        else:
            if(len(line) != offset):
                line = line + " "
            line = line + word

    spacer = " " * ((blockSize+offset)-len(line))
    line = line + spacer
    lines.append(line)
    return "\n".join(lines)

def wrapTextBlock(txt, blockSize = 40, offset = 0):
    if isinstance(txt, str):
        linesRaw = txt.splitlines()
    elif isinstance(txt, list):
        linesRaw = txt
    else:
        return "ERROR!!! input is neither a string or array"

    wrappedLines = []
    for rawLine in linesRaw:
        split_lines = rawLine.splitlines()
        for split_line in split_lines:
            wrappedLines.append(wrapText(split_line, blockSize - 4, offset))
    wrappedText = "\n".join(wrappedLines)

    return wrappedText

def printGameBlock(txt, blockSize=60, offset=0):
    new_txt = []
    if isinstance(txt, list):
        for i, line in enumerate(txt):
            new_txt.append(removeNewline(line).replace("<br>", " \n"))
            if i != len(txt) -1:
                new_txt.append(' ')
    else:
        new_txt.append(removeNewline(txt))
    wrappedText = wrapTextBlock(new_txt, blockSize, offset)
    block = wrapInBlock(wrappedText, blockSize)
    fauxTypePrint(block, 60)

def getOption(prompt, options, default_selection = -1, numeral_color='yellow', block_size = 40):
    print('')
    print(prompt)
    print('')

    for opt_num, line in enumerate(options):
        print(colored(f'{opt_num+1})', numeral_color), end='')
        option = wrapText(line, block_size, offset = 5)
        print(option[4:])

    selection = -1
    while selection < 0:
        try:
            user_input = input("> ").strip()
            if user_input == 'quit':
                return 'quit'
            elif user_input == '' and default_selection >= 0:
                return default_selection
            elif user_input.isnumeric():
                selection = int(user_input)-1
            else:
                selection = -1
        except:
            selection = -1
        if selection < 0 or selection > len(options)-1:
            print(f"Please select a number between 1-{len(options)}")
            if default_selection >= 0:
                print(f"You can also press enter to confirm the default selection: {default_selection}")
        else:
            return selection

def replaceWithColors(line):
    line = replaceWithColor(line, '*', colorMap['color_nar'])
    line = replaceWithColor(line, '@', colorMap['color_item'])
    line = replaceWithColor(line, '^', colorMap['color_loc'])
    line = replaceWithColor(line, '#', colorMap['color_env'])
    return line

def replaceWithColor(line, splitOn, color):
    splits = line.split(splitOn)
    result_list = []
    in_color_blk = False
    for index, split in enumerate(splits):
        if index == 0:
            result_list.append(split)
        elif in_color_blk:
            result_list.append(split)
            in_color_blk = False
        elif not in_color_blk:
            result_list.append(addColor(split, color))
            in_color_blk = True

    return ''.join(result_list)

def formatHtmlBlock(msg_block):
    new_txt = []
    if isinstance(msg_block, list):
        for i, line in enumerate(msg_block):
            normal_line = removeNewline(line)
            colored_line = replaceWithColors(normal_line)
            new_txt.append(colored_line)
            if i != len(msg_block) -1:
                new_txt.append(' ')
    else:
        colored_line = replaceWithColors(
            removeNewline(msg_block)
        )
        new_txt.append(colored_line)
    return new_txt

def promptInput(prompt, options):
    print(prompt)

    legal_keys = [option['key'] for option in options] + ['quit']

    opt_text = '<br>'.join(formatHtmlBlock("  ".join([
        f"#{option['key']}#: *{option['text']}*"
        for option in options
    ])))
    print(opt_text.replace('<br>', '\n'))

    cmd = ['']
    while cmd[0] not in legal_keys:
        try:
            cmd = input("> ").strip().split(' ')
            if cmd[0] == 'quit':
                return ['quit']
            elif cmd[0] not in legal_keys:
                print(f"Please select option from {legal_keys}")
                cmd = ['']
        except:
            cmd = ['']

    return cmd

