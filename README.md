# Podium Bots · Starter bot (Python)

Bot mínimo para la liga **gratuita** de bots de pronósticos de La Quiniela de [Podium Bots](https://podiumbots.com).
Solo Python 3.9+ y la biblioteca estándar: sin dependencias.

> **+18.** Podium Bots no admite apuestas, no guarda dinero, no da premios, no promete aciertos ni ganancias y no está afiliado a ningún operador. Si el juego te hace daño: 900 200 225 (FEJAR, gratuito).

## Qué hace
1. `GET /api/v1/bots/me` — comprueba tu clave.
2. `GET /api/v1/jornadas/current` — lee la jornada abierta (15 partidos, `lock_at`, `accepting_predictions`).
3. Construye una columna con `strategy()` (por defecto, siempre "1" y Pleno 1-0).
4. Solo con `--submit`: `POST /api/v1/jornadas/{season}/{number}/predictions`.

## Registro (una vez)
Crea el bot en <https://podiumbots.com/bots> o por API:
```bash
curl -s https://podiumbots.com/api/v1/bots/register \
  -H 'Content-Type: application/json' \
  -d '{"nick":"mi_bot_quiniela","accept_terms":true}'
```
La respuesta muestra la clave `pb_...` **una sola vez**. Guárdala en `.env` (nunca en el repo ni en una URL). Luego puedes vincular el bot a tu cuenta en /cuenta.

Comprobar un nick: `python bot.py --check-nick mi_bot_quiniela`

## Ejecutar
```bash
cp .env.example .env        # pon tu PODIUM_API_KEY
python bot.py               # ensayo: lee y muestra, no envía nada
python bot.py --submit      # envía (sustituye tu envío anterior en esa jornada)
```
Para automatizarlo basta un cron semanal antes del cierre, p. ej. `0 10 * * 6 cd /ruta && python bot.py --submit`.

## Haz tu propio modelo
Edita `strategy(match)`: recibe `home`, `away`, `competition`, `kickoff` y devuelve `1`, `X`, `2` o dobles/triples (`1X`, `12`, `X2`, `1X2`).
Límites: 1–10 columnas, máx. 81 combinaciones en total, 30 envíos/hora, 120 lecturas/hora. Docs: <https://podiumbots.com/api> · OpenAPI: <https://podiumbots.com/openapi.json>

---

## English
Minimal, dependency-free Python starter for the free, 18+, no-gambling La Quiniela bot league at podiumbots.com. Register a bot (`POST /api/v1/bots/register`), put the `pb_` key in `.env`, run `python bot.py` (dry run) and `python bot.py --submit` to send your column. Replace `strategy()` with your model. No betting, no prizes, no promise of winnings. MIT licensed.
