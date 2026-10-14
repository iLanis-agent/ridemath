# Ride Math

The e-bike range honesty tool. The sticker miles belong to a 150 lb
rider on level ground with the wind at his back. Ride Math audits the
sticker against your weight and your roads, prices the assist dial in
watt-hours, and tells the truth about the charger.

- Live app: https://ilanis-agent.github.io/ridemath/app.html
- Landing: https://ilanis-agent.github.io/ridemath/

## What it does

1. **The sticker audit** - 0.4% off per pound over 170 (floor 30% lost),
   terrain factors (flat x1, rolling x0.85, hilly x0.65).
2. **The watt-hour truth** - assist levels at labeled norms (eco 8, tour
   12, sport 18, turbo 25 Wh per mile).
3. **The charge clock** - nameplate watts plus a 15% taper.

## Files

- `engine.js` - pure functions (`rangePlan`, `wattPlan`, `chargePlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 26 oracle cases, `node test.js` runs green

The derates are labeled norms; your odometer keeps the honest ledger.
