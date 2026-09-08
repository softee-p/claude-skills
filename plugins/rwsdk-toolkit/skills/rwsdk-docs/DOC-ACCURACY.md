# RedwoodSDK Doc Accuracy — where the shipped docs disagree with the library

The `references/` files in this skill are a verbatim mirror of `docs/src/content/docs`
in `redwoodjs/sdk`. **That documentation lags the published `rwsdk` package.** This file
records every place where, at the last sync, a shipped reference file was wrong for the
current release, or where a released user-facing API has no documentation at all.

**Docs mirror synced:** 2026-09-08 · **`rwsdk` release at sync time:** 1.7.3

**How to use:** Read this file before trusting `references/` on any of the topics below.
Where a reference file is marked **superseded**, prefer the code in this file over the
`.mdx`. Everything here is self-contained — no repo or diff access is needed.

**Scope:** only divergences that change what a developer should write. Internal fixes,
dependency bumps, and build-pipeline changes are deliberately omitted.

---

## 1. Correction — React Compiler setup is wrong for Vite 8 / `@vitejs/plugin-react` v6

**Affects:** `references/guides/optimize/react-compiler.mdx` — **superseded, do not follow as written.**

That guide says "Use React 19, Vite 6+" and configures the compiler through the React
plugin's `babel` option. Per the **rwsdk 1.5.0** release notes, `@vitejs/plugin-react` v6
**no longer accepts the `babel` option**. Because the guide also tells you to install with
`@latest`, following it today produces a config that the plugin rejects.

**Before (as printed in the guide — breaks on `@vitejs/plugin-react` v6):**
```ts
react({
  babel: {
    plugins: ["babel-plugin-react-compiler"],
  },
}),
```

**After (Vite 8 / `@vitejs/plugin-react` v6):**
```ts
import babel from "@rolldown/plugin-babel";
import react, { reactCompilerPreset } from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [
    react(),
    babel({ presets: [reactCompilerPreset()] }),
    cloudflare({ viteEnvironment: { name: "worker" } }),
    redwood(),
  ],
});
```

If you are **not** using the React Compiler and pass no custom Babel options, plain
`react()` is enough — drop the `babel` option entirely.

**Which path applies:** check the installed `@vitejs/plugin-react` major version. v5 and
earlier still take `babel`; v6 does not. `rwsdk@1.7.3` accepts `vite@^6.2.6 || 7.x || 8.x`,
so a Vite 6/7 app on plugin-react v5 can keep the old config. Everything else in the
guide (install steps, DevTools "Memo ✨" verification, clearing `node_modules/.vite`)
is still correct.

**Files to check:** `vite.config.mts` / `vite.config.ts` — search for `babel:` inside a
`react(...)` call.

---

## 2. Behavior change — a failed client navigation now hard-reloads by default

