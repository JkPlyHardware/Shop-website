import { ExternalLink, MessageSquareText } from "lucide-react";
import "./GoogleReviewButton.css";

const GOOGLE_REVIEW_URL = "https://g.page/r/CS9E2cV0KIszEBM/review";

export default function GoogleReviewButton({ className = "" }) {
  return (
    <a
      className={`google-review-button ${className}`.trim()}
      href={GOOGLE_REVIEW_URL}
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Share your experience about JK Ply Hardware and Furniture Workshop on Google"
    >
      <MessageSquareText size={18} aria-hidden="true" />
      <span>Share your experience on Google</span>
      <ExternalLink size={16} aria-hidden="true" />
    </a>
  );
}
