import os
from tqdm import tqdm
from lxml import etree
import json

# Run this script to generate json file

# 读取 xml 文件信息，并返回字典形式
def parse_xml_to_dict(xml):
    if len(xml) == 0:  # 遍历到底层，直接返回 tag对应的信息
        return {xml.tag: xml.text}

    result = {}
    for child in xml:
        child_result = parse_xml_to_dict(child)  # 递归遍历标签信息
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:  # 因为object可能有多个，所以需要放入列表里
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}


# 提取xml中name保留为json文件
def xml2json(data):
    xml_path = [os.path.join(data, i) for i in os.listdir(data)]
    classes = []      # 目标类别
    num_object = 0
    for xml_file in tqdm(xml_path, desc="loading..."):
        with open(xml_file, encoding='gb18030', errors='ignore') as fid:      # 防止出现非法字符报错
            xml_str = fid.read()
        xml = etree.fromstring(xml_str)
        data = parse_xml_to_dict(xml)["annotation"]  # 读取xml文件信息
        if 'object' in data:  # 检查是否存在'object'键
            for j in data['object']:        # 获取单个xml文件的目标信息
                ob = j['name']
                num_object += 1
                if ob not in classes:
                    classes.append(ob)
    print(num_object)
    # 生成json文件
    labels = {}
    for index, object in enumerate(classes):
        labels[index] = object
    labels = json.dumps(labels, indent=4)
    with open('instances_val2017.json', 'w') as f:
        f.write(labels)



if __name__ == "__main__":
    root = './New_GC-DET/New_GC-DET/ANNOTATIONS/val2017'  # 数据集的 xml 目录
    xml2json(root)