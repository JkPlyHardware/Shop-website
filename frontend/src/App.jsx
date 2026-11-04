import { useEffect, useMemo, useState } from "react";
import { Routes, Route, Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ArrowRight, ArrowUpRight, Hammer, Ruler, ShieldCheck, Truck, Phone, MapPin, Instagram, Facebook, CheckCircle2, Search, Menu, Sparkles } from "lucide-react";
import Navbar from "./components/Navbar";
import FestivalBanner from "./components/FestivalBanner";
import ProductCard from "./components/ProductCard";
import ChatWidget from "./components/ChatWidget";
import { api, makeIdempotencyKey } from "./services/api";
import ShopMap from "./ShopMap";
import GoogleReviewButton from "./components/GoogleReviewButton";

const categoriesFallback = ["Wooden Doors", "Beds", "Tables", "Bed Tables", "Plywood & Laminates", "Hardware", "Custom Furniture"];

function useTheme() {
  const [theme, setTheme] = useState(() => localStorage.getItem("jk-theme") || "light");
  useEffect(() => { document.documentElement.dataset.theme = theme; localStorage.setItem("jk-theme", theme); }, [theme]);
  return [theme, () => setTheme((v) => v === "light" ? "dark" : "light")];
}

function HomePage() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  useEffect(() => {
    Promise.all([api.products(), api.categories()]).then(([p, c]) => { setProducts(p); setCategories(c); }).catch(() => { }).finally(() => setLoading(false));
  }, []);
  useEffect(() => { const focus = () => document.getElementById("product-search")?.focus(); window.addEventListener("jk:focus-search", focus); return () => window.removeEventListener("jk:focus-search", focus); }, []);
  const filtered = useMemo(() => products.filter((p) => `${p.name} ${p.description} ${p.category?.name}`.toLowerCase().includes(query.toLowerCase())), [products, query]);
  return <>
    <section className="hero-section">
      <div className="hero-leaf hero-leaf-one" /><div className="hero-leaf hero-leaf-two" />
      <div className="container hero-grid">
        <div className="hero-copy">
          <p className="eyebrow">FURNITURE & PLYWOOD WORKSHOP <span>·</span> PATNA, BIHAR</p>
          <h1>Furniture that fits your home, <em>not the other way round.</em></h1>
          <p className="hero-description">Wooden doors, tables, beds, bed tables and custom furniture, built in our own workshop in Patna. Plywood, laminates and hardware you can inspect before you buy — and prices confirmed in writing before any work starts.</p>
          <div className="hero-buttons"><Link className="button" to="/collection">Explore the collection <ArrowRight size={18} /></Link><Link className="button button-outline" to="/contact">Get a quote</Link></div>
          <div className="hero-facts"><span><Phone size={17} /> +91 96613 82988</span><i /><span><Ruler size={18} /> Made to measure</span><i /><span><Hammer size={18} /> Own workshop</span></div>
        </div>
        <div className="hero-visual" aria-label="Furniture workshop showcase">
          <div className="hero-visual-top"><span>PATNA</span><span>BIHAR</span></div>
          <div className="showroom-art"><div className="art-window" /><div className="art-plant plant-a">♣</div><div className="art-plant plant-b">♣</div><div className="art-lamp" /><div className="art-chair" /><div className="art-console"><div /><div /><div /></div><div className="art-rug" /></div>
          <div className="hero-visual-brand"><strong>JK</strong><span>Ply & Furniture</span><small>DOORS · TABLES · BEDS · BED TABLES</small></div>
          <div className="hero-visual-footer"><span><Hammer size={16} /> Made in our workshop</span><span><CheckCircle2 size={16} /> Made to order</span></div>
          <div className="price-badge"><ShieldCheck size={18} /> Price confirmed before work starts</div>
        </div>
      </div>
      <div className="hero-bottom container"><span>CRAFTED FOR YOUR SPACE</span><span>MADE WITH CARE IN PATNA</span></div>
    </section>
    <FestivalBanner />
    <section className="section container" id="collection">
      <div className="section-heading"><div><p className="eyebrow">EXPLORE OUR RANGE</p><h2>Made for the way <em>you live.</em></h2></div><Link className="text-link" to="/collection">View all products <ArrowUpRight size={17} /></Link></div>
      <div className="category-pills">{(categories.length ? categories : categoriesFallback.map((name, i) => ({ id: i, name }))).map((c) => <button key={c.id} onClick={() => navigate(`/collection?category=${encodeURIComponent(c.slug || c.name)}`)}>{c.name}</button>)}</div>
      <div className="product-grid">{loading ? <p className="muted">Loading catalogue…</p> : filtered.slice(0, 4).map((p) => <ProductCard key={p.id} product={p} />)}{!loading && products.length === 0 && <div className="empty-state"><PackageIcon /><h3>Catalogue being updated</h3><p>Contact the workshop to discuss your furniture or material requirements.</p><Link className="text-link" to="/contact">Make an enquiry <ArrowRight size={16} /></Link></div>}</div>
      <div className="search-row"><div className="search-field"><Search size={18} /><input id="product-search" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search doors, beds, tables, plywood..." /></div></div>
    </section>
    <section className="workshop-band"><div className="container workshop-grid"><div><p className="eyebrow light">OUR WORKSHOP</p><h2>See the material.<br /><em>Know the price.</em></h2><p>Visit the workshop to inspect plywood, laminates and hardware before you decide. For custom furniture, share your requirements and measurements with our team.</p><Link to="/workshop" className="button button-light">About the workshop <ArrowRight size={17} /></Link></div><div className="workshop-points"><div><Ruler /><strong>Made to measure</strong><span>Furniture planned around your space.</span></div><div><Hammer /><strong>Own workshop</strong><span>Work built in our Patna workshop.</span></div><div><ShieldCheck /><strong>Price in writing</strong><span>Price confirmed before work starts.</span></div></div></div></section>
    <section className="section container"><div className="section-heading"><div><p className="eyebrow">HOW WE HELP</p><h2>From idea to <em>made-to-order.</em></h2></div></div><div className="service-grid"><ServiceCard icon={<Ruler />} title="Custom furniture" text="Discuss sizes, design preferences and practical needs for your home." /><ServiceCard icon={<PackageIcon />} title="Plywood & laminates" text="Explore material options and inspect products before you buy." /><ServiceCard icon={<Hammer />} title="Doors, beds & tables" text="Enquire about workshop-made furniture for your space." /></div></section>
    <ContactStrip />
  </>;
}

