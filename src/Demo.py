import re

def test():
    content = "dependencies {\ntraytry\n}"
    pattarn = "dependencies {(.*?)}"
    tStr = "\n    implementation fileTree(include: ['*.jar'], dir: 'libs')\n"
    #tStr = re.sub("\d+", "222", "hello 123 world 456")
    content1 = re.findall(pattarn, content, flags=re.DOTALL)
    result = content.replace(content1[0], tStr)
    print (content1[0])

test()