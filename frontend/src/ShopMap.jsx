import "./ShopMap.css";

// This is the public Google Maps Embed URL copied from the user's
// Google Maps "Share > Embed a map" HTML snippet.
// It does not use a Google Cloud API key.
const SHOP_MAP_URL =
  "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1996.6539194411162!2d85.03675529285033!3d25.603103246509722!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39ed5777d1200c7b%3A0x338b2874c5d9442f!2sJK%20PLY%20HARDWARE%20AND%20FURNITURE%20WORKSHOP!5e1!3m2!1sen!2sin!4v1793791923361!5m2!1sen!2sin";

const GOOGLE_MAPS_DIRECTIONS_URL =
  "https://www.google.com/maps/dir/?api=1&destination=25.603103246509722%2C85.03675529285033";

export default function ShopMap() {
  return (
    <section className="shop-map" aria-labelledby="shop-map-title">
      <div className="shop-map__heading">
        <p className="shop-map__eyebrow">FIND OUR WORKSHOP</p>
        <h2 id="shop-map-title">Visit Our Workshop</h2>
        <p>Find JK Ply Hardware &amp; Furniture Workshop on Google Maps.</p>
      </div>

      <div className="shop-map__frame">
        <iframe
          title="JK Ply Hardware and Furniture Workshop location on Google Maps"
          src={SHOP_MAP_URL}
          width="100%"
          height="420"
          style={{ border: 0 }}
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
          allowFullScreen
        />
      </div>

      <a
        className="shop-map__directions"
        href={GOOGLE_MAPS_DIRECTIONS_URL}
        target="_blank"
        rel="noopener noreferrer"
      >
        Get directions on Google Maps <span aria-hidden="true">↗</span>
      </a>
    </section>
  );
}
