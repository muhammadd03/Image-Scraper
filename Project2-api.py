from httpx import get
import os


def get_response_for(keyword, results_per_page, page=1):
    url = f'https://unsplash.com/napi/search/photos?page={page}&per_page={results_per_page}&query={keyword}&xp=semantic-search%3Aexperiment'
    response = get(url)

    if response.status_code == 200:
        return response.json()


def get_image_url(data):
    results = data['results']

    img_urls = [x['urls']['raw'] for x in results if x['premium'] is False]
    img_urls = [x.split('?')[0] for x in img_urls]  # To get Canonical Image urls

    return img_urls


def download_images(img_urls, max_download, dest_dir='images_from_api_method', tag="" ):
    successfully_downloaded_images = 0

    for url in img_urls:
        if successfully_downloaded_images < max_download:
            response = get(url)
            file_name = url.split('/')[-1]

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            with open(f'{dest_dir}/{tag}{file_name}.jpeg', 'wb') as f:
                f.write(response.content)
                successfully_downloaded_images += 1
        else:
            break

    return successfully_downloaded_images


def scrape(keyword, num_of_results):
    start_page = 1
    success_count = 0

    while success_count < num_of_results:
        data = get_response_for(keyword, results_per_page=20, page=start_page)

        max_download = num_of_results - success_count

        if data:
            img_urls = get_image_url(data)
            successful_downloads = download_images(img_urls, max_download, tag=keyword)
            success_count += successful_downloads
            start_page += 1
        else:
            print('Error: no data returned')
            break


if __name__ == '__main__':
    # download x images under this term
    # x = 2, page 1 suffices
    # x =200, page 1 most definitely does not suffice
    # data = get_response_for('dolphins', 3)
    # print(get_image_url(data))
    scrape('microphone', 10)
