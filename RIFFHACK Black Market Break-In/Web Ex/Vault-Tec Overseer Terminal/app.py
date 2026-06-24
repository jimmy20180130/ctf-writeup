import os
import secrets
from flask import (
    Flask,
    make_response,
    redirect,
    render_template_string,
    request,
    url_for,
)
from markupsafe import Markup, escape
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# The Overseer's sealed directive lives only in the terminal's process
# environment. Vault residents are never meant to read it. Note it is NOT placed
# in Flask config, so the usual "{{ config }}" reflex is a dead end here.
os.environ.setdefault(
    "FLAG", "bitctf{{w4r_n3v3r_ch4ng3s_0verseer_t3rm1nal_pwn3d}}"
)
FLAG = os.environ["FLAG"]
VAULT_ID = "101"

# In-memory resident registry and active terminal sessions.
RESIDENTS = {}
SESSIONS = {}

PAGE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ROBCO TERMLINK :: VAULT {{ vault_id }}</title>
    <style>
        :root {
            --amber:#33ff66;
            --amber-dim:#1f9b3f;
            --bg:#04140a;
        }
        * { box-sizing: border-box; }
        html, body { height: 100%; }
        body {
            margin: 0;
            background: var(--bg);
            color: var(--amber);
            font-family: "Courier New", "Lucida Console", monospace;
            letter-spacing: 0.06em;
            text-shadow: 0 0 6px rgba(51,255,102,0.55);
            line-height: 1.5;
        }
        /* CRT curvature + vignette */
        body::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 50;
            background: radial-gradient(ellipse at center, rgba(4,20,10,0) 55%, rgba(0,0,0,0.85) 100%);
        }
        /* scanlines + phosphor flicker */
        body::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 49;
            background: repeating-linear-gradient(
                to bottom,
                rgba(0,0,0,0) 0px,
                rgba(0,0,0,0) 2px,
                rgba(0,0,0,0.28) 3px,
                rgba(0,0,0,0.28) 4px);
            animation: flicker 6s infinite;
        }
        @keyframes flicker {
            0%,100%{opacity:.92}
            50%{opacity:.99}
            8%{opacity:.86}
        }
        .wrap {
            max-width: 860px;
            margin: 0 auto;
            padding: 2.4rem 1.6rem 4rem;
            position: relative;
            z-index: 1;
        }
        .boot {
            font-size: .82rem;
            color: var(--amber-dim);
            white-space: pre-wrap;
            margin-bottom: 1.6rem;
        }
        h1 {
            font-size: 1.5rem;
            margin: 0 0 .2rem;
            text-transform: uppercase;
        }
        h2 {
            font-size: 1rem;
            text-transform: uppercase;
            border-bottom: 1px solid var(--amber-dim);
            padding-bottom: .35rem;
        }
        a { color: var(--amber); }
        a:hover {
            background: var(--amber);
            color: var(--bg);
            text-shadow:none;
        }
        .panel {
            border: 1px solid var(--amber-dim);
            padding: 1.1rem 1.2rem;
            margin: 1.2rem 0;
            background: linear-gradient(180deg, rgba(51,255,102,0.04), rgba(51,255,102,0));
        }
        label {
            display:block;
            text-transform: uppercase;
            font-size:.8rem;
            margin-top:.7rem;
            color: var(--amber-dim);
        }
        input, textarea {
            width: 100%;
            background: #021007;
            border: 1px solid var(--amber-dim);
            color: var(--amber);
            font-family: inherit;
            padding: .55rem .6rem;
            margin-top:.25rem;
            text-shadow:none;
        }
        textarea {
            min-height: 4.5rem;
            resize: vertical;
        }
        button, .btn {
            display:inline-block;
            margin-top:1rem;
            background:#021007;
            border:1px solid var(--amber);
            color:var(--amber);
            font-family:inherit;
            text-transform:uppercase;
            letter-spacing:.12em;
            padding:.55rem 1.1rem;
            cursor:pointer;
        }
        button:hover, .btn:hover {
            background: var(--amber);
            color: var(--bg);
            text-shadow:none;
        }
        .menu a {
            display:block;
            padding:.2rem 0;
        }
        .menu a::before { content:"> "; }
        .greet {
            border:1px dashed var(--amber-dim);
            padding:1rem;
            margin:1rem 0;
            min-height:2rem;
        }
        .err {
            color:#ff5c5c;
            text-shadow:0 0 6px rgba(255,92,92,.6);
        }
        .muted {
            color: var(--amber-dim);
            font-size:.85rem;
        }
        .cursor::after {
            content:"_";
            animation: blink 1s steps(1) infinite;
        }
        @keyframes blink { 50% { opacity: 0; } }
        footer {
            margin-top:2.4rem;
            color:var(--amber-dim);
            font-size:.72rem;
        }
    </style>
