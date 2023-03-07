# video-capture란 무엇인가요?
video-capture는 동영상의 프레임을 읽어 이미지로 추출하는 도구입니다.

### [📜ENGLISH DOCUMENT](https://github.com/jesunglim/video-capture/blob/main/README_EN.md)

![diagram](screenshots/diagram.jpg)



## video-capture을 설치하는 방법

### Clone the repository
```
https://github.com/jesunglim/video-capture.git
```

### 필수 패키지 설치
video-capture는 OpenCV 와 Pandas만 설치하면 됩니다.
pip install로 설치하는것을 권장합니다.
```
pip install opencv-python
pip install pandas
```

requirements로 설치도 가능합니다.

```
cd video-capture
pip install -r requirements.txt
```

## video-capture 실행 방법
리눅스나 macOS를 사용하신다면 파일 경로만 변경해주세요.
```
cd video-capture
# Generic
python main.py --path [video folder path]

# Example
python main.py --path C:\\Users\\jesung\\Videos\\4k
```
![photo](screenshots/run.png)

## Arguments
|   Arguments   |       설명
|:-------------:|:------------------------------------:|
|   path        |   캡쳐할 비디오들이 있는 경로
|   frame       |   캡쳐할 프레임 주기. 만약 24라면 24프레임마다 한번씩 저장합니다.
|   split_num   |   분할할 화면 수. None, 4 중 선택
|   gaussian    |   Gaussian Filter Kernel Size.  1~3 권장
|   compres     |   blur 처리를 위해 압축할 해상도
|   outpres     |   blur된 이미지를 출력할 해상도

## Result
Crop Result
![crop_result](screenshots/crop_result.jpg)

저장된 4분할 이미지
![split_result](screenshots/split_result.png)c