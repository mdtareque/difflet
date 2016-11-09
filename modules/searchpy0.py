import sys
import pprint

def getdata(path, text):

    with open(path + "/i"+text[:2].lower(),'r') as f:
        lines = f.readlines()

        d = {}
        read = False
        for no,line in enumerate(lines):
            if line.lower() == text.lower() + ':' + '\n':
                read = True
                continue

            if read == True:
                if line[-2:] != ',\n':
                    break
                line = line[:-2]
                line = line.split(':')
                key = line[0]
                values = ':'.join(line[1:])
                d[key] = values

    return d

if __name__ == '__main__':
    d = getdata('../private/index/' , sys.argv[1])
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(d)
