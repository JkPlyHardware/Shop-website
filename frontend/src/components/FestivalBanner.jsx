import { useEffect, useState } from "react";
import { ArrowLeft, ArrowRight, Sparkles } from "lucide-react";
import { api } from "../services/api";

export default function FestivalBanner() {
  const [items, setItems] = useState([]);
  const [index, setIndex] = useState(0);
  useEffect(() => { api.campaigns().then(setItems).catch(() => setItems([])); }, []);
  useEffect(() => {
    if (items[index]) api.campaignEvent(items[index].id, "impression").catch(() => {});
  }, [items, index]);
  useEffect(() => {
    if (items.length < 2) return undefined;
    const timer = window.setInterval(() => setIndex((i) => (i + 1) % items.length), 6500);
    return () => window.clearInterval(timer);
  }, [items.length]);
  if (!items.length) return null;
  const current = items[index];
  const track = (event_type) => api.campaignEvent(current.id, event_type).catch(() => {});
  const next = () => { setIndex((i) => (i + 1) % items.length); track("click"); };
  const prev = () => { setIndex((i) => (i - 1 + items.length) % items.length); track("click"); };
  return <section className="festival-wrap container" aria-label="Current promotions">
    <div className="festival-banner">
      <picture className="festival-picture">{current.mobile_image_url && <source media="(max-width: 768px)" srcSet={current.mobile_image_url} />}<img src={current.desktop_image_url} alt="" loading={index === 0 ? "eager" : "lazy"} /></picture><div className="festival-overlay" />
      <div className="festival-copy"><span className="eyebrow light"><Sparkles size={14} /> {current.title}</span><h2>{current.heading}</h2>{current.description && <p>{current.description}</p>}{current.offer_text && <strong className="festival-offer">{current.offer_text}</strong>}{current.button_text && <a className="button festival-cta" href={current.button_url} onClick={() => track("cta")}>{current.button_text} <ArrowRight size={17} /></a>}</div>
      {items.length > 1 && <div className="festival-controls"><button onClick={prev} aria-label="Previous banner"><ArrowLeft size={17} /></button><div className="festival-dots">{items.map((item, i) => <button key={item.id} className={i === index ? "active" : ""} onClick={() => setIndex(i)} aria-label={`Show banner ${i + 1}`} />)}</div><button onClick={next} aria-label="Next banner"><ArrowRight size={17} /></button></div>}
    </div>
  </section>;
}
