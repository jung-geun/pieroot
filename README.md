# svelte + FastAPI + tailwindCSS + uvicorn(gunicorn)

[![Quality Gate Status](https://sonar.pieroot.xyz/api/project_badges/measure?project=pieroot_pieroot_598da0cf-84bb-44e0-b2cc-b93946dd2620&metric=alert_status&token=sqb_0cd1c62de713d658470bb234fa460b2089d94a1f)](https://sonar.pieroot.xyz/dashboard?id=pieroot_pieroot_598da0cf-84bb-44e0-b2cc-b93946dd2620)

[![Technical Debt](https://sonar.pieroot.xyz/api/project_badges/measure?project=pieroot_pieroot_598da0cf-84bb-44e0-b2cc-b93946dd2620&metric=sqale_index&token=sqb_0cd1c62de713d658470bb234fa460b2089d94a1f)](https://sonar.pieroot.xyz/dashboard?id=pieroot_pieroot_598da0cf-84bb-44e0-b2cc-b93946dd2620)

[![Bugs](https://sonar.pieroot.xyz/api/project_badges/measure?project=pieroot_pieroot_598da0cf-84bb-44e0-b2cc-b93946dd2620&metric=bugs&token=sqb_0cd1c62de713d658470bb234fa460b2089d94a1f)](https://sonar.pieroot.xyz/dashboard?id=pieroot_pieroot_598da0cf-84bb-44e0-b2cc-b93946dd2620)

```
├─ backend/                 // fastapi + uvicorn
├─ frontend/                // svelte + tailwindcss
├─ .gitignore
└─ README.md
```

개인 포트폴리오 사이트를 위해 만든 프로젝트입니다.

완성된 페이지는 [여기](https://www.pieroot.xyz) 에서 확인 할 수 있습니다.

백엔드는 FastAPI를 사용하여 라우팅을 하고, vite 의 svelte-ts 템플릿을 사용하여 프론트엔드를 구성했습니다.

현재는 홈, 포트폴리오, 로그인, 파일 업로드/다운로드, 각 템플릿 게시판 이 구현되어있습니다.

추후 연구하면서 만들 프로젝트를 연결할 예정입니다.
