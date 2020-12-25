from bing_image_downloader import downloader


def image(word):
    downloader.download(word, limit=5,  output_dir='app/data/images',
                        adult_filter_off=True, force_replace=False, timeout=60)
