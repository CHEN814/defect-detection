# 缺陷检测 defect-detection
缺陷检测是图像处理领域一个应用广泛的问题。本课题依托科研项目，采用无人机上的图像探测器采集工厂内部货架图片；通过图片配准及比对，识别螺丝松动等缺陷。从而防止隐患的发生。也可以使用公开数据集处理，课题主要是算法，不限制算法依托的软件平台。

## 数据集 datasets
数据集选择GC10-DET。GC10-DET是在真实工业中收集的表面缺陷数据集。一个真实的行业。它包含十种类型的表面缺陷，即冲孔（Pu）、焊缝（Wl）、新月形缝隙（Cg）、水斑（Water Spot）。油斑(Os)、丝斑(Ss)、夹杂物(In)、轧坑(Rp)、折痕(Cr)、腰部折痕 (Wf)。所收集的缺陷都在钢板的表面。该数据集包括3570张灰度图像。<br/>
GC10-DET数据集可以在github上获得：https://github.com/lvxiaoming2019/GC10-DET-Metallic-Surface-Defect-Matasets<br/>
因原始数据集有误，可采用链接中修正错误后的版本：http://t.csdnimg.cn/jNolA<br/>

### 训练集和验证集划分
训练集和验证集的划分：数据总共2294个，按照约9：1比例分训练集train和验证集val，其中训练集1998个，验证集296个。

### 统一格式
因为采用YOLOv6模型，需要将数据集转化成特定形式。格式转换过程如下。<br/>
images：将图片划分在训练集和验证集两个文件夹中。<br/>
annotations：train和val分别生成json文件，参考http://t.csdnimg.cn/JFkYw。<br/>
labels：数据集的标签为xml格式，需要转换成txt格式，并对数据进行归一化处理，以便yolo算法使用，参考http://t.csdnimg.cn/skq1Y。

整理后的数据集文件结构如下：

### COCO 数据集

├── coco<br/>
│   ├── annotations<br/>
│   │   ├── instances_train2017.json<br/>
│   │   └── instances_val2017.json<br/>
│   ├── images<br/>
│   │   ├── train2017<br/>
│   │   └── val2017<br/>
│   ├── labels<br/>
│   │   ├── train2017<br/>
│   │   ├── val2017<br/>

### YOLO格式的数据集下载链接
YOLO格式的GC10-DET数据集<br/>
链接：https://pan.baidu.com/s/11slnV0Bvpagweqxzi2UgDw?pwd=zzai <br/>
提取码：zzai
