#encoding: UTF-8

import urllib2
import os
import tensorflow as tf
import requests
from PIL import Image

FLAGS = tf.app.flags.FLAGS;
tf.app.flags.DEFINE_string(
    'datafile', '~/workspace/ai/imagenet/fall09_urls.txt',
    """data set list"""
)
tf.app.flags.DEFINE_string(
    'tmpdir', '/tmp/imagenet/original/',
    """for original files"""
)
tf.app.flags.DEFINE_string(
    'imagedir', '/tmp/imagenet/',
    """bmp converted files"""
)

def isValid(image): # 이미지 없음을 알려주는 이미지 판별
    Valid = True
    pixel = image.getpixel((1, 1))
    print pixel
    for i in range(2, 11):
        print image.getpixel((i, i))
        if (pixel != image.getpixel((i, i))):
            Valid = False
            break
    return Valid

def download(datafile, target = FLAGS.imagedir, tmp = FLAGS.tmpdir):
    classlist = []
    imagelist = []

    if not tf.gfile.Exists(datafile):
        tf.logging.fatal('File does not exists %s', datafile)
    if not os.path.isdir(target):
        os.mkdir(target)
    if not os.path.isdir(tmp):
        os.mkdir(tmp)

    l = 3
    for line in file(datafile):
        urlinfo = line[:-1].split('\t')
        url = urlinfo[1]
        name = urlinfo[0]
        classname = name.split('_')[0]
        if not classname in classlist:
            if (len(classlist) < 1000):
                classlist.append(classname)
                l -= 1
                if (l <= 0):
                    break
            else:
                continue
        try:
            with open(tmp + name, 'wb') as f:
                f.write(urllib2.urlopen(url).read());
            bitmap = Image.open(tmp + name)
            if (isValid(bitmap)):
                bitmap.save(target + name + '.bmp')
                imagelist.append(urlinfo)
        except urllib2.HTTPError:
            pass
        except IOError:
            pass
        except:
            raise
            pass
    with open('list', 'w') as f:
        for image in imagelist:
            f.write('\t'.join(image))
            f.write('\n');

def main(_):
    download(FLAGS.datafile)

if __name__ == '__main__':
    tf.app.run();
