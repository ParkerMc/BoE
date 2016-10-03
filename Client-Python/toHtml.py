def toHtml(text):
    real_output = ""
    for i in text.split("\n"):
        output = _replace(i, "*", "<b>", "</b>")
        output = _replace(output, "-", "<s>", "</s>")
        output = _replace(output, "_", "<u>", "</u>")
        output = _replace(output, "~", "<i>", "</i>")
        real_output += _replace(output, "`", "<code>", "</code>") + "<br>"
    return real_output


def _replace(text, replace, replacementb, replacemente):
    output = ""
    num = 0
    last = ""
    for i in text.split(replace):
        if num == 0:
            num += 1
            output += i
        elif num == 1:
            num += 1
            last = i
        else:
            print str(i)[-1]
            output += replacementb + last + replacemente + i
            num = 1
    if num == 2:
        output += last
    return output
