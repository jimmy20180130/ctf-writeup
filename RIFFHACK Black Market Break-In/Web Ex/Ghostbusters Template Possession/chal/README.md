## Summary

The Ghostbusters containment HUD, where haunted template text starts warping the render pipeline.

## Running the challenge

**Docker (from sources):** From the challenge directory:

```bash
docker build -t ghostbusters-template-possession .
docker run -p 8080:8080 -e FLAG="bitctf{{custom_flag}}" ghostbusters-template-possession
```

**Docker (from Docker Hub):**

```bash
docker pull biterra/ghostbusters-template-possession:latest
docker run -p 8080:8080 -e FLAG="your_flag_here" biterra/ghostbusters-template-possession:latest
```

**Docker (publish multi-arch image):**

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t biterra/ghostbusters-template-possession:latest \
  --push .
```

**Local (Python):** Ensure Python 3.11+ is available. From the challenge directory: `pip install -r requirements.txt`, set `FLAG` (e.g. `export FLAG="bitctf{{local_test_flag}}"`), then `python app.py`. Service binds to `0.0.0.0:8080`.

Visit the service at `http://localhost:8080`.

## Vulnerability

### Type

Server-Side Template Injection (SSTI)

### Initial state

Players load a neon-styled "Ecto-Containment Console" where they can paste a "chant" that supposedly reformats P.K.E. readouts. The interface hints that control blocks are stripped, nudging players to toy with Jinja syntax while seeing live previews of their chant output.

### Discovery

Using browser developer tools or simple payloads like `{{ 7*7 }}` inside the chant field immediately shows arithmetic results instead of literal text, revealing that Jinja expressions are still executed. Even after noticing that `{% ... %}` blocks disappear, expression delimiters remain intact. Observing blocked keywords in the flash messages ("Spectral firewall rejected that fragment") confirms that only a very small blacklist is in play, making further probing trivial. At this point players recognize a classic SSTI scenario: server-rendered user input with ineffective filtering.

### Technical details

`app.py` takes the chant, strips `{%`/`%}` pairs via `scrub_chant`, and checks for a handful of fragments (`config`, `self`, `request`). The filtered text is passed straight into `render_template_string`. Because the entire chant is evaluated as a Jinja template, any remaining `{{ }}` expression executes in the server context. Jinja exposes helper objects like `cycler` whose constructor retains a reference to module globals, including `__builtins__`. Attackers can therefore pivot from harmless math to Python object access, import the `os` module, and read arbitrary files or environment variables. The Flask app injects runtime data (`ecto_status`, `proton_level`, `spectral_density`, `sealed_checksum`) through a context processor, meaning sensitive process state is just one expression away.

### Exploit

Crafting a chant such as `{{ cycler.__init__.__globals__.__builtins__.__import__('os').environ['FLAG'] }}` returns the flag because the payload imports `os` via builtins and reads the `FLAG` environment variable exposed inside the container. The provided `exploit.py` automates the process: it POSTs the malicious chant to `/`, verifies the HTTP 200 response, and regexes `bitctf{{...}}` from the HTML. No special headers or sessions are required, so the exploit is reliable both locally and against a remote deployment.

### Root cause

Designers attempted to "sanitize" user templates by stripping control tags and blacklisting a few substrings, but they still execute untrusted input via `render_template_string`. Expressions remained untouched, meaning arbitrary Jinja evaluation survived. Fundamental issue: rendering user-supplied template code without sandboxing or whitelisting a safe subset.

### Educational value

Players practice identifying SSTI by observing dynamic rendering differences, escalate from benign expressions to full environment reads, and learn how helpers like `cycler` expose Python internals. The scenario mirrors real incidents where server-side markdown or email templating mistakenly evaluates user input. Preventing this requires treating templates as code: render only trusted strings, escape user content, or switch to safe evaluators (e.g., `jinja2.sandbox.SandboxedEnvironment`) with strict allowlists. The challenge reinforces why blacklist-based filters are brittle and why environment-provided secrets must assume server compromise.