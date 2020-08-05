import string

def replaceContext(text, replObj):
    for key, value in replObj.items():
        if key != None and value != None:
            searchPattern = '<'+key+'>'
            if text.find(searchPattern) > 0:
                text = text.replace(searchPattern, '*'+str(value)+'*')
    return text

def removeNewline(text):
    return text.replace('\n', ' ')

def properNoun(text):
    return string.capwords(text)
