# 테스트 환경에서 테스트 먼저
docker exec python__2__test bash -c "cd /data/site_projects/python__2__test/src/ ; git pull origin master"

{
  docker exec python__2__test bash -c "cd /data/site_projects/python__2__test/src/ ; python manage.py test --settings=base.settings.prod"
} || {
  exit 1
}

# 기존장고 종료
docker exec python__2 pkill "gunicorn"

# 폴더에 깃에 있는 최신소스코드 가져오기
docker exec python__2 bash -c "cd /data/site_projects/python__2/src/ ; git pull origin master"

# 의존성 설치
docker exec python__2 bash -c "cd /data/site_projects/python__2/src/ ; pip install -r requirements/prod.txt"

# 마이그레이트
docker exec python__2 bash -c "cd /data/site_projects/python__2/src/ ; python manage.py migrate --settings=base.settings.prod"

# static collect 다시 수행
docker exec -it python__2 bash -c "cd /data/site_projects/python__2/src ; echo yes | python manage.py collectstatic --settings=base.settings.prod"

# 장고를 운영모드로 실행
docker exec python__2 bash -c "cd /data/site_projects/python__2/src ; nohup gunicorn --bind=0.0.0.0:8000 base.wsgi &"