function PackageIcon() { return <span className="package-icon">JK</span>; }
function ServiceCard({ icon, title, text }) { return <article className="service-card"><span className="service-icon">{icon}</span><h3>{title}</h3><p>{text}</p><Link to="/contact" className="text-link">Enquire <ArrowUpRight size={16} /></Link></article>; }
function ContactStrip() { return <section className="contact-strip container"><div><p className="eyebrow light">LET'S PLAN YOUR SPACE</p><h2>Have a project in mind?</h2><p>Tell us what you need. We'll help you take the next step.</p></div><Link className="button button-light" to="/contact">Get a quote <ArrowRight size={18} /></Link></section>; }

function CollectionPage() {
  const [searchParams] = useSearchParams();
  const [products, setProducts] = useState([]); const [query, setQuery] = useState(""); const [category, setCategory] = useState(searchParams.get("category") || "all"); const [categories, setCategories] = useState([]);
  useEffect(() => { api.products().then(setProducts).catch(() => setProducts([])); api.categories().then(setCategories).catch(() => { }); }, []);
  const list = products.filter((p) => (category === "all" || p.category?.slug === category) && `${p.name} ${p.description}`.toLowerCase().includes(query.toLowerCase()));
  return <PageIntro eyebrow="THE COLLECTION" title={<>A considered range for <em>your home.</em></>}><div className="catalog-tools"><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search products..." aria-label="Search products" /><select value={category} onChange={(e) => setCategory(e.target.value)} aria-label="Filter by category"><option value="all">All categories</option>{categories.map((c) => <option key={c.id} value={c.slug}>{c.name}</option>)}</select></div><div className="product-grid">{list.map((p) => <ProductCard key={p.id} product={p} />)}</div>{!list.length && <EmptyNotice title="No matching catalogue items" text="Try another search or contact the workshop for a product enquiry." />}</PageIntro>;
}

function ProductPage() {
  const { slug } = useParams(); const [product, setProduct] = useState(null); const [error, setError] = useState(false);
  useEffect(() => { api.products().then((items) => setProduct(items.find((p) => p.slug === slug) || null)).catch(() => setError(true)); }, [slug]);
  if (error) return <EmptyNotice title="Could not load product" text="Please try again or contact the workshop." />;
  if (!product) return <div className="container page-loading">Loading product…</div>;
  return <main className="container product-detail"><div className="detail-image">{product.image_url ? <img src={product.image_url} alt={product.name} /> : <div className="product-placeholder"><PackageIcon /></div>}</div><div><p className="eyebrow">{product.category?.name}</p><h1>{product.name}</h1><p>{product.description}</p><p className="detail-price">{product.price ? `₹${Number(product.price).toLocaleString("en-IN")}` : "Price on enquiry"}</p><p className="muted">Availability and final pricing are confirmed by the workshop.</p><Link to={`/contact?product=${encodeURIComponent(product.name)}`} className="button">Enquire about this product <ArrowRight size={17} /></Link></div></main>;
}

