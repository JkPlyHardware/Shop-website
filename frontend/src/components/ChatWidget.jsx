import { useState } from "react";
import { MessageCircle, Send, X, Bot, LoaderCircle } from "lucide-react";
import { api } from "../services/api";
export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [messages, setMessages] = useState([{ role: "assistant", content: "Namaste! Welcome to JK Ply. Ask about our furniture, plywood, laminates or how to request a quote." }]);
  const send = async (event) => {
    event.preventDefault();
    const text = input.trim();
    if (!text || busy) return;
    if (text.length > 500) return;
    const history = messages.slice(-6).map(({ role, content }) => ({ role, content }));
    setMessages((old) => [...old, { role: "user", content: text }]); setInput(""); setBusy(true);
    try { const data = await api.chat({ message: text, history }); setMessages((old) => [...old, { role: "assistant", content: data.reply }]); }
    catch (error) { setMessages((old) => [...old, { role: "assistant", content: error.message || "Chat is unavailable. Please call +91 96613 82988." }]); }
    finally { setBusy(false); }
  };
  return <div className="chat-widget">
    {open && <section className="chat-panel" aria-label="JK Ply chat assistant">
      <header><span className="chat-avatar"><Bot size={18} /></span><div><strong>JK Ply Assistant</strong><small>FAQ support · Patna, Bihar</small></div><button onClick={() => setOpen(false)} aria-label="Close chat"><X size={18} /></button></header>
      <div className="chat-messages" aria-live="polite">{messages.map((m, i) => <div key={`${i}-${m.role}`} className={`chat-message ${m.role}`}>{m.content}</div>)}{busy && <div className="chat-message assistant"><LoaderCircle className="spin" size={16} /> Thinking...</div>}</div>
      <form onSubmit={send} className="chat-form"><input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask us something..." maxLength={500} aria-label="Your message" /><button disabled={busy || !input.trim()} aria-label="Send message"><Send size={17} /></button></form>
    </section>}
    <button className="chat-launch" onClick={() => setOpen((v) => !v)} aria-label={open ? "Close chat" : "Open chat"}>{open ? <X size={23} /> : <MessageCircle size={23} />}</button>
  </div>;
}
