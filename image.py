from PIL import Image

def combine_images_vertically(img1_path, img2_path, output_path):
    # 이미지 열기
    image1 = Image.open(img1_path)
    image2 = Image.open(img2_path)

    # 새로운 이미지의 크기 계산
    new_width = max(image1.width, image2.width)
    new_height = image1.height + image2.height

    # 새로운 이미지 생성
    new_image = Image.new('RGB', (new_width, new_height))

    # 첫 번째 이미지를 새 이미지에 붙여넣기
    new_image.paste(image1, (0, 0))

    # 두 번째 이미지를 새 이미지에 붙여넣기
    new_image.paste(image2, (0, image1.height))

    # 결과 이미지 저장
    new_image.save(output_path)

# 사용 예시
combine_images_vertically('C:/Users/Ahn Yehyeon/Desktop/2023-1/emo/User/example/Results/Score/0001.png', 'C:/Users/Ahn Yehyeon/Desktop/2023-1/emo/User/example/Results/Score/0002.png', 'combined.png')
