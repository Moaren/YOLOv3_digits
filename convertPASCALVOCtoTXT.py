import sys
import os
import argparse
from bs4 import BeautifulSoup as soup 

parser = argparse.ArgumentParser(description='Convert XML Pascal VOC style annotations to one txt file ready for YOLO training.')
parser.add_argument('--pascal_path', help='Path to Darknet cfg file.', default='data/annotations/')
parser.add_argument('--output_name', help='Path to output Keras model file.', default='annotations.txt')

def convertVOCtoTXT(handler):
    xml_data = soup(handler, 'lxml')

    classCorrespondance = {
        '10': '0',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
    }

    line = xml_data.find('filename').text 
    
    for obj in xml_data.find_all('object'):
        line += ' ' + \
        obj.find('xmin').text + ',' + \
        obj.find('ymin').text + ',' + \
        obj.find('xmax').text + ',' + \
        obj.find('ymax').text + ',' + \
        classCorrespondance[obj.find('name').text]
    
    line += '\n'
    
    return line

def main(args):
    print('[INFO] Converting VOC style to YOLO txt')
    
    # Iterate thourgh the directories
    for subdir, _, files in os.walk(args.pascal_path):
        print('[INFO] Working on: ' + str(subdir))
        print(os.pardir)
        txt = ''
        if(not files):
            continue
        files.sort()
        for _file in files:
            print('>>> File: ' + str(_file))
            if str(_file).lower().endswith('.xml'):
                try:
                    handler = open(os.path.join(subdir, _file)).read()
                except Exception as e:
                    print('[ERROR] Reading file: ' +
                            str(os.path.join(subdir, _file)))
                    sys.exit(0)
                    
                # Convert files
                line = convertVOCtoTXT(handler)
                txt += line

        with open(subdir + '_' + args.output_name, 'w') as f:
            f.write(txt)
    print('[INFO] Done converting VOC style to YOLO txt')

if __name__ == '__main__':
    main(parser.parse_args())