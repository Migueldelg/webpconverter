# Guía completa: De cero a web monetizada

## Índice
1. [Requisitos previos](#1-requisitos-previos)
2. [Subir el código a GitHub](#2-subir-el-código-a-github)
3. [Publicar con Vercel](#3-publicar-con-vercel)
4. [Comprar y conectar tu dominio](#4-comprar-y-conectar-tu-dominio)
5. [Google Analytics (medir tráfico)](#5-google-analytics-medir-tráfico)
6. [Google AdSense (monetizar)](#6-google-adsense-monetizar)
7. [SEO básico](#7-seo-básico)
8. [Cómo actualizar la web](#8-cómo-actualizar-la-web)

---

## 1. Requisitos previos

Antes de empezar necesitas tener creadas estas cuentas (todas gratuitas):

| Servicio | Para qué sirve | URL |
|---|---|---|
| **GitHub** | Guardar y versionar el código | github.com |
| **Vercel** | Hosting gratuito + deploy automático | vercel.com |
| **Google** | Analytics + AdSense | google.com |

> Si no tienes GitHub, créate una cuenta en [github.com](https://github.com) antes de continuar.

---

## 2. Subir el código a GitHub

> El repositorio debe ser **público** — Vercel necesita acceso para el deploy automático en el plan gratuito.

### Paso 1 — Crear el repositorio en GitHub.com

1. Ve a [github.com/new](https://github.com/new) (tienes que estar logado)
2. Rellena:
   - **Repository name**: `jpgtowebp`
   - **Description**: `Free JPG to WebP converter — runs in your browser`
   - Marca **Public**
   - **NO** marques "Add a README file" (ya tenemos archivos)
3. Haz clic en **"Create repository"**
4. GitHub te muestra una página con instrucciones — copia la URL del repo, será algo como `https://github.com/TU_USUARIO/jpgtowebp.git`

### Paso 2 — Subir el código desde la terminal

Abre la terminal, navega a la carpeta del proyecto y ejecuta:

```bash
# Entra en la carpeta del proyecto
cd /ruta/a/webconvertotowebp

# Inicializa git
git init

# Añade todos los archivos
git add .

# Primer commit
git commit -m "primera versión"

# Conecta con el repo de GitHub (sustituye TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/jpgtowebp.git

# Sube el código
git branch -M main
git push -u origin main
```

Si es la primera vez usando git, te pedirá autenticarte. GitHub ya no acepta contraseña — usa un **Personal Access Token**:
1. Ve a [github.com/settings/tokens](https://github.com/settings/tokens) → **"Generate new token (classic)"**
2. Dale scope `repo` y genera el token
3. Usa ese token como contraseña cuando te lo pida la terminal

✅ Tu código ya está en `github.com/TU_USUARIO/jpgtowebp`

---

## 3. Publicar con Vercel

Vercel es el hosting. Con el plan gratuito tienes todo lo que necesitas al principio.

1. Ve a [vercel.com](https://vercel.com) y haz clic en **"Sign up"**
2. Elige **"Continue with GitHub"** — así Vercel accede a tus repositorios
3. Una vez dentro, haz clic en **"Add New → Project"**
4. Busca tu repositorio `webconvertotowebp` y haz clic en **"Import"**
5. En la pantalla de configuración:
   - **Framework Preset**: Other (es HTML estático, no hace falta nada especial)
   - Deja todo lo demás por defecto
6. Haz clic en **"Deploy"**

Vercel tarda unos 30 segundos. Al terminar te da una URL tipo:
`https://webconvertotowebp.vercel.app`

🎉 **Tu web ya está pública en internet.**

Cada vez que hagas cambios en GitHub, Vercel los despliega automáticamente.

---

## 4. Comprar y conectar tu dominio

Un dominio propio (ej. `convertirwebp.com`) da más credibilidad y posicionamiento SEO.

### Comprar el dominio

Opciones recomendadas por precio:
- **Namecheap** → [namecheap.com](https://namecheap.com) (~10–12€/año)
- **Porkbun** → [porkbun.com](https://porkbun.com) (~8–10€/año)
- **Cloudflare Registrar** → [cloudflare.com/products/registrar](https://www.cloudflare.com/products/registrar/) (precio de coste, sin margen)

> Sugerencias de dominio: `convertirwebp.com`, `webpconverter.es`, `imagenaswebp.com`

### Conectar el dominio a Vercel

1. En tu proyecto de Vercel, ve a **Settings → Domains**
2. Escribe tu dominio (ej. `convertirwebp.com`) y haz clic en **Add**
3. Vercel te dará unos registros DNS. Tienes dos opciones:

**Opción recomendada — Nameservers de Vercel:**
- En tu proveedor de dominio, cambia los nameservers a los de Vercel:
  - `ns1.vercel-dns.com`
  - `ns2.vercel-dns.com`
- Vercel gestiona todo automáticamente, incluyendo el HTTPS

**Opción alternativa — Registro A + CNAME:**
- Crea un registro `A` apuntando a `76.76.21.21`
- Crea un registro `CNAME` de `www` apuntando a `cname.vercel-dns.com`

Los cambios DNS tardan entre 5 minutos y 48 horas en propagarse.

---

## 5. Google Analytics (medir tráfico)

Antes de pedir AdSense necesitas tener Analytics para ver cuántas visitas recibes.

1. Ve a [analytics.google.com](https://analytics.google.com)
2. Haz clic en **"Empezar a medir"**
3. Crea una cuenta → ponle el nombre de tu web
4. Crea una propiedad → elige **"Web"**
5. Introduce tu dominio
6. Google te dará un código similar a este:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

7. Pega ese código en `index.html`, dentro de la etiqueta `<head>`, justo antes de `</head>`
8. Guarda, sube a GitHub → Vercel lo desplegará automáticamente

---

## 6. Google AdSense (monetizar)

AdSense requiere que tu web tenga cierto tráfico y contenido antes de aprobarte. No te aprueba al instante.

### Paso 1 — Solicitar la cuenta

1. Ve a [adsense.google.com](https://adsense.google.com)
2. Haz clic en **"Empezar"**
3. Introduce tu dominio y tu email de Google
4. Acepta los términos y condiciones
5. Te pedirá añadir un código en tu web para verificarla:

```html
<meta name="google-adsense-account" content="ca-pub-XXXXXXXXXXXXXXXX">
```

Añade ese meta tag dentro de `<head>` en `index.html`.

### Paso 2 — Activar los anuncios en la web

Una vez aprobado (puede tardar días o semanas), descomenta las líneas de AdSense en `index.html`:

**Banner superior (728×90)** — busca y reemplaza el bloque de comentario:
```html
<!-- Google AdSense — descomentar cuando tengas aprobación -->
<ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px"
     data-ad-client="ca-pub-TU_ID_REAL"
     data-ad-slot="TU_AD_SLOT"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
```

**Anuncio cuadrado medio (336×280)** — mismo proceso con el segundo bloque.

También elimina o oculta los `<div class="ad-placeholder">` que son solo placeholders visuales.

### ¿Cuánto se gana?

Depende del país del visitante, nicho y CTR. Como referencia orientativa para una herramienta de utilidad:
- RPM (ingreso por 1.000 visitas): entre 0,5€ y 3€
- Con 10.000 visitas/mes → 5€ a 30€/mes inicialmente
- Con tráfico constante y buenas keywords → puede escalar

---

## 7. SEO básico

Para recibir visitas de Google necesitas posicionarte para búsquedas como:
- "convertir jpg a webp gratis"
- "pasar imagen a webp online"
- "convertidor png webp"

### Checklist SEO mínimo

- [x] **Título de página** claro con keywords → ya incluido en el `<title>`
- [x] **Meta description** → ya incluida
- [x] **H1 con keywords** → ya incluido
- [x] **Texto en la página** → ya hay sección informativa con texto indexable
- [ ] **Google Search Console** → regístrate en [search.google.com/search-console](https://search.google.com/search-console), añade tu dominio y envía el sitemap
- [ ] **Sitemap** → crea un archivo `sitemap.xml` (ver abajo)
- [ ] **Velocidad** → al ser HTML estático ya es muy rápida ✅

### Crear sitemap.xml

Crea un archivo `sitemap.xml` en la carpeta del proyecto:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://TUDOMINIO.com/</loc>
    <lastmod>2026-05-29</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>
```

Reemplaza `TUDOMINIO.com` con tu dominio real y sube el archivo a GitHub.

---

## 8. Cómo actualizar la web

El flujo de trabajo una vez todo esté montado es:

1. Edita `index.html` (u otros archivos) en tu ordenador
2. Abre **GitHub Desktop**
3. Verás los cambios listados → escribe un mensaje de commit (ej. "mejora diseño")
4. Haz clic en **"Commit to main"**
5. Haz clic en **"Push origin"**
6. Vercel detecta el push y despliega automáticamente en ~30 segundos ✅

---

## Resumen de pasos por orden

```
1. ✅ index.html creado
2. ⬜ Crear cuenta GitHub
3. ⬜ Subir proyecto a GitHub (GitHub Desktop)
4. ⬜ Crear cuenta Vercel y hacer deploy
5. ⬜ Comprar dominio
6. ⬜ Conectar dominio a Vercel
7. ⬜ Añadir Google Analytics
8. ⬜ Solicitar Google AdSense
9. ⬜ Añadir sitemap.xml y registrar en Search Console
10. ⬜ Esperar tráfico → activar anuncios cuando te aprueben
```
