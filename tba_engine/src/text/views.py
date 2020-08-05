import src.text.textIO as txt

def bashBlockPrint(msg_block):
    txt.printGameBlock(msg_block)
    return msg_block

def bashRawPrint(msg_block):
    print(msg_block)
    return msg_block

def htmlPrint(msg_block):
    return txt.formatHtmlBlock(msg_block)