function PageIntro({ eyebrow, title, children }) { return <main className="container inner-page"><div className="inner-heading"><p className="eyebrow">{eyebrow}</p><h1>{title}</h1></div>{children}</main>; }
function EmptyNotice({ title, text }) { return <div className="container empty-notice"><h2>{title}</h2><p>{text}</p><Link className="button" to="/contact">Contact the workshop</Link></div>; }

function SimplePage({ type }) {
  const configs = {
    services: { eyebrow: "WHAT WE DO", title: <>Practical help for <em>your space.</em></>, body: "Enquire about custom furniture, wooden doors, tables, beds, bed tables, plywood, laminates and hardware. Share your requirements with the workshop to discuss available options." },
    gallery: { eyebrow: "OUR WORK", title: <>A space for <em>project stories.</em></>, body: "Project photographs can be added by the administrator as genuine workshop work becomes available. We do not display sample customer projects as completed JK Ply work." },
    workshop: { eyebrow: "MADE IN PATNA", title: <>Built with care in <em>our workshop.</em></>, body: "JK Ply Hardware & Furniture Workshop is based in Patna, Bihar. Customers can inspect plywood, laminates and hardware before purchase. Custom furniture is discussed around your space and requirements; prices are confirmed in writing before work starts." },
    privacy: { eyebrow: "PRIVACY", title: <>Your details stay <em>with the enquiry.</em></>, body: "This local demo site sends the details you submit to its Django backend for the workshop to respond. It does not implement advertising trackers or collect payment details. Before public launch, the business owner should review and publish a privacy policy that reflects the final hosting, analytics and communication setup." },
    terms: { eyebrow: "TERMS", title: <>Clear details before <em>work begins.</em></>, body: "Product prices, material availability, measurements, timelines and final project specifications must be confirmed directly with the workshop. A website enquiry is a request for contact and is not an order confirmation or payment transaction." },
  };
  const c = configs[type]; return <PageIntro eyebrow={c.eyebrow} title={c.title}><div className="simple-content"><p>{c.body}</p><div className="simple-callout"><Hammer size={28} /><div><strong>Talk to the workshop</strong><span>+91 96613 82988</span></div><a href="tel:+919661382988" className="button">Call now <ArrowUpRight size={16} /></a></div></div></PageIntro>;
}


function ContactPage() {
  const params = new URLSearchParams(window.location.search);
  const product = params.get("product") || "";

  const [tab, setTab] = useState("quote");
  const [busy, setBusy] = useState(false);
  const [cooldown, setCooldown] = useState(false);
  const [notice, setNotice] = useState(null);

  const [form, setForm] = useState({
    customer_name: "",
    name: "",
    phone: "",
    email: "",
    product_name: product,
    message: "",
  });

  const update = (e) => {
    setForm((v) => ({
      ...v,
      [e.target.name]: e.target.value,
    }));
  };

  const submit = async (e) => {
    e.preventDefault();
    if (busy || cooldown) return;

    setBusy(true);
    setNotice(null);

    try {
      const payload =
        tab === "quote"
          ? {
              customer_name: form.customer_name,
              phone: form.phone,
              email: form.email,
              product_name: form.product_name,
              message: form.message,
            }
          : {
              name: form.name,
              phone: form.phone,
              email: form.email,
              message: form.message,
            };

      const res =
        tab === "quote"
          ? await api.quote(payload, makeIdempotencyKey())
          : await api.contact(payload, makeIdempotencyKey());

      setNotice({ type: "success", text: res.message });

      setForm({
        customer_name: "",
        name: "",
        phone: "",
        email: "",
        product_name: "",
        message: "",
      });

      setCooldown(true);
      window.setTimeout(
        () => setCooldown(false),
        tab === "quote" ? 5000 : 3000
      );
    } catch (err) {
      setNotice({ type: "error", text: err.message });
    } finally {
      setBusy(false);
    }
  };

  return (
    <PageIntro
      eyebrow="GET IN TOUCH"
      title={
        <>
          Let's make something <em>for your home.</em>
        </>
      }
    >
      <div className="contact-layout contact-layout--map">

        {/* LEFT SIDE: GOOGLE MAP */}
        <div className="contact-map-column">
          <ShopMap />
        </div>
        

        {/* RIGHT SIDE: CONTACT DETAILS AND FORM */}
        <div className="contact-side">

          <div className="contact-details">
            <h2>Talk to the workshop.</h2>

            <p>
              Call us or send a message with your requirements.
              We will get back to you through the contact details
              you provide.
            </p>

            <a className="contact-detail-link" href="tel:+919661382988">
              <Phone />
              +91 96613 82988
            </a>

            <div className="contact-detail-link">
              <MapPin />
              Patna, Bihar
            </div>

            <div className="contact-note">
              <ShieldCheck />
              <span>
                Prices are confirmed in writing before work starts.
              </span>
            </div>
          </div>

          <form className="enquiry-form" onSubmit={submit}>

            <div className="form-tabs">
              <button
                type="button"
                className={tab === "quote" ? "active" : ""}
                onClick={() => setTab("quote")}
              >
                Request a quote
              </button>

              <button
                type="button"
                className={tab === "contact" ? "active" : ""}
                onClick={() => setTab("contact")}
              >
                General message
              </button>
            </div>

            {notice && (
              <div className={`form-notice ${notice.type}`}>
                {notice.text}
              </div>
            )}

            <label>
              Your name
              <input
                name={tab === "quote" ? "customer_name" : "name"}
                value={tab === "quote" ? form.customer_name : form.name}
                onChange={update}
                required
                maxLength={100}
              />
            </label>

            <label>
              Phone number
              <input
                name="phone"
                value={form.phone}
                onChange={update}
                required
                type="tel"
                minLength={10}
                maxLength={20}
              />
            </label>

            <label>
              Email (optional)
              <input
                name="email"
                value={form.email}
                onChange={update}
                type="email"
                maxLength={254}
              />
            </label>

            {tab === "quote" && (
              <label>
                Product / requirement
                <input
                  name="product_name"
                  value={form.product_name}
                  onChange={update}
                  placeholder="Wooden door, bed, table..."
                  maxLength={180}
                />
              </label>
            )}

            <label>
              How can we help?
              <textarea
                name="message"
                value={form.message}
                onChange={update}
                required
                rows={4}
                maxLength={3000}
                placeholder="Share your requirements..."
              />
            </label>

            <button
              className="button form-submit"
              disabled={busy || cooldown}
            >
              {busy
                ? "Sending..."
                : cooldown
                  ? "Sent — please wait"
                  : tab === "quote"
                    ? "Send quote request"
                    : "Send message"}

              <ArrowRight size={17} />
            </button>

          </form>
          
        </div>
        
      </div>
      <div className="contact-note">
  <ShieldCheck />
  <span>
    Prices are confirmed in writing before work starts.
  </span>
</div>

<GoogleReviewButton />
      
    </PageIntro>
  );
}



