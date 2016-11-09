import sys
import pprint
import wptools

#Gets an image using wptools
def getImage(entity_name):
	q = wptools.page(entity_name,silent=True).get_query()
        img_url = ""
        try:
            img_url = q.pageimage
        except:
            img_url = q.images[0]['url']
	return img_url


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
        d['img'] = getImage(text)

    return d

if __name__ == '__main__':
    d = getdata('../private/index/' , sys.argv[1])
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(d)
