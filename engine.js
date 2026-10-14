// Ride math - e-bike range honesty.
// The sticker miles belong to a 150 lb rider on level ground with the wind
// at his back. Weight, hills and the assist dial all ride the same battery.
// Verdicts judge the unrounded figure; rounding is for display only.
var RideMath = (function () {
  function pos(x) { return typeof x === "number" && isFinite(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }

  // Labeled norms.
  var TERRAIN = { flat: 1, rolling: 0.85, hilly: 0.65 };
  var WH_PER_MI = { eco: 8, tour: 12, sport: 18, turbo: 25 };

  function rangePlan(stickerMiles, riderLb, terrain) {
    if (!pos(stickerMiles)) return { error: "the sticker miles must be above zero" };
    if (!pos(riderLb)) return { error: "the rider weight must be above zero" };
    if (!TERRAIN[terrain]) return { error: "pick a terrain" };
    // Labeled norm: 0.4% off per pound over 170, floor at 70% kept.
    var w = Math.max(0.7, 1 - Math.max(0, riderLb - 170) * 0.004);
    var miles = stickerMiles * w * TERRAIN[terrain];
    return { miles: r1(miles) };
  }

  function renderRange(r, stickerMiles, riderLb, terrain) {
    return "Your " + stickerMiles + "-mile sticker with a " + riderLb + " lb rider on " + terrain
      + " roads figures about " + r.miles + " miles - the sticker rider weighed 150 and the wind was at his back.";
  }

  function wattPlan(wh, assist) {
    if (!pos(wh)) return { error: "the battery watt-hours must be above zero" };
    if (!WH_PER_MI[assist]) return { error: "pick an assist level" };
    var miles = wh / WH_PER_MI[assist];
    return { miles: r1(miles), rate: WH_PER_MI[assist] };
  }

  function renderWatt(r, wh, assist) {
    return "Your " + wh + " Wh battery in " + assist + " figures about " + r.miles
      + " miles at " + r.rate + " Wh a mile - the eco number on the box belongs to a different ride.";
  }

  function chargePlan(wh, chargerW) {
    if (!pos(wh)) return { error: "the battery watt-hours must be above zero" };
    if (!pos(chargerW)) return { error: "the charger watts must be above zero" };
    // Labeled norm: 15% taper on top of the nameplate watts.
    var hours = wh / chargerW * 1.15;
    return { hours: r1(hours) };
  }

  function renderCharge(r, wh, chargerW) {
    return "Your " + wh + " Wh battery on the " + chargerW + " W charger figures about " + r.hours
      + " hours empty to full - the last 15% is the slow part.";
  }

  return {
    rangePlan: rangePlan, renderRange: renderRange,
    wattPlan: wattPlan, renderWatt: renderWatt,
    chargePlan: chargePlan, renderCharge: renderCharge
  };
})();
if (typeof module !== "undefined") module.exports = RideMath;
