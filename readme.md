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

---

# 엘라스틱서치 시작
- [엘라스틱 서치 개발환경 세팅](https://wiken.io/ken/3374) 참고
- 개발환경(장고, MySQL, virtualbox, elk on virtualbox)을 모드 세팅하고 http://localhost/products/search_by_elastic/ 로 접속하시면 연동결과를 확인할 수 있습니다.

---

# 엘라스틱서치 팁
## 인덱스 깔끔하게 지우고 MySQL의 모든 데이터를 처음부터 다시 인덱스에 넣는 방법
1. 로그스태시의 sql_last_value 값 클리어
2. 로그스태시만 리스타트
3. 키바나에서, 인덱스 삭제, 인덱스 세팅, 인덱스 매핑 세팅
4. 자세한 내용은 [엘라스틱 서치 개발환경 세팅, wiken.io/ken/3374, 16강 ~ 18강](https://wiken.io/ken/3374) 참고

---

# 키바나에서 사용하면 좋은 명령어들

## 인덱스 목록(실행은 Alt + Enter)

```
GET /_cat/indices
```

## 첫번째 인덱스 삭제

```
DELETE /sample1_dev___products_product_type_1___v1
```

## 첫번째 인덱스 생성 및 설정

```
PUT /sample1_dev___products_product_type_1___v1
{
  "settings": {
    "index": {
      "number_of_shards": 5,
      "number_of_replicas": 1
    },
    "analysis": {
      "analyzer": {
        "nori_analyzer": {
          "type": "custom",
          "tokenizer": "nori_tokenizer",
          "filter": "nori_filter"
        }
      },
      "tokenizer": {
        "nori_tokenizer": {
          "type": "nori_tokenizer",
          "decompound_mode": "discard",
          "user_dictionary": "dict.txt"
        }
      },
      "filter": {
        "nori_filter": {
          "type": "nori_part_of_speech",
          "stoptags": [
            "E", "IC", "J", "MAG", "MAJ", "MM", "SP", "SSC", "SSO", "SC", "SE", "XPN", "XSA", "XSN", "XSV", "UNA", "NA", "VSV"
          ]
        }
      }
    }
  }
}
```

## 첫번째 인덱스의 타입 설정(엘라스틱 서치 7.0 부터 인덱스에 타입 1개만 설정 가능)

```
PUT /sample1_dev___products_product_type_1___v1/_mappings
{
  "properties": {
    "id": {
      "type": "long"
    },
    "name": {
      "type": "keyword",
      "copy_to": [ "name_nori"]
    },
    "name_nori": {
      "type": "text",
      "analyzer": "nori_analyzer"
    },
    "display_name": {
      "type": "keyword",
      "copy_to": [ "display_name_nori"]
    },
    "display_name_nori": {
      "type": "text",
      "analyzer": "nori_analyzer"
    },
    "description": {
      "type": "keyword",
      "copy_to": [ "display_name_nori"]
    },
    "description_nori": {
      "type": "text",
      "analyzer": "nori_analyzer"
    },
    "cate_item_id": {
      "type": "integer"
    },
    "market_id": {
      "type": "integer"
    },
    "price": {
      "type": "integer"
    },
    "sale_price": {
      "type": "integer"
    }
  }
}
```

## 첫번째 인덱스 확인

```
GET /sample1_dev___products_product_type_1___v1
```

## 첫번째 인덱스 안의 데이터 개수 확인

```
GET _sql?format=json
{
  "query": """
  SELECT COUNT(*) FROM sample1_dev___products_product_type_1___v1
  """
}
```

## 첫번째 인덱스 안의 데이터 확인

```
GET _sql?format=json
{
  "query": """
  SELECT * FROM sample1_dev___products_product_type_1___v1
  """
}
```

## 두번째 인덱스 삭제

```
DELETE /sample1_dev___products_product_type_2___v1
```

## 두번째 인덱스 설정

```
PUT /sample1_dev___products_product_type_2___v1
{
  "settings": {
    "index": {
      "number_of_shards": 5,
      "number_of_replicas": 1
    },
    "analysis": {
      "analyzer": {
        "nori_analyzer": {
          "type": "custom",
          "tokenizer": "nori_tokenizer",
          "filter": "nori_filter"
        }
      },
      "tokenizer": {
        "nori_tokenizer": {
          "type": "nori_tokenizer",
          "decompound_mode": "discard",
          "user_dictionary": "dict.txt"
        }
      },
      "filter": {
        "nori_filter": {
          "type": "nori_part_of_speech",
          "stoptags": [
            "E", "IC", "J", "MAG", "MAJ", "MM", "SP", "SSC", "SSO", "SC", "SE", "XPN", "XSA", "XSN", "XSV", "UNA", "NA", "VSV"
          ]
        }
      }
    }
  }
}
```

## 두번째 인덱스의 타입 설정

```
PUT /sample1_dev___products_product_type_2___v1/_mappings
{
  "properties": {
    "id": {
      "type": "long"
    },
    "name": {
      "type": "keyword",
      "copy_to": [ "name_nori"]
    },
    "name_nori": {
      "type": "text",
      "analyzer": "nori_analyzer"
    },
    "display_name": {
      "type": "keyword",
      "copy_to": [ "display_name_nori"]
    },
    "display_name_nori": {
      "type": "text",
      "analyzer": "nori_analyzer"
    },
    "description": {
      "type": "keyword",
      "copy_to": [ "description_nori"]
    },
    "description_nori": {
      "type": "text",
      "analyzer": "nori_analyzer"
    },
    "market_name": {
      "type": "keyword",
      "copy_to": [ "market_name_nori"]
    },
    "market_name_nori": {
      "type": "text",
      "analyzer": "nori_analyzer"
    },
    "cate_item_name": {
      "type": "keyword",
      "copy_to": [ "cate_item_name_nori"]
    },
    "cate_item_name_nori": {
      "type": "text",
      "analyzer": "nori_analyzer"
    },
    "price": {
      "type": "integer"
    },
    "sale_price": {
      "type": "integer"
    }
  }
}
```

## 두번째 인덱스 확인

```
GET /sample1_dev___products_product_type_2___v1
```

## 두번째 인덱스 안의 데이터 개수 확인

```
GET _sql?format=json
{
  "query": """
  SELECT COUNT(*) FROM sample1_dev___products_product_type_2___v1
  """
}
```

## 두번째 인덱스 안의 데이터 확인

```
GET _sql?format=json
{
  "query": """
  SELECT * FROM sample1_dev___products_product_type_2___v1
  """
}
```