function Footer() { return <footer className="site-footer"><div className="container footer-grid"><div><Link to="/" className="brand footer-brand"><span className="brand-mark">JK</span><span className="brand-copy"><strong>JK Ply Hardware</strong><small>FURNITURE WORKSHOP</small></span></Link><p>Furniture and plywood workshop in Patna, Bihar.</p></div><div><h4>Explore</h4><Link to="/collection">Collection</Link><Link to="/services">Services</Link><Link to="/gallery">Gallery</Link><Link to="/workshop">Workshop</Link><Link to="/privacy-policy">Privacy policy</Link><Link to="/terms">Terms</Link></div><div><h4>Contact</h4><a href="tel:+919661382988">+91 96613 82988</a><span>Patna, Bihar</span><Link to="/contact">Get a quote</Link></div><div><h4>Our promise</h4><p>Inspect materials before you buy. Prices confirmed in writing before work starts.</p></div></div><div className="container footer-bottom"><span>© {new Date().getFullYear()} JK Ply Hardware & Furniture Workshop</span><span>Made for homes in Patna, Bihar</span></div></footer>; }

export default function App() {
  const [theme, toggleTheme] = useTheme();
  useEffect(() => { document.title = "JK Ply Hardware | Furniture Workshop"; }, []);
  return <div className="app-shell"><Navbar theme={theme} onToggleTheme={toggleTheme} /><Routes><Route path="/" element={<HomePage />} /><Route path="/collection" element={<CollectionPage />} /><Route path="/product/:slug" element={<ProductPage />} /><Route path="/services" element={<SimplePage type="services" />} /><Route path="/gallery" element={<SimplePage type="gallery" />} /><Route path="/workshop" element={<SimplePage type="workshop" />} /><Route path="/privacy-policy" element={<SimplePage type="privacy" />} /><Route path="/terms" element={<SimplePage type="terms" />} /><Route path="/contact" element={<ContactPage />} /><Route path="*" element={<EmptyNotice title="Page not found" text="The page you are looking for does not exist." />} /></Routes><Footer /><ChatWidget /><a className="whatsapp-float" href={`https://wa.me/${import.meta.env.VITE_WHATSAPP_NUMBER || "919661382988"}`} target="_blank" rel="noreferrer" aria-label="Chat on WhatsApp"><MessageCircleIcon /> WhatsApp</a></div>;
}
function MessageCircleIcon() { return <span className="whatsapp-mark">◔</span>; }



