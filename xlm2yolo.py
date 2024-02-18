import xml. etree. ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os. path import join
import glob
# classes =["3_yueyawan", "9_zhehen", "6_siban", "4_shuiban", "2_hanfeng", "7_yiwu", "5_youban", "8_yahen", "1_chongkong", "10_yaozhe"]
classes = ["6_siban", "4_shuiban", "7_yiwu", "2_hanfeng", "3_yueyawan", "10_yaozhe", "5_youban", "9_zhehen"]
# HERE NEED TO CHANGE

def convert(size, box):
    dw=1./size[0]
    dh =1./size[1]
    x = (box[0] + box[1]) / 2.0
    y=(box[2]+box[3])/2.0
    w=box[1] -box[0]
    h = box[3] - box[2]
    x=x*dw
    w=w*dw
    y= y*dh
    h =h*dh
    return(x,y,w,h)

def convert_annotation(image_name):
    in_file=open('./New_GC-DET/New_GC-DET/labels/val2017xml/'+image_name[: -3]+'xmL') # HERE NEED TO CHANGE
    out_file=open('./New_GC-DET/New_GC-DET/labels/val2017'+image_name[: -3]+'txt', 'w') # HERE NEED TO CHANGE
    tree=ET. parse(in_file)
    root=tree. getroot()
    size=root.find('size')
    w=int(size.find('width').text)
    h=int(size. find( 'height'). text)
    for obj in root.iter('object'):
        cls=obj. find('name').text
        if cls not in classes:
            print(cls)
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text),
            float(xmlbox.find('xmax').text),
            float(xmlbox.find('xmin').text),
            float(xmlbox.find('xmax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb])+'\n')

wd = getcwd()

if __name__ == '__main__':
    for image_path in glob.glob(r"./New_GC-DET/New_GC-DET/images/val2017/*.jpg"): # HERE NEED TO CHANGE
        image_name = image_path.split('\\')[-1]
    # print (imege path)
        convert_annotation(image_name)

