# frontend

```
├─ public/
├─ src/                  // frontend src directory
│  ├─ assets/            // images, fonts, etc...
│  ├─ components/        // svelte pages components
│  ├─ lib/               // js, ts, svelte library
│  ├─ pages/             // svelte pages
│  ├─ static/
│  ├─ store/             // svelte store
│  ├─ app.css            // tailwindCSS
│  ├─ App.svelte         // svelte main
│  ├─ main.js            // frontend main
│  └─ routes.ts          // svelte router
├─ .gitignore            // frontend gitignore
├─ index.html            // base index.html
├─ package.json          // vite/svelte/tailwindcss
├─ postcss.config.js
├─ svelte.config.js
├─ tailwind.config.js
├─ tsconfig.json
└─ vite.config.js
```

프론트엔드는 vite + svelte + tailwindcss를 사용합니다.

vite는 webpack과 같은 번들러입니다. 하지만 webpack과는 다르게 빌드 시간이 매우 빠릅니다.

svelte 설치 방법

```bash
npm install
```

설치 후 실행

```bash
npm run dev
```

빌드

```bash
npm run build
```
