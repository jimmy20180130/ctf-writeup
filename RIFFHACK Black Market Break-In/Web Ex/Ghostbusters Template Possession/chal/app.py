#!/usr/bin/env python3
import os
from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash
from jinja2 import TemplateError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "ecto-secret-key")

FLAG = os.environ.get("FLAG", "bitctf{{gh057ly_j1nj4_p0ss35510n}}")

BLOCKED_FRAGMENTS = ("config", "self", "request")
DEFAULT_CHANT = "Manifest level: {{ ecto_status }} | Proton surge: {{ proton_level }}"


def scrub_chant(chant: str) -> str:
    """Attempt to remove control structures but still vulnerable to expression injection."""
    return chant.replace("{%", "").replace("%}", "")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        chant = request.form.get("chant", "").strip()
        if not chant:
            flash("Provide a chant for the containment console.")
            return redirect(url_for("index"))

        if len(chant) > 600:
            flash("Chant too long; the console destabilizes.")
            return redirect(url_for("index"))

        lowered = chant.lower()
        for fragment in BLOCKED_FRAGMENTS:
            if fragment in lowered:
                flash("Spectral firewall rejected that fragment.")
                return redirect(url_for("index"))

        filtered = scrub_chant(chant)
        try:
            rendered = render_template_string(filtered)
        except TemplateError as exc:
            flash(f"Chant failed to compile: {exc}")
            return redirect(url_for("index"))

        return render_template(
            "index.html",
            rendered=rendered,
            default=DEFAULT_CHANT,
            last_input=chant,
        )

    return render_template("index.html", rendered=None, default=DEFAULT_CHANT, last_input=None)


@app.route("/healthz")
def healthz():
    return {"status": "ok"}


@app.context_processor
def inject_defaults():
    return {
        "ecto_status": "unstable",
        "proton_level": 321,
        "spectral_density": "0x9e3779b9",
        "sealed_checksum": len(FLAG),
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)