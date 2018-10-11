from xml.dom import minidom


def prettify(xml):
    reparsed = minidom.parseString(xml)
    return reparsed.toprettyxml(indent="\t")
