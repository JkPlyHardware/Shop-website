import { useEffect, useRef, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { Menu, X, Phone, Sun, Moon, Search, ArrowUpRight } from "lucide-react";

const links = [
  ["Home", "/"], ["Collection", "/collection"], ["Services", "/services"],
  ["Gallery", "/gallery"], ["Workshop", "/workshop"], ["Contact", "/contact"],
];

export default function Navbar({ theme, onToggleTheme }) {
  const [open, setOpen] = useState(false);
  const panelRef = useRef(null);
  const triggerRef = useRef(null);
  const location = useLocation();

  useEffect(() => { setOpen(false); }, [location.pathname]);

  useEffect(() => {
    if (!open) return undefined;
    const oldOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKey = (event) => {
      if (event.key === "Escape") { setOpen(false); triggerRef.current?.focus(); }
      if (event.key === "Tab" && panelRef.current) {
        const nodes = panelRef.current.querySelectorAll('a[href], button:not([disabled])');
        if (!nodes.length) return;
        const first = nodes[0], last = nodes[nodes.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    };
    const onPointer = (event) => {
      if (!panelRef.current?.contains(event.target) && !triggerRef.current?.contains(event.target)) setOpen(false);
    };
    document.addEventListener("keydown", onKey);
    document.addEventListener("pointerdown", onPointer);
    requestAnimationFrame(() => panelRef.current?.querySelector("a")?.focus());
    return () => { document.body.style.overflow = oldOverflow; document.removeEventListener("keydown", onKey); document.removeEventListener("pointerdown", onPointer); };
  }, [open]);

  useEffect(() => {
    const media = window.matchMedia("(min-width: 769px)");
    const close = (event) => { if (event.matches) setOpen(false); };
    media.addEventListener?.("change", close);
    return () => media.removeEventListener?.("change", close);
  }, []);

  return <>
    <header className="site-header">
      <div className="nav-inner container">
        <Link to="/" className="brand" aria-label="JK Ply Hardware home">
          <span className="brand-mark">JK</span>
          <span className="brand-copy"><strong>JK Ply Hardware</strong><small>FURNITURE WORKSHOP</small></span>
        </Link>
        <nav className="desktop-links" aria-label="Main navigation">
          {links.map(([label, href]) => <NavLink key={href} to={href} end={href === "/"}>{label}</NavLink>)}
        </nav>
        <div className="nav-actions">
          <a className="nav-phone" href="tel:+919661382988"><Phone size={16} /> <span>+91 96613 82988</span></a>
          <button className="icon-button desktop-icon" onClick={() => window.dispatchEvent(new Event("jk:focus-search"))} aria-label="Search products"><Search size={18} /></button>
          <button className="icon-button theme-button" onClick={onToggleTheme} aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}>{theme === "light" ? <Moon size={18} /> : <Sun size={18} />}</button>
          <Link to="/contact" className="button button-small nav-quote">Get a quote</Link>
          <button ref={triggerRef} className={`menu-toggle ${open ? "is-open" : ""}`} type="button" aria-label={open ? "Close navigation menu" : "Open navigation menu"} aria-expanded={open} aria-controls="mobile-menu" onClick={() => setOpen((v) => !v)}>
            <Menu className="menu-icon" size={23} /><X className="close-icon" size={23} />
          </button>
        </div>
      </div>
    </header>
    <div className={`mobile-scrim ${open ? "visible" : ""}`} aria-hidden="true" />
    <nav id="mobile-menu" ref={panelRef} className={`mobile-menu ${open ? "is-open" : ""}`} aria-label="Mobile navigation" aria-hidden={!open} inert={!open}>
      <p className="menu-eyebrow">EXPLORE JK PLY</p>
      <div className="mobile-menu-links">
        {links.map(([label, href], index) => <NavLink key={href} to={href} end={href === "/"} style={{ "--menu-index": index }} onClick={() => setOpen(false)} tabIndex={open ? 0 : -1}><span>{label}</span><ArrowUpRight size={17} /></NavLink>)}
      </div>
      <div className="mobile-menu-footer">
        <a href="tel:+919661382988"><Phone size={16} /> +91 96613 82988</a>
        <Link to="/contact" className="button" onClick={() => setOpen(false)}>Get a quote <ArrowUpRight size={17} /></Link>
      </div>
      <p className="menu-location">FURNITURE & PLYWOOD WORKSHOP · PATNA, BIHAR</p>
    </nav>
  </>;
}
