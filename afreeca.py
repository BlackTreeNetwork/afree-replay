from xml.etree.ElementTree import Element, parse
import requests
import sys
import subprocess
import signal
import threading
import os

def download_from(url, filename):
    resp = requests.get(url)
    f = None
    with open(filename, "wb") as file:
        file.write(resp.content)
        f = file
        f.close()
    return f

def process(url, bj_name, output):
    os.system("ffmpeg -i {u} -c copy ./{bj}/{out}".format(u=url, out=output, bj=bj_name))

if __name__ == "__main__":
    url = None
    if len(sys.argv) > 1:
        url = sys.argv[1]
    f = None
    xml_filename = "{x}.xml".format(x=1)
    if not url is None:
        f = download_from(url, xml_filename)
    tree = parse(xml_filename)
    note = tree.getroot()
    bj_name = None
    for bj_element in note.iter('bj_id'):
        bj_name = bj_element.text

    if not os.path.exists(bj_name):
        os.mkdir(bj_name)
    
    for logo in note.iter('titleImage'):
        download_from(logo.text, "logo.jpg".format(bj=bj_name))
        os.rename("logo.jpg", "./{bj}/logo.jpg".format(bj=bj_name))
    t = None
    for file_node in note.iter('file'):
        ip_address = file_node.text
        if file_node.get('key') is None:
            continue
        output_file = file_node.get('key') + ".mp4"
        t = threading.Thread(target=process, args=(ip_address, bj_name, output_file))
        t.start()
    t.join()
