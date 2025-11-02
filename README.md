<!--
# 세팅 순서
0. poetry install
1. .env 생성하고 .env.dev에 있는 형식대로 작성
2. psql -U postgres : db접속
3. CREATE DATABASE <db이름>; : db생성
4. GRANT ALL PRIVILEGES ON DATABASE <db이름> TO <님이름>;
5. aerich init -t app.db.migration.TORTOISE_ORM : aerich 초기화 파일 연결
6. aerich init-db : 초기화
7. aerich migrate
8. aerich upgrade

# aerich migrate
- aerich init -t app.db.migration.TORTOISE_ORM : 
- aerich init-db
- aerich migrate
- aerich upgrade
-->
# 📌 FastAPI 웹 스크래핑 & 일기 서비스 미니 프로젝트

> FastAPI + Poetry + Tortoise ORM + JWT 인증 + AWS EC2 배포

사용자는 로그인 후  
- ✅ 일기를 작성/조회/수정/삭제(CRUD)
- ✅ 랜덤 명언 제공
- ✅ 랜덤 자기성찰 질문 제공

을 수행할 수 있는 백엔드 API 서비스입니다.

---

## 🚀 기술 스택

| 구분 | 사용 기술 |
|------|-----------|
| Backend Framework | FastAPI |
| ORM | Tortoise ORM |
| DB | SQLite(Local), PostgreSQL(Optional) |
| Auth | JWT 인증 + Token Blacklist |
| Infra | AWS EC2 |
| Dependency 관리 | Poetry |
| Web Server | Uvicorn |
| Test | Pytest / pytest-asyncio |
| VCS | Git / GitHub |

---

## 📂 프로젝트 구조

```
app/
 ┣ api/
 ┃ ┗ v1/
 ┃   ┣ auth.py
 ┃   ┣ diary.py
 ┃   ┣ question.py
 ┃   ┗ quote.py
 ┣ core/
 ┣ db/
 ┣ models/
 ┣ repositories/
 ┣ schemas/
 ┗ main.py
```

---

## 🧠 기능 요약

### ✅ 사용자 인증
- JWT 로그인 / 회원가입
- 로그아웃 시 refresh token blacklist 처리

### ✅ 다이어리 기능
| 기능 | 설명 |
|------|------|
| POST `/diaries` | 일기 생성 |
| GET `/diaries` | 내 일기 전체 조회 |
| GET `/diaries/{id}` | 특정 일기 조회 |
| PUT `/diaries/{id}` | 일기 수정 |
| DELETE `/diaries/{id}` | 일기 삭제 |

### ✅ 기타
- 명언 API
- 랜덤 질문 API

---

## 🗂 ERD

<img width="1178" height="566" alt="스크린샷 2025-10-30 오후 7 01 54" src="https://github.com/user-attachments/assets/3abc3e76-d491-4835-b029-b716879065ca" />


### ERD 테이블 요약

| 테이블 | 설명 |
|--------|------|
| users | 사용자 |
| token_blacklist | 만료된 토큰(로그아웃 처리) |
| diaries | 사용자 일기 |
| quotes | 저장된 명언 |
| questions | 저장된 질문 |

---

## 🔧 설치 & 실행

### ✅ 1) 프로젝트 클론

```bash
git clone <repo_url>
cd FastAPI-Project
```

### ✅ 2) Poetry 설치 & 진입

```bash
poetry install
poetry shell
```

### ✅ 3) DB 초기화 (Tortoise ORM)

```bash
aerich init -t app.core.config.TORTOISE_ORM
aerich init-db
```

### ✅ 4) 서버 실행

```bash
uvicorn app.main:app --reload
```

접속 주소 👉 http://127.0.0.1:8000/docs

---

## 🧪 테스트 실행

```bash
pytest -v
```

---

## ☁️ AWS 배포 요약

| 항목 | 내용 |
|------|------|
OS | Ubuntu (EC2) |
Server | Uvicorn |
Proxy | Nginx |
Process | Systemd |

---

## 🤝 Git 협업 전략

### Branch 전략

| 브랜치 | 역할 |
|--------|------|
| main | 배포 브랜치 |
| develop | 통합 브랜치 |
| feature/* | 기능 단위 브랜치 |

### Commit 컨벤션

```
feat: 기능 추가
fix: 버그 수정
docs: 문서 수정
refactor: 코드 리팩토링
test: 테스트 코드
```

---

## 👥 역할 분담

| 이름 | 역할 |
|------|------|
| 조장 김기훈 | 권한 / JWT인증 |
| 팀원 최건희 | DB및 환경변수/질문 스크래핑/UI |
| 팀원 이성현 | 일기 CRUD/페이징 및 정렬/ README 작성/ |
| 팀원 이아진 | 명언 스크래핑/서버관리
|  

---

## ✅ 회고

- FastAPI 구조 설계 경험
- JWT 인증 및 토큰 블랙리스트 이해
- Tortoise ORM 모델링
- AWS 배포 경험
- Git 협업 workflow 습득

---

## 📞 Contact

| 항목 | 내용 |
|------|------|
GitHub | https://github.com/oz-union-be-14-team3
Email | nike000112@gmail.com
