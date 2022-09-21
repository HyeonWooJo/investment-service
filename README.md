# 📋목차

1. investment-service
2. 구현사항
3. 기술 스택
4. API Endpoints
5. ERD
6. 참조 문서

<br>

---

# 1. investment-service
- 설명: 증권 투자 및 계좌 관리 서비스
- 개발 기간: 2022.09.16 ~ 2022.09.21

<br>

---


# 2. 구현 사항

## 1) 데이터 업로더

- 제공되는 데이터 셋을 API에서 사용할 수 있도록 정제하여 DB에 업로드
- 오류 데이터가 있을 경우 이를 제외한 데이터만 업로드

<br>

## 2) 투자화면 데이터 조회 API

- 계좌명, 증권사 등 기본적인 계좌 정보들을 조회할 수 있는 API

<br>

## 3) 투자상세 화면 데이터 조회 API

- 계좌 정보와 투자 원금, 총 수익금, 수익률을 조회할 수 있는 API
- 총 수익금, 수익률은 DB 내에 저장되어 있지 않음
- 총 자산, 투자 원금, 총 수익금을 연산 처리하여 총 수익금, 수익률을 반환

<br>

## 4) 보유 종목 조회 API

- 유저가 보유하고 있는 종목을 조회할 수 있는 API
- 보유 종목 평가 금액은 DB에 저장되어 있는 종목 보유 수량과 종목 현재가를 곱해서 반환

<br>

## 5) 투자금 입금 API

### 투자금 유효성 검사 API

- 계좌번호, 고객명, 거래금액을 요청 데이터로 받음
- 전달한 계좌번호의 계좌가 전달한 고객명으로 되어 있는지 유효성 검사
- 식별자를 클라이언트에 반환


<br>

### 투자금 입금 API

- 식별자와 계좌번호, 고객명, 거래금액을 해싱 처리한 시그니처를 요청 데이터를 받음
- 식별자로부터 식별자와 연결된 계좌번호, 고객명, 거래금액을 뽑아낸 후 해당 데이터를 해싱 처리한 값과 시그니처 값을 비교하여 유효성 검사
- 유효성 검사 통과 후 계좌에 거래금액 입금 진행


<br>

---

# 3. 기술 스택
Language | Framwork | Database | HTTP | Tools
| :----------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------: | 
| <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> | <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> | <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> | <img src="https://img.shields.io/badge/postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white"> | <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> 


<br>

---

# 4. API Endpoints
| endpoint | HTTP Method | 기능   | require parameter                                                                                                   | response data |
|----------|-------------|------|---------------------------------------------------------------------------------------------------------------------|---------------|
| /apis/account/:int:/  | GET   | 투자화면 데이터 조회 |  없음  | 투자화면 데이터 |
| /apis/account-asset/:int:/ | GET   | 투자화면 상세 데이터 조회 |  없음  | 투자화면 상세 데이터 |
| /apis/my-holding/:int:/  | GET   | 보유 종목 조회 |  없음  | 보유 종목 데이터 |
| /apis/deposit-validation/  | POST   | 투자금 입금 유효성 검사 |  account_number: int <br> user_name: str <br> transfer_amount: int | 식별자 |
| /apis/deposit/  | POST   | 투자금 입금 |  transfer_identifier: int <br> signature: str | 입금 성공 여부 |

<br>

---

# 5. ERD
![](https://user-images.githubusercontent.com/65996045/191393108-2e9cdf4f-387e-452a-b22d-be6011ee95bd.png)

<br>

---

# 6. 참조 문서
- [Postman API Docs](https://documenter.getpostman.com/view/21254145/2s7YYvYgZn)


