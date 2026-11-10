# CORS (Cross-Origin Resource Sharing, 교차 출처 리소스 공유)

CORS (Cross-Origin Resource Sharing, 교차 출처 리소스 공유)는 웹 브라우저가 보안상의 이유로 다른 출처(Origin)의 리소스에 접근하는 것을 기본적으로 차단(동일 출처 정책, SOP)할 때, 예외적으로 안전한 교류를 허용해 주는 표준 메커니즘입니다.

---

## 1. 왜 CORS가 존재할까요? (동일 출처 정책, SOP)

<img width="1671" height="941" alt="image" src="https://github.com/user-attachments/assets/782f0f2c-ec9f-42de-a166-cd8eaf79903f" />


* **동일 출처(Same-Origin):** 프로토콜(HTTP/HTTPS), 도메인(domain.com), 포트(3000, 8080 등)가 모두 일치하는 경우를 뜻합니다.
* **SOP (Same-Origin Policy):** 브라우저는 기본적으로 하나의 웹페이지에서 실행 중인 스크립트가 다른 출처의 리소스에 함부로 접근하지 못하도록 막습니다. 이를 통해 악성 사이트가 사용자의 쿠키나 세션을 이용해 다른 서비스(예: 은행 사이트)에서 정보를 탈취하는 것을 방지합니다.

하지만 현대 웹 서비스는 프론트엔드 서버와 백엔드 API 서버가 서로 다른 도메인/포트로 분리되어 있는 경우가 많기 때문에(예: `localhost:3000`과 `api.example.com`), 이 제도를 유연하게 풀어주는 **CORS**가 필수적입니다.

---

## 2. CORS는 어떻게 동작하나요?

브라우저가 다른 출처로 리소스를 요청할 때 HTTP 헤더를 통해 소통합니다. 대표적으로 두 가지 방식을 거칩니다.

* **예비 요청 (Preflight Request):**
실제 요청을 보내기 전, 브라우저는 `OPTIONS` 메서드를 사용해 서버에 *"이 도메인에서 이런 요청을 보내도 되나요?"*라고 먼저 사전 문의를 보냅니다. 서버가 허용 응답을 주면 그때 실제 요청을 보냅니다.
* **주요 응답 헤더:**
* `Access-Control-Allow-Origin`: 리소스 접근을 허용할 출처(도메인)를 지정합니다. (`*`로 설정하면 모든 곳 허용)
* `Access-Control-Allow-Methods`: 허용할 HTTP 메서드(GET, POST 등)를 지정합니다.

---

## 3. 개발하다 마주치는 CORS 에러 해결법

개발 중 콘솔창에 `CORS policy` 에러가 뜬다면 대부분 백엔드 서버에서 올바른 CORS 헤더를 내려주지 않았기 때문입니다.

* **서버 설정 (가장 올바른 방법):** 백엔드 코드에서 응답 헤더에 허용할 프론트엔드 출처를 명시합니다.
```http
Access-Control-Allow-Origin: https://my-frontend-domain.com

```


* **프록시(Proxy) 서버 활용:** 로컬 개발 환경에서는 프론트엔드 프록시 설정(예: Vite/Webpack DevServer Proxy)을 통해 브라우저가 동일 출처로 인식하도록 우회할 수 있습니다.
