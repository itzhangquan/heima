import xmltodict
xml="<xml>""<name>zhangsan</name>""<age>18</age>""</xml>"

dict=xmltodict.parse(xml)
print dict

xml2=xmltodict.unparse(dict)
print xml2
