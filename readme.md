# 의존성
- node js
  - nvm 으로 설치하기를 권장
- mariadb

# 가정
- mariadb 계정
  - sbsst / sbs123414
- mysql 실행파일 경로
  - /c/xampp/mysql/bin/mysql
- DB명 : sample1_dev

# 프로젝트 세팅
- npm install
- pip install -r requirements/dev.txt
- /c/xampp/mysql/bin/mysql -u sbsst -psbs123414 -e "DROP DATABASE IF EXISTS sample1_dev; CREATE DATABASE sample1_dev"
  - DB 초기화

# 프로젝트 실행
- mariadb 실행
- npm run css
- 다른 터미널 열기
- ./manage.py migrate
- ./manage.py runserver 0.0.0.0:8000

---

# 유용한 명령어
- /c/xampp/mysql/bin/mysql -u sbsst -psbs123414 -e "DROP DATABASE IF EXISTS sample1_dev; CREATE DATABASE sample1_dev"
  - DB 초기화 명령어
- /c/xampp/mysql/bin/mysql -u sbsst -psbs123414 -e "DROP DATABASE IF EXISTS sample1_dev; CREATE DATABASE sample1_dev" && ./manage.py migrate
  - DB 초기화 명령어 && 마이그레이트
- /c/xampp/mysql/bin/mysql -u sbsst -psbs123414 -e "DROP DATABASE IF EXISTS sample1_dev; CREATE DATABASE sample1_dev" && ./manage.py migrate && ./manage.py runserver 0.0.0.0:8000
  - DB 초기화 명령어 && 마이그레이트 && 서버실행