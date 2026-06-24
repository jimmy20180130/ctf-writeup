# The Glitchy Contact System

## Description

Something in the marketplace isn't working quite right. Those who dig deeper find more than they bargained for.

## Solution Walkthrough

Entering `/contact` reveals that the entire page is broken, displaying a client-side exception error.

![alt text](image.png)

Open the developer tools console, and you can see the flag directly embedded in the thrown error message.

![alt text](image-1.png)

### Cause

This is a Next.js app. The contact client component takes the `flag` prop passed from the server and directly `throw`s it inside `useEffect`:

```js
function i(e){
  let{flag:t}=e;
  return useEffect(()=>{
    throw Error("Contact service initialization failed: missing transporter config. FLAG=".concat(t))
  },[t]),null
}
```

Because the flag is passed as a prop from the server component to the client component, it is serialized into the HTML (RSC payload) returned by the page. Therefore, you don't even need a browser; you can get it by simply fetching the HTML:

```bash
curl -s http://159.89.230.27/contact | grep -oE 'bitflag\{[^}]*\}'
# bitflag{d3bug_m0d3_1s_d4ng3r0us}
```

## Flag

```text
bitflag{d3bug_m0d3_1s_d4ng3r0us}
```
