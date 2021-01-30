with open("test_shopee/test_shopee_filters.txt", 'r') as f:
    img_urls = [line.rstrip('\n').split(',') for line in f.readlines()]
    cat_no = int(img_urls[9][0])
    print(f'Image loaded (filter_no={9}, cat_no={cat_no}):\n  {img_urls[9][1]}')
    print(len(img_urls))