import { ArrowUpRight, Package } from "lucide-react";
import { Link } from "react-router-dom";
export default function ProductCard({ product }) {
  const image = product.image_url;
  return <article className="product-card">
    <Link to={`/product/${product.slug}`} className="product-image" aria-label={`View ${product.name}`}>
      {image ? <img src={image} alt={product.name} loading="lazy" /> : <div className="product-placeholder"><Package size={36} /><span>JK PLY</span></div>}
      {product.featured && <span className="product-tag">Featured</span>}
    </Link>
    <div className="product-info"><p className="product-category">{product.category?.name || "Furniture"}</p><h3>{product.name}</h3><p className="product-desc">{product.description || "Contact the workshop for details and made-to-measure options."}</p><div className="product-bottom"><span>{product.price ? `₹${Number(product.price).toLocaleString("en-IN")}` : "Price on enquiry"}</span><Link to={`/product/${product.slug}`} aria-label={`Enquire about ${product.name}`}><ArrowUpRight size={18} /></Link></div></div>
  </article>;
}
