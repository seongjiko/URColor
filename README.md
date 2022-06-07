# URColor
- 22년도 1학기 영상처리 프로그래밍 기말 단기 프로젝트
- 프로젝트 우수작 선정 (22.06.07)

# 프로젝트 초안
### 아이디어
아이디어: 사진이 주어지면 흑백으로 변환하고, 원하는 색만 컬러로 나타내어주는 기능을 제공합니다. 색은 여러 개 추가, 선택이 가능하며 이 색을 다른 색으로 변환해주는 기능까지 제공할 예정입니다.
색의 탐지범위는 trackbar을 통해 지정할 수 있도록 하며 BGR to HSV변환을 통해 색상정보를 검출합니다.

아이디어는 예전에 포토샵을 공부했을 때 일부 색상만 추출하는 강의를 보게되었는데, openCV로 충분히 구현할 수 있다고 생각하였습니다.

![image](https://user-images.githubusercontent.com/46768743/171196838-27cf55f7-e5de-4fa7-9111-f1a06ef9e98e.png)  
<만약 빨간색을 지정했다면 위의 사진처럼 나오도록 합니다. 그리고 이 부분의 색을 원하는 색으로 변경할 수 있도록 기능을 제공합니다.>


## 22.06.05 구현 완료, 시연 사진
### 자세한 기능들은 doc폴더 속 functions.txt를 참고해주시고 소스파일과 이미지파일이 모두 업로드 되어있습니다. src속 event_platte.py를 실행하시면 됩니다!

`프로그램 초기화면`  
![image](https://user-images.githubusercontent.com/46768743/172040645-60f8c9d7-d240-4a52-a532-c3ec24278c8d.png)

`원본 사진파일 및 파일을 불러왔을 때의 장면 (흑백으로 시작)`  
![image](https://user-images.githubusercontent.com/46768743/172040668-07cd63d2-91df-493a-bab2-4cab6cbadb4d.png)
![image](https://user-images.githubusercontent.com/46768743/172040669-48967845-84e0-489a-8ed2-978ec046697c.png)


`HUE에서 파란색 부분을 클릭하고 추출 아이콘을 클릭할 경우, 파란색을 띄는 하트만 컬러를 입힌 모습`    
![image](https://user-images.githubusercontent.com/46768743/172040710-004eb586-ebcd-415e-a8c4-5e3d5882b623.png)
![image](https://user-images.githubusercontent.com/46768743/172040712-4c336694-b2d0-4a0d-8174-eebe746d259a.png)

`이어서 핑크색 하트도 추출 (STACK mode가 ON인 상태)`    
![image](https://user-images.githubusercontent.com/46768743/172040734-f9ab8887-cb9e-4857-a363-2c12becf2d58.png)
![image](https://user-images.githubusercontent.com/46768743/172040737-6d16f486-f836-4737-8ed3-9f74751387a0.png)

`블러링을 이용한 아웃포커싱 (파란, 핑크 하트 제외 블러) 그리고 저장(saveIcon 클릭)한 사진`  
![image](https://user-images.githubusercontent.com/46768743/172040773-e5015e03-e7d1-42d7-8c6f-15c7c361d2bf.png)
![image](https://user-images.githubusercontent.com/46768743/172040775-4743e5e2-5058-4fb4-a905-a4bcc31abb96.png)

