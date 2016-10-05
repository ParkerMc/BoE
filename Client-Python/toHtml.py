import re
def toHtml(text):
    real_output = ""
    for i in text.split("\n"):
        output = re.sub('\*(.*?)\*', r'<b>\1</b>', i.replace("\\*", "<temp>")).replace("<temp>", "*")
        output = re.sub('-(.*?)-', r'<s>\1</s>', output.replace("\\-", "<temp>")).replace("<temp>", "-")
        output = re.sub('_(.*?)_', r'<u>\1</u>', output.replace("\\_", "<temp>")).replace("<temp>", "_")
        output = re.sub('~(.*?)~', r'<i>\1</i>', output.replace("\\~", "<temp>")).replace("<temp>", "~")
        output = re.sub('`(.*?)`', r'<code>\1</code>', output.replace("\\`", "<temp>")).replace("<temp>", "`")
        real_output += re.sub('\[(.*?)\]\((.*?)\)', r"""<a href="#" onclick="RunOnPython.openUrl('\2');">\1</a>""", output) + "<br>"
    return real_output
