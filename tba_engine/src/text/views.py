import src.text.textIO as txt

def bashBlockPrint(msg_block):
    txt.printGameBlock(msg_block)
    return msg_block

def bashRawPrint(msg_block):
    print(msg_block)
    return msg_block

def bashPrint(msg_block):
    msg_block = txt.formatHtmlBlock(msg_block)
    if isinstance(msg_block, str):
        print(msg_block.replace('<br>', '\n'))
    else:
        for msg in msg_block:
            print(msg.replace('<br>', '\n'))

def htmlPrint(msg_block):
    print('htmlPrint')
    return txt.formatHtmlBlock(msg_block)

