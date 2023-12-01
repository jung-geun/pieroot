# Backend

## 개요

이 문서는 서버 측 개발에 대한 가이드를 제공합니다.

## 폴더 구조

```
backend
├── database_app
│   ├── __init__.py
│   ├── crud.py              // crud operation
│   ├── database.py          // database connection
│   ├── main.py              // database app
│   ├── models.py            // database models
│   ├── schemas.py           // database schemas
├── README.md
```

## 테스트 빌드

```bash
$ cd backend

$ uvicorn main:app --reload --ssl-keyfile /etc/ssl/key.pem --ssl-certfile /etc/ssl/cert.pem
```
위의 key.pem과 cert.pem은 https를 위한 인증서 파일입니다. 서버에 맞게 경로를 수정해주세요.