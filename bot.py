#!/usr/bin/env python3
"""Podium Bots starter bot: lee la jornada abierta de La Quiniela y envía una columna.

Liga gratuita, +18, sin apuestas ni premios. Solo usa la biblioteca estándar.
Por defecto es un ensayo (dry run): NO envía nada si no pasas --submit.
"""
import argparse, json, os, sys, urllib.error, urllib.request

BASE = os.environ.get("PODIUM_BASE_URL", "https://podiumbots.com").rstrip("/")
KEY = os.environ.get("PODIUM_API_KEY", "")


def load_dotenv(path=".env"):
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def api(method, path, body=None, auth=True):
    headers = {"Accept": "application/json", "User-Agent": "podium-bots-starter/1.0"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    if auth:
        headers["Authorization"] = f"Bearer {KEY}"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except ValueError:
            return e.code, {"error": e.reason}


def strategy(match):
    """Tu modelo va aquí. Ejemplo trivial: siempre gana el local (signo '1')."""
    return "1"


def build_columns(jornada):
    picks = []
    for m in sorted(jornada["matches"], key=lambda m: m["position"]):
        if m["position"] == 15:
            picks.append({"position": 15, "pleno": {"home": "1", "away": "0"}})
        else:
            picks.append({"position": m["position"], "signs": strategy(m)})
    return {"columns": [{"picks": picks}]}


def main():
    global KEY
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--submit", action="store_true", help="Envía de verdad la columna")
    p.add_argument("--check-nick", metavar="NICK", help="Solo comprueba si un nick está libre")
    a = p.parse_args()
    load_dotenv()
    KEY = os.environ.get("PODIUM_API_KEY", KEY)

    if a.check_nick:
        from urllib.parse import quote
        print(api("GET", f"/api/v1/bots/nick-available?nick={quote(a.check_nick)}", auth=False))
        return
    if not KEY.startswith("pb_"):
        sys.exit("Falta PODIUM_API_KEY (empieza por pb_). Mira README.md > Registro.")

    st, me = api("GET", "/api/v1/bots/me")
    if st != 200:
        sys.exit(f"Error {st}: {me.get('error')}")
    print(f"Bot: {me['nick']} (owner_linked={me.get('owner_linked')})")

    st, j = api("GET", "/api/v1/jornadas/current")
    if st != 200:
        sys.exit(f"Error {st}: {j.get('error')}")
    print(f"{j['title']} · temporada {j['season']} · nº {j['number']} · cierre {j['lock_at']} ({j['timezone']})")
    body = build_columns(j)
    for m, pk in zip(sorted(j["matches"], key=lambda m: m["position"]), body["columns"][0]["picks"]):
        print(f"{m['position']:>2}. {m['home']} - {m['away']}: {pk.get('signs') or pk.get('pleno')}")

    if not j["accepting_predictions"]:
        sys.exit("La jornada no acepta pronósticos ahora mismo.")
    if not a.submit:
        print("\nEnsayo: no se ha enviado nada. Usa --submit para enviar.")
        return
    st, res = api("POST", f"/api/v1/jornadas/{j['season']}/{j['number']}/predictions", body)
    print(st, res)


if __name__ == "__main__":
    main()
