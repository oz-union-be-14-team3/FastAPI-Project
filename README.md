# 세팅 순서
1. .env 생성하고 .env.dev에 있는 형식대로 작성
2. psql -U postgres : db접속
3. CREATE DATABASE <db이름>; : db생성
4. GRANT ALL PRIVILEGES ON DATABASE <db이름> TO <님이름>;
5. aerich init -t app.db.migration.TORTOISE_ORM : aerich 초기화 파일 연결
6. aerich init-db : 초기화

# aerich migrate
- aerich init -t app.db.migration.TORTOISE_ORM
- aerich init-db
- aerich migrate
- aerich upgrade