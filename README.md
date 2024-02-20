# 缺陷检测
缺陷检测是图像处理领域一个应用广泛的问题。本课题依托科研项目，采用无人机上的图像探测器采集工厂内部货架图片；通过图片配准及比对，识别螺丝松动等缺陷。从而防止隐患的发生。也可以使用公开数据集处理，课题主要是算法，不限制算法依托的软件平台。

## 环境
模型算法选择：YOLOv6<br/>
https://yolov6-docs.readthedocs.io/zh-cn/latest<br/>
其中，python =3.9；torch=2.2.0；cpu版本

## 数据集
数据集选择GC10-DET。GC10-DET是在真实工业中收集的表面缺陷数据集。一个真实的行业。它包含十种类型的表面缺陷，即冲孔（Pu）、焊缝（Wl）、新月形缝隙（Cg）、水斑（Water Spot）。油斑(Os)、丝斑(Ss)、夹杂物(In)、轧坑(Rp)、折痕(Cr)、腰部折痕 (Wf)。所收集的缺陷都在钢板的表面。该数据集包括3570张灰度图像。<br/>
GC10-DET数据集可以在github上获得：https://github.com/lvxiaoming2019/GC10-DET-Metallic-Surface-Defect-Matasets<br/>
因原始数据集有误，可采用链接中修正错误后的版本：http://t.csdnimg.cn/jNolA<br/>

### 训练集和验证集划分
训练集和验证集的划分：数据总共2294个，按照约9：1比例分训练集train和验证集val，其中训练集1998个，验证集296个。

### 统一格式
因为采用YOLOv6模型，需要将数据集转化成特定形式。格式转换过程如下。<br/>
```
images：将图片划分在训练集和验证集两个文件夹中。<br/>
annotations：train和val分别生成json文件，参考http://t.csdnimg.cn/JFkYw。<br/>
labels：数据集的标签为xml格式，需要转换成txt格式，并对数据进行归一化处理，以便yolo算法使用，参考http://t.csdnimg.cn/skq1Y。
```

整理后的数据集文件结构如下：

### COCO 数据集
```
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
```

### YOLO格式的数据集下载链接
YOLO格式的GC10-DET数据集<br/>
```
链接：https://pan.baidu.com/s/11slnV0Bvpagweqxzi2UgDw?pwd=zzai <br/>
提取码：zzai
```

## 模型训练、评估、推理

### 配置文件准备
#### 创建数据集配置文件
1) 数据集组织成COCO格式后，选择YOLOv6/data/coco.yaml作为配置文件。（其他数据集格式参考官网文档，目前支持VOC格式和自定义数据集） <br/>
2) 配置文件中train和val路径必填，test选填，其他信息按要求填好即可。 <br/>

#### 选择网络配置文件
1) 如果是训练 COCO 数据集或与 COCO 差异较大的数据集，建议选用 yolov6n(/s/m/l).py 配置文件； <br/>
2) 如果是训练自定义数据集，建议选用 yolov6n(/s/m/l)_finetune.py 配置文件；

### 模型训练
#### CPU
cpu训练时一直在报错，对YOLOv6源码修改，记录如下：（用gpu训练时要改回去） <br/>
1) yolov6/utils/envs.py，第20行，device = ‘cpu’  <br/>
```
def select_device(device):
    device = 'cpu'
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    LOGGER.info('Using CPU for training... ')
    # for testing, set device to 'cpu'.
    '''
        if device == 'cpu':
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        LOGGER.info('Using CPU for training... ')

    elif device:
        os.environ['CUDA_VISIBLE_DEVICES'] = device
        assert torch.cuda.is_available()
        nd = len(device.strip().split(','))
        LOGGER.info(f'Using {nd} GPU for training... ')
    cuda = device != 'cpu' and torch.cuda.is_available()
    device = torch.device('cuda:0' if cuda else 'cpu')
    '''

    return device
```

2) yolov6/core/engine.py，458行，将dp_mode和ddp_model恒定为0<br/>
```
    def parallel_model(args, model, device):
        # If DP mode
        dp_mode = 0
        # dp_mode = device.type != 'cpu' and args.rank == -1  #For test
        if dp_mode and torch.cuda.device_count() > 1:
            LOGGER.warning('WARNING: DP not recommended, use DDP instead.\n')
            model = torch.nn.DataParallel(model)

        # If DDP mode
        ddp_mode = 0
        # ddp_mode = device.type != 'cpu' and args.rank != -1  #For test
        if ddp_mode:
            model = DDP(model, device_ids=[args.local_rank], output_device=args.local_rank)

        return model
```

#### GPU
(...)

### 模型推理
```
步骤 0. 从 YOLOv6官方github 下载一个训练好的模型权重文件，或选择您自己训练的模型；<br/>
步骤 1. 通过 tools/infer.py文件进行推理。<br/>
```
```
P5 models<br/>
python tools/infer.py --weights yolov6s.pt --source img.jpg / imgdir / video.mp4<br/>
P6 models<br/>
python tools/infer.py --weights yolov6s6.pt --img-size 1280 1280 --source img.jpg / imgdir / video.mp4<br/>
```
运行后，在runs/inference/exp目录下能看到对应的可视化结果。<br/>
关键参数说明见官网，网址最前面写过。

