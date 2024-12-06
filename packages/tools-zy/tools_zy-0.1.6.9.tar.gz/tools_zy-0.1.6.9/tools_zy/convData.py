# -*- coding: utf-8 -*-

import time
import copy
import os
import json

def get_categories(json_file: str = './categories_person.json') -> dict:
    # with open(json_file, 'r', encoding='utf-8') as file:
    #     categories = json.load(file)
    categories = {
        "supercategory": "person",
        "id": 1,
        "name": "person",
        "keypoints": [
            "nose",
            "l_shoulder",
            "r_shoulder",
            "l_elbow",
            "r_elbow",
            "l_wrist",
            "r_wrist",
            "l_hip",
            "r_hip",
            "l_knee",
            "r_knee",
            "l_ankle",
            "r_ankle"
        ],
        "skeleton": [
            [1, 2],
            [1, 3],
            [2, 3],
            [2, 4], [4, 6],
            [3, 5], [5, 7],
            [2, 8],
            [3, 9],
            [8, 9],
            [8, 10], [10, 12],
            [9, 11], [11, 13]
        ]
    }
    return categories

def labelme2coco(labelme_json_path, coco_json_path, exists_add=False, bbox=None):
    with open(labelme_json_path, 'r', encoding='utf-8') as f:
        labelme_data = json.load(f)

    coco_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    if os.path.exists(coco_json_path):
        if exists_add:
            with open(coco_json_path, 'r') as f:
                coco_data = json.load(f)
        else:
            coco_json_path = coco_json_path.split('.')[0] + '_' + str(time.time()) + '.json'
        
    file_name = os.path.basename(labelme_data['imagePath'])
    image_id = file_name.split('.')[0]

    categorie_i = get_categories()
    if categorie_i not in coco_data['categories']:
        coco_data['categories'].append(categorie_i)

    image_i = {'height': labelme_data['imageHeight'], 
               'width': labelme_data['imageWidth'],
               'file_name': file_name,
               'id': image_id}
    coco_data['images'].append(image_i)

    keypoints = [0] * 3 * len(categorie_i['keypoints'])
    shapes = labelme_data['shapes']
    for shape_i in shapes:
        if shape_i['shape_type'] == 'rectangle':
            (x1, y1), (x2, y2) = shape_i['points']
            x1, x2 = (x1, x2) if x1 <= x2 else (x2, x1)
            y1, y2 = (y1, y2) if y1 <= y2 else (y2, y1)
            if bbox is None:
                bbox = [x1, y1, x2 - x1, y2 - y1]
        elif shape_i['shape_type'] == 'point':
            idx = int(shape_i['label'])
            keypoints[(idx - 1) * 3 + 0] = shape_i['points'][0][0]
            keypoints[(idx - 1) * 3 + 1] = shape_i['points'][0][1]
            keypoints[(idx - 1) * 3 + 2] = 2
            if shape_i['group_id'] is not None:
                keypoints[(idx - 1) * 3 + 2] = int(shape_i['group_id'])
    if bbox is None:
        bbox = [1, 1, labelme_data['imageWidth'] - 1, labelme_data['imageHeight'] - 1]
    annotation_i = {'segmentation': [[]],
                    'num_keypoints': len(categorie_i['keypoints']),
                    'area': int((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])),
                    'iscrowd': 0,
                    'keypoints': copy.deepcopy(keypoints),
                    'image_id': image_id,
                    'bbox': bbox,
                    'category_id': 1,
                    'id': image_id
                    }
    coco_data['annotations'].append(annotation_i)
    with open(coco_json_path, 'w') as f:
        json.dump(coco_data, f, indent=4, ensure_ascii=False)
    return coco_json_path

def labelmes2coco(labelme_json_folder, coco_json_path, bbox=None):
    for f_name in os.listdir(labelme_json_folder):
        if f_name.endswith('.json'):
            labelme2coco(os.path.join(labelme_json_folder, f_name), coco_json_path, exists_add=True, bbox=bbox)