**rwsdk 1.7.0** (PR #1277). **Undocumented.** The upstream PR calls this out as a
behavioral breaking change.

When `navigate()` or a back/forward (`popstate`) navigation throws — a network hiccup, an
expired auth token, a chunk missing after a deploy — the framework previously left the tab
stranded: the address bar showed the new route while the screen showed the old page,
permanently, until a manual reload.

Now the framework rolls back its internal URL bookkeeping and, **by default, performs a
hard navigation to the intended URL**, then rethrows. `navigate()` still rejects with the
original error, so the Promise contract is unchanged.

**Who this breaks:** an app that catches a `navigate()` rejection and deliberately stays on
the current document. Hard-load recovery now begins *before* that catch handler runs. Take
back control with the new `onNavigationError` option — when you supply it, the framework
performs no hard navigation of its own:

```tsx
import { initClient, initClientNavigation } from "rwsdk/client";

const { handleResponse, onHydrated } = initClientNavigation({
  onNavigationError({ error, href }) {
    // Framework does NOT hard-navigate when this is provided.
    toast.error(`Could not open ${href}`);
    reportToSentry(error);
  },
});

initClient({ handleResponse, onHydrated });
```

**Files to check:** `src/client.tsx`, and any `navigate(...).catch(...)` call sites.

---

## 3. Opt-in — navigation commit watchdog

**rwsdk 1.6.0** (PR #1273). **Undocumented.**

Under heavy main-thread CPU load, a navigation could fetch successfully but never commit,
leaving the URL and the rendered page permanently out of sync. Navigation payloads now
commit at default priority instead of inside an interruptible transition, which fixes the
common case with no config. (Trade-off: navigation renders are no longer time-sliced, so a
heavy navigation render blocks the main thread until it finishes.)

For commits that never begin at all — a hung fetch, a render error in the new tree, a
misbehaving custom transport — there is an **opt-in** watchdog. It is disabled unless
`navigationTimeoutMs` is set, so existing apps see no change:

```tsx
initClientNavigation({
  navigationTimeoutMs: 10_000,
  // Optional: replace the default hard-navigation recovery.
  onNavigationTimeout({ href }) {
    showStuckNavigationBanner(href);
  },
});
```

**Action:** additive. Consider setting `navigationTimeoutMs` on apps with heavy client work.

---

## 4. Opt-in — recovery for missing client chunks after a deploy

**rwsdk 1.3.0** (PR #1222). **Undocumented.**

After a deploy, a long-lived tab can request a `"use client"` chunk whose content hash no
longer exists. The dynamic import fails, React crashes, and the user gets a permanent blank
page. Reloading immediately is not safe either — the new worker may be live before its
assets are reachable.

`initClient()` accepts `onModuleNotFound`. It is **off by default**. The built-in
`"reloadWhenReady"` preset waits until the current route actually serves HTML again
(jittered exponential backoff), then reloads:

```ts
import { initClient, initClientNavigation } from "rwsdk/client";

const { handleResponse, onHydrated } = initClientNavigation();
initClient({
  handleResponse,
  onHydrated,
  onModuleNotFound: "reloadWhenReady",
});
```

For custom UX or observability, pass a callback instead — it receives a `RecoveryController`
exposing `state` and `attempts`. The SDK renders no recovery UI of its own:

```ts
initClient({
  onModuleNotFound: (controller) => {
    console.log("chunk missing", controller.state, controller.attempts);
  },
});
```

Debug logging is available under `window.__RWSDK_DEBUG__` / `window.__RWSDK_DEBUG_RECOVERY__`.

**Note:** an earlier `onDisconnected` recovery path was removed in the same release.
`use-synced-state` still reconnects on its own after a WebSocket drop; page-level recovery
is not the right layer for ordinary connection churn.

**Action:** additive, recommended for any app that deploys while users have tabs open.

---

## 5. New API — opting a link out of client-side navigation

**rwsdk 1.6.0** (PR #1271). **Undocumented.**

Internal links are soft-navigated by default, which breaks when you cross a boundary
between two sections that use different `Document`s — a public site at `/` and an admin
area at `/admin`, say. Two ways to force a real browser load:

**Per link — the `data-reload` attribute:**
```tsx
<a href="/admin" data-reload>Admin</a>
```

**App-wide — the `shouldIntercept` callback.** Return `true` for a soft navigation,
`false` for a full reload. It runs for anchor clicks, `navigate()` calls, and
back/forward (`popstate`):
```tsx
initClientNavigation({
  shouldIntercept({ toUrl, fromUrl }) {
    const isAdmin = (url: URL) => url.pathname.startsWith("/admin");
    return isAdmin(toUrl) === isAdmin(fromUrl);
  },
});
```

Prefetching stays in sync: any `<link rel="x-prefetch">` that would end in a full reload is
skipped rather than warming a cache entry that will never be used.

**Action:** additive. Use it wherever two areas of one app ship different `Document`s.

---

## 6. Opt-in — `use-synced-state` hibernation transport

**rwsdk 1.3.0 / 1.3.1** (PRs #1235, #1237). **Undocumented.**

A hibernation-based transport for `use-synced-state` can be switched on at **build time**
via an import condition, with no handler rewrites and no second Durable Object class. Keep
importing from `rwsdk/use-synced-state/client` and `rwsdk/use-synced-state/worker`; add the
`rwsdk-use-synced-state-hibernation` condition to resolve them to the new implementation:

```ts
// vite.config.mts
resolve: {
  conditions: process.env.APP_ENV !== "production"
    ? ["rwsdk-use-synced-state-hibernation", "workerd", "browser", "import"]
    : ["workerd", "browser", "import"],
}
```

The shim keeps the legacy capnweb-style signatures for `registerKeyHandler`,
`registerSetStateHandler`, `registerGetStateHandler`, `registerSubscribeHandler`, and
`registerUnsubscribeHandler`, and legacy handlers that read `requestInfo.ctx` keep working.
**No wrangler migration is needed** — the exported Durable Object class name does not change.

When you are ready to make hibernation the default, drop the conditional and make the
condition unconditional. The dedicated `rwsdk/use-synced-state/hibernation/client` and
`rwsdk/use-synced-state/hibernation/worker` subpaths expose the new identity-first API
directly, unshimmed.

**Action:** additive and staged — production can stay on capnweb until you switch.

---

## 7. Version and peer-dependency facts not stated in the docs

As published in `rwsdk@1.7.3`:

| Peer dependency | Accepted range |
|---|---|
| `vite` | `^6.2.6 \|\| 7.x \|\| 8.x` |
| `react`, `react-dom`, `react-server-dom-webpack` | `>=19.2.0-0 <19.3.0 \|\| >=19.3.0-0 <20.0.0` |
| `@cloudflare/vite-plugin` | `^1.26.1` |
| `wrangler` | `^4.77.0` |
| `capnweb` | `~0.5.0 \|\| ~0.10.0` |

Vite 8 is the recommended path for new upgrade work; Vite 6/7 remain supported so apps can
migrate incrementally. Upgrading an app to Vite 8:

```sh
pnpm add rwsdk@latest
pnpm add -D vite@latest
pnpm add -D @vitejs/plugin-react@latest   # only if the app uses it
```

Then check every other Vite plugin in the app for a Vite 8-compatible version, and apply
the React Compiler correction in section 1 if the app passes Babel config to `react()`.