</head>
<body>
    <div class="wrap">
        <div class="boot">ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL ESTABLISHING UPLINK TO VAULT-TEC OVERSEER MAINFRAME .... OK VAULT {{ vault_id }} :: LIFE-SUPPORT NOMINAL :: RAD LEVELS NOMINAL {{ flavor }}</div>
        <h1>{{ title }}</h1>
        {{ body }}
        <footer>VAULT-TEC (R) -- PREPARING FOR THE FUTURE, TODAY. UNAUTHORIZED ACCESS IS A REGISTERED VIOLATION OF YOUR RESIDENCY AGREEMENT.<span class="cursor"></span></footer>
    </div>
</body>
</html>"""


def render_page(
    title, body_html, flavor="ALL RESIDENTS REPORT TO YOUR ASSIGNED TERMINAL."
):
    return render_template_string(
        PAGE,
        title=title,
        body=Markup(body_html),
        vault_id=VAULT_ID,
        flavor=flavor,
    )


def current_resident():
    token = request.cookies.get("pipboy_token", "")
    username = SESSIONS.get(token)
    if not username:
        return None
    return RESIDENTS.get(username)


@app.route("/")
def index():
    body = """
    <div class="panel">
        <p>WELCOME, RESIDENT. THIS TERMINAL GRANTS ACCESS TO VAULT 101 RESIDENT SERVICES.</p>
        <div class="menu">
            <a href="/enroll">ENROLL NEW RESIDENT</a>
            <a href="/access">ACCESS RESIDENT TERMINAL</a>
        </div>
    </div>
    <p class="muted">OVERSEER BROADCASTS ARE RESTRICTED. RESIDENT GREETINGS ARE DISPLAYED ON YOUR PERSONAL TERMINAL.</p>
    """
    return render_page("VAULT 101 RESIDENT TERMINAL", body)


@app.route("/enroll", methods=["GET", "POST"])
def enroll():
    if request.method == "POST":
        username = request.form.get("vault_id", "").strip().lower()
        access_code = request.form.get("access_code", "")

        if not username or not username.replace("-", "").replace(
            "_", ""
        ).isalnum():
            return (
                render_page(
                    "ENROLLMENT ERROR",
                    "<p class='err'>VAULT ID MUST BE ALPHANUMERIC.</p><p><a href='/enroll'>RETRY</a></p>",
                ),
                400,
            )

        if len(access_code) < 8:
            return (
                render_page(
                    "ENROLLMENT ERROR",
                    "<p class='err'>ACCESS CODE MUST BE 8+ CHARACTERS.</p><p><a href='/enroll'>RETRY</a></p>",
                ),
                400,
            )

        if username in RESIDENTS:
            return (
                render_page(
                    "ENROLLMENT ERROR",
                    "<p class='err'>RESIDENT ID ALREADY REGISTERED.</p><p><a href='/enroll'>RETRY</a></p>",
                ),
                409,
            )

        RESIDENTS[username] = {
            "code_hash": generate_password_hash(access_code),
            "clearance": "resident",
            "greeting": "PIP-BOY ONLINE. STAY SAFE DOWN HERE.",
        }

        token = secrets.token_urlsafe(24)
        SESSIONS[token] = username
        resp = make_response(redirect(url_for("terminal")))
        resp.set_cookie("pipboy_token", token, httponly=True, samesite="Lax")
        return resp

    body = """
    <div class="panel">
        <form method="post">
            <label>ASSIGN VAULT ID</label>
            <input name="vault_id" autocomplete="username" placeholder="e.g. resident-a7">
            <label>SET ACCESS CODE</label>
            <input name="access_code" type="password" autocomplete="new-password">
            <button>ENROLL</button>
        </form>
    </div>
    <p><a href="/access">RETURN TO ACCESS TERMINAL</a></p>
    """
    return render_page(
        "NEW RESIDENT ENROLLMENT",
        body,
        flavor="VAULT-TEC THANKS YOU FOR CHOOSING SURVIVAL.",
    )


@app.route("/access", methods=["GET", "POST"])
def access():
    if request.method == "POST":
        username = request.form.get("vault_id", "").strip().lower()
        access_code = request.form.get("access_code", "")
        resident = RESIDENTS.get(username)

        if not resident or not check_password_hash(
            resident["code_hash"], access_code
        ):
            return (
                render_page(
                    "ACCESS DENIED",
                    "<p class='err'>INVALID RESIDENT CREDENTIALS.</p><p><a href='/access'>RETRY</a></p>",
                ),
                403,
            )

        token = secrets.token_urlsafe(24)
        SESSIONS[token] = username
        resp = make_response(redirect(url_for("terminal")))
        resp.set_cookie("pipboy_token", token, httponly=True, samesite="Lax")
        return resp

    body = """
    <div class="panel">
        <form method="post">
            <label>VAULT ID</label>
            <input name="vault_id" autocomplete="username">
            <label>ACCESS CODE</label>
            <input name="access_code" type="password" autocomplete="current-password">
            <button>ACCESS</button>
        </form>
    </div>
    <p><a href="/enroll">ENROLL NEW RESIDENT</a></p>
    """
    return render_page("RESIDENT ACCESS TERMINAL", body)


@app.route("/terminal")
def terminal():
    resident = current_resident()
    if not resident:
        return redirect(url_for("access"))

    # SSTI sink: the resident greeting is rendered as a template so residents can
    # use VAULT-TEC inscription macros. The inscription is evaluated against the
    # full Jinja terminal context, so a resident can pivot out to the runtime.
    raw = resident.get("greeting", "")
    try:
        rendered = render_template_string(raw)
    except Exception:
        rendered = "[INSCRIPTION RENDER FAULT]"

    body = f"""
    <div class="panel">
        <p>RESIDENT TERMINAL ACTIVE. CLEARANCE: <strong>{escape(resident.get('clearance'))}</strong></p>
        <h2>PERSONAL GREETING</h2>
        <div class="greet">{Markup(rendered)}</div>
        <div class="menu">
            <a href="/inscribe">EDIT TERMINAL GREETING</a>
            <a href="/overseer">OVERSEER BROADCAST CHANNEL</a>
            <a href="/logout">SIGN OUT</a>
        </div>
    </div>
    <p class="muted">TIP: INSCRIPTION MACROS USE VAULT-TEC DOUBLE-BRACE SYNTAX.</p>
    """
    return render_page(
        "RESIDENT TERMINAL", body, flavor=f"SESSION ESTABLISHED FOR RESIDENT {VAULT_ID}."
    )


@app.route("/inscribe", methods=["GET", "POST"])
def inscribe():
    resident = current_resident()
    if not resident:
        return redirect(url_for("access"))

    message = ""
    if request.method == "POST":
        greeting = request.form.get("greeting", "")
        if len(greeting) > 240:
            message = (
                "<p class='err'>INSCRIPTION EXCEEDS HOLOTAPE CAPACITY (240).</p>"
            )
        else:
            resident["greeting"] = greeting
            return redirect(url_for("terminal"))

    body = f"""
    <div class="panel">
        {message}
        <form method="post">
            <label>TERMINAL GREETING INSCRIPTION</label>
            <textarea name="greeting">{escape(resident.get('greeting', ''))}</textarea>
            <button>BURN TO HOLOTAPE</button>
        </form>
    </div>
    <p><a href="/terminal">BACK TO TERMINAL</a></p>
    """
    return render_page(
        "INSCRIBE GREETING", body, flavor="PERSONALIZE YOUR VAULT EXPERIENCE."
    )


@app.route("/overseer")
def overseer():
    resident = current_resident()
    if not resident:
        return redirect(url_for("access"))

    # The Overseer directive is never sent to resident clearance. This page only
    # confirms that the resident is locked out.
    if resident.get("clearance") != "overseer":
        body = """
        <div class="panel">
            <p class="err">ACCESS DENIED. OVERSEER CLEARANCE REQUIRED.</p>
            <p class="muted">THE SEALED DIRECTIVE NEVER LEAVES THE OVERSEER TERMINAL'S RUNTIME ENVIRONMENT.</p>
        </div>
        <p><a href="/terminal">BACK TO TERMINAL</a></p>
        """
        return (
            render_page("OVERSEER BROADCAST CHANNEL", body, flavor="OVERSEER EYES ONLY."),
            403,
        )

    return render_page(
        "OVERSEER BROADCAST CHANNEL",
        f"<div class='panel'><p>{escape(FLAG)}</p></div>",
    )


@app.route("/logout")
def logout():
    token = request.cookies.get("pipboy_token", "")
    SESSIONS.pop(token, None)
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie("pipboy_token")
    return resp


@app.route("/healthz")
def healthz():
    return {"status": "ok"}


@app.errorhandler(404)
def not_found(_):
    return (
        render_page(
            "SECTOR NOT FOUND",
            "<p class='err'>REQUESTED TERMINAL SECTOR DOES NOT EXIST.</p>",
        ),
        404,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))