# svelte + FastAPI + tailwindCSS + uvicorn(gunicorn)

```

├─ backend                  // fastapi + uvicorn
│  └─ main.py               // backend main - FastAPI
├─ frontend                 // svelte + tailwindcss
│  ├─ public
│  ├─ src                   // frontend src directory
│  │  ├─ components         //
│  │  ├─ lib                // js, ts, svelte library
│  │  ├─ pages              // svelte pages
│  │  ├─ static
│  │  ├─ app.css            // tailwindCSS
│  │  ├─ App.svelte         // svelte main
│  │  ├─ main.ts            // frontend main
│  │  └─ routes.ts          // svelte router
│  ├─ .gitignore            // frontend gitignore
│  ├─ index.html            // base index.html
│  ├─ package.json          // vite/svelte/tailwindcss
│  ├─ postcss.config.js
│  ├─ svelte.config.js
│  ├─ tailwind.config.js
│  ├─ tsconfig.json
│  └─ vite.config.ts
├─ .gitignore
└─ README.md
```

개인 포트폴리오 사이트를 위해 만든 프로젝트입니다.

완성된 페이지는 [여기](https://www.pieroot.xyz) 에서 확인 할 수 있습니다.

백엔드는 FastAPI를 사용하여 라우팅을 하고, vite 의 svelte-ts 템플릿을 사용하여 프론트엔드를 구성했습니다.

현재는 홈 페이지와 포트폴리오 페이지만 구현되어 있습니다.
