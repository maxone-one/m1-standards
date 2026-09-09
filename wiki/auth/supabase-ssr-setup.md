# Supabase SSR Auth: das vollständige Middleware-Setup

**Herkunft:** Bis zum 09.09.2026 stand das hier im Standard `018-auth-db.md`, Abschnitt A.
Beim Neuschnitt ist der Code hierher gewandert, **ohne dass eine Zeile entfallen ist**.

**Die Regel steht in**
[`standards/014-auth-und-db-trennung.md`](../../standards/014-auth-und-db-trennung.md)
**Abschnitt A**: Die Auth-Middleware läuft auf **allen** Routes außer Static-Assets, niemals
auf einem selektiven Matcher. Dort steht auch der Pflicht-Matcher und die Begründung. Hier
steht der Code dazu.

## Next.js

```ts
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value));
          supabaseResponse = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options));
        },
      },
    }
  );
  await supabase.auth.getUser();

  // Bei Redirects: Cookies mitschleppen
  function redirectWithCookies(url: URL) {
    const res = NextResponse.redirect(url);
    supabaseResponse.headers.getSetCookie().forEach(c => res.headers.append("set-cookie", c));
    return res;
  }
  return supabaseResponse;
}
```

**Next.js 16:** Die Datei heißt `proxy.ts` und exportiert `proxy(request)` statt
`middleware(request)`. Beide Dateien gleichzeitig führen zum Build-Fehler.

## SvelteKit

In `src/hooks.server.ts`. **Der `try/catch` ist nicht optional:** ohne ihn killt der async
Auth-Refresh den Node-Prozess, sobald die Response bereits gesendet ist.

```ts
setAll: (cookies) => {
  try {
    cookies.forEach(({ name, value, options }) =>
      event.cookies.set(name, value, { ...options, path: '/' }));
  } catch { /* Response bereits gesendet */ }
}
```
