#!/usr/bin/env python3
import requests
import re
import boto3
import os

# make sure /tmp/pictures directory exists
target_store_picture_dir = '/tmp/pictures/'
if not os.path.exists(target_store_picture_dir):
    os.makedirs(target_store_picture_dir)

patt = re.compile(r'2sc2.*?.jpg(?=\")')
#patt = re.compile(r'2sc2.*?(?<=jpg)(?=\")')

s3 = boto3.client('s3')

def get_img_url(url):
    '''get the image url'''
    res = requests.get(url)
    res.encoding = 'gb2312'
    html = res.text
    img_url_list = re.findall(patt, html)

    return img_url_list

def download_img(img_url):
    '''download the image'''
    response = requests.get(img_url)
    image_name = img_url.split('__')[1]
    if image_name.endswith('.jpg'):
        if os.path.exists(target_store_picture_dir + image_name):
            print(image_name, 'already exists')
        else:
            print('downloading the image', img_url, 'save it as', image_name)
            with open(target_store_picture_dir + image_name, 'wb') as f:
                f.write(response.content)

def upload_file_2_s3(img_name, s3_name, target_name):
    print("uploading {} to {}".format(img_name, s3_name), target_name)
    s3.upload_file(img_name, s3_name, target_name)

def run():
    for i in range(1, 100):
        downloaded_img_list = []
        web_page_url = 'https://www.che168.com/china/50_0/a0_0msdgscncgpiltocsp{}exx0/'.format(i)
        print('preparing the image url list from', web_page_url)
        image_url_list = get_img_url(web_page_url)
        for url in image_url_list:
            image_name = url.split('__')[1]
            if image_name.endswith('.jpg'):
                # download the image
                download_img("https://" + url)
                downloaded_img_list.append(image_name)
        for image in downloaded_img_list:
            upload_file_2_s3(target_store_picture_dir + image, 'ops-hackathon-store-go', str(i)+ '/' + image)

if __name__ == '__main__':
    run()
