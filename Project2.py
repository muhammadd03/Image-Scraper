# Use imgs = tree.css("figure a img + div img") instead of imgs = tree.css("figure a img")
import os
from httpx import get
from selectolax.parser import HTMLParser
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_img_tags_for(term=None):
    if not term:
        raise Exception('No search term provided')

    url = f'https://unsplash.com/s/photos/{term}'
    response = get(url)

    if response.status_code != 200:
        raise Exception('Error getting response')

    tree = HTMLParser(response.text)
    imgs = tree.css('figure a img + div img')
    return imgs


def img_filter_out(url: str, keywords: list) -> bool:
    return not any(x in url for x in keywords)

# img_filter(src, ['premium','profile']) -> true/false


def get_high_res_img_urls(image_node):
    srcset = image_node.attrs['srcset']
    srcset_list = srcset.split(', ')

    url_res = [src.split(' ')for src in srcset_list if img_filter_out(src, ['plus', 'premium', 'profile'])]

    if not url_res:
        return None

    return url_res[0][0].split('?')[0]


def save_images(img_urls, dest_dir='images', tag=''):
    for url in img_urls:
        response = get(url)
        logging.info(f'Downloading {url}...')

        file_name = url.split('/')[-1]

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        with open(f'{dest_dir}/{tag}{file_name}.jpeg', 'wb') as f:
            f.write(response.content)
            logging.info(f'Saved {file_name}, with size {round(len(response.content)/1024/1024,2)} MB.')


if __name__ == '__main__':
    search_tag = 'dolphin'
    dest_dir = 'dolphins'
    image_nodes = get_img_tags_for(search_tag)
    all_img_urls = [get_high_res_img_urls(image) for image in image_nodes]
    img_urls = [u for u in all_img_urls if u]
    save_images(img_urls[:3], dest_dir, search_tag)


    # [print(get_high_res_img_urls(image))for image in image_nodes[:4]]
    # image_urls = [image.attrs['src'] for image in image_nodes]
    # relevant_urls = [image for image in image_urls if img_filter_out(image, ['plus', 'premium', 'profile'])]
    #
    # #  here u means url for each image
    # for u in relevant_urls:
    #     print(u)
    #
    # print(len(image_nodes))
    # print(image_nodes)
