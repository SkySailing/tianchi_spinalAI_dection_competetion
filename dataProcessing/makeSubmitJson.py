# author: 
# contact: onlydgi@foxmail.com
# datetime:2020/8/12 下午7:55
# software: PyCharm
"""
文件说明：
"""

import json
import os
import pandas as pd
import SimpleITK as sitk

jsondir = r"../../tcdata/round2_series_map.json"
img_dir = r"../../tcdata/round2test"
saveName = r"../../tcdata/round2_test50.csv"


def dicom_metainfo(dicm_path, tag):
    '''
    获取dicom的元数据信息
    :param dicm_path: dicom文件地址
    :param list_tag: 标记名称列表,比如['0008|0018',]
    :return:
    '''
    reader = sitk.ImageFileReader()
    reader.LoadPrivateTagsOn()
    reader.SetFileName(dicm_path)
    reader.ReadImageInformation()
    return reader.GetMetaData(tag)

def pickeT2fromtestdata(jsondir, img_dir, saveName='./', ShowFlag=False):
    with open(jsondir, 'r', encoding='utf8')as fp:
        a = json.load(fp)
        l_seriesUID = []
        l_studyUID = []
        for study in a:
            l_seriesUID.append(study["seriesUid"])
            l_studyUID.append(study["studyUid"])
        fp.close()
    subfile = os.listdir(img_dir)
    subfile.sort(key=lambda x: int(x[5:]))
    testList = []
    for subfile_name in subfile:
        subfile_path = os.path.join(img_dir, subfile_name)
        img_file = os.listdir(subfile_path)
        img_file.sort(key=lambda x: int(x[5:-4]))
        testImgList = []
        for imgfile_name in img_file:
            img_path = os.path.join(subfile_path, imgfile_name)
            sz = os.path.getsize(img_path)
            if ShowFlag:
                print("sz", sz)
            if sz < 1000:
                continue
            uid = dicom_metainfo(img_path, '0020|000e')
            if ShowFlag:
                print(uid)
            if uid in l_seriesUID:
                testImgList.append(img_path[:])
        mid = len(testImgList)//2
        # 1 +
        testList.append(testImgList[mid])
    if ShowFlag:
        pdImg = pd.DataFrame(testList)
        pdImg.to_csv(saveName, header=None, index=None)
    return testList

if __name__ == '__main__':
    a = pickeT2fromtestdata(jsondir, img_dir, saveName, ShowFlag=False)
    print(a)





