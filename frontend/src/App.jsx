import { useState, useRef, useEffect } from "react"

export default function App() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hey! 👋 I'm your Workshop Carnival 2.0 assistant. Ask me anything!" }
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, open])

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    const userMessage = input.trim()
    setInput("")
    setMessages(prev => [...prev, { role: "user", text: userMessage }])
    setLoading(true)
    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage })
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: "bot", text: data.answer }])
    } catch {
      setMessages(prev => [...prev, { role: "bot", text: "Couldn't connect to server. Please try again!" }])
    }
    setLoading(false)
  }

  const handleKey = (e) => {
    if (e.key === "Enter") sendMessage()
  }

  const suggestions = ["📅 Event dates?", "🎯 What domains?", "💰 Fee?", "📞 Contact?"]

  const domains = [
    { label: "🎨 UI/UX Design", bg: "#ec4899", color: "#fff" },
    { label: "💻 WebDev", bg: "#f97316", color: "#fff" },
    { label: "🤖 Agentic AI", bg: "#06b6d4", color: "#fff" },
    { label: "📊 Data Analysis", bg: "#eab308", color: "#000" },
    { label: "🔐 Ethical Hacking", bg: "#22c55e", color: "#fff" },
    { label: "📱 App Dev", bg: "#a855f7", color: "#fff" }
  ]

  return (
    <div style={s.page}>
      {/* Background Page */}
      <div style={s.hero}>
        {/* Decorative circles */}
        <div style={s.circle1} />
        <div style={s.circle2} />
        <div style={s.circle3} />

        <div style={s.heroBadge}>✨ MLRIT-CIE Presents</div>
        <div style={s.heroTitle}>WORKSHOP</div>
        <div style={s.heroTitle2}>CARNIVAL 2.0</div>
        <div style={s.heroTagline}>Think. Design. Build.</div>
        <div style={s.heroDate}>🗓️ 10th - 11th April 2026 &nbsp;|&nbsp; 📍 MLRIT, Hyderabad</div>

        <div style={s.domainsWrap}>
          {domains.map((d, i) => (
            <div key={i} style={{ ...s.domainChip, backgroundColor: d.bg, color: d.color }}>
              {d.label}
            </div>
          ))}
        </div>
      </div>

      {/* Chat Widget */}
      {open && (
        <div style={s.chatWidget}>
          {/* Header */}
          <div style={s.chatHeader}>
            <div style={s.chatHeaderLeft}>
              <div style={s.chatAvatar}>🤖</div>
              <div>
                <div style={s.chatName}>CIE Assistant</div>
                <div style={s.chatStatus}>
                  <span style={s.greenDot} /> Online
                </div>
              </div>
            </div>
            <button style={s.closeBtn} onClick={() => setOpen(false)}>✕</button>
          </div>

          {/* Messages */}
          <div style={s.messages}>
            {messages.map((msg, i) => (
              <div key={i} style={{ display: "flex", justifyContent: msg.role === "user" ? "flex-end" : "flex-start", marginBottom: 10, alignItems: "flex-end", gap: 6 }}>
                {msg.role === "bot" && <div style={s.botIcon}>🤖</div>}
                <div style={msg.role === "user" ? s.userBubble : s.botBubble}>
                  {msg.text}
                </div>
              </div>
            ))}

            {loading && (
              <div style={{ display: "flex", marginBottom: 10, alignItems: "flex-end", gap: 6 }}>
                <div style={s.botIcon}>🤖</div>
                <div style={s.botBubble}>
                  <div style={s.typingDots}>
                    <span style={{ ...s.dot, animationDelay: "0s" }} />
                    <span style={{ ...s.dot, animationDelay: "0.2s" }} />
                    <span style={{ ...s.dot, animationDelay: "0.4s" }} />
                  </div>
                </div>
              </div>
            )}

            {messages.length === 1 && (
              <div style={s.suggestions}>
                {suggestions.map((sg, i) => (
                  <button key={i} style={s.suggBtn} onClick={() => setInput(sg)}>
                    {sg}
                  </button>
                ))}
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div style={s.inputRow}>
            <input
              style={s.input}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Ask me anything..."
            />
            <button style={s.sendBtn} onClick={sendMessage} disabled={loading}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M22 2L11 13" stroke="white" strokeWidth="2.5" strokeLinecap="round" />
                <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button style={s.fab} onClick={() => setOpen(!open)}>
        <span style={{ fontSize: 28 }}>{open ? "✕" : "🤖"}</span>
        {!open && <div style={s.fabLabel}>Ask me!</div>}
      </button>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Righteous&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { overflow: hidden; }
        ::-webkit-scrollbar { width: 3px; }
        ::-webkit-scrollbar-thumb { background: #a855f7; border-radius: 2px; }
        @keyframes bounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-5px); }
        }
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); box-shadow: 0 8px 25px #6d28d966; }
          50% { transform: scale(1.08); box-shadow: 0 8px 35px #6d28d999; }
        }
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
        }
      `}</style>
    </div>
  )
}

const s = {
  page: { height: "100vh", width: "100vw", fontFamily: "'Inter', sans-serif", position: "relative", overflow: "hidden" },

  // Hero background
  hero: { height: "100vh", background: "linear-gradient(160deg, #7B2FBE 0%, #9B59E8 30%, #7C3AED 60%, #5B21B6 100%)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 14, position: "relative", overflow: "hidden" },
  circle1: { position: "absolute", width: 400, height: 400, borderRadius: "50%", background: "#ffffff08", top: -100, left: -100 },
  circle2: { position: "absolute", width: 300, height: 300, borderRadius: "50%", background: "#ffffff06", bottom: -80, right: -80 },
  circle3: { position: "absolute", width: 200, height: 200, borderRadius: "50%", background: "#2dd4bf15", top: "40%", right: "10%" },

  heroBadge: { backgroundColor: "#ffffff20", color: "#e9d5ff", fontSize: 13, fontWeight: 600, padding: "6px 18px", borderRadius: 20, border: "1px solid #ffffff30", letterSpacing: 1, backdropFilter: "blur(10px)" },
  heroTitle: { fontFamily: "'Righteous', cursive", fontSize: 80, fontWeight: 700, color: "#ffffff", lineHeight: 1, textShadow: "3px 3px 0px #4C1D95, 0 0 40px #a855f788", letterSpacing: 2 },
  heroTitle2: { fontFamily: "'Righteous', cursive", fontSize: 80, fontWeight: 700, color: "#2DD4BF", lineHeight: 1, textShadow: "3px 3px 0px #0f766e, 0 0 40px #2dd4bf88", marginTop: -10, letterSpacing: 2 },
  heroTagline: { color: "#fde68a", fontSize: 18, fontWeight: 600, fontStyle: "italic", letterSpacing: 1 },
  heroDate: { color: "#ddd6fe", fontSize: 15, fontWeight: 500, backgroundColor: "#ffffff15", padding: "8px 20px", borderRadius: 20, backdropFilter: "blur(10px)" },
  domainsWrap: { display: "flex", flexWrap: "wrap", gap: 10, justifyContent: "center", marginTop: 10, maxWidth: 620, padding: "0 20px" },
  domainChip: { fontSize: 13, fontWeight: 700, padding: "7px 16px", borderRadius: 20, boxShadow: "0 4px 12px #0004" },

  // Chat widget
  chatWidget: { position: "fixed", bottom: 90, right: 24, width: 365, height: 530, backgroundColor: "#0f0f0f", borderRadius: 20, boxShadow: "0 20px 60px #0009, 0 0 0 1px #ffffff11", display: "flex", flexDirection: "column", overflow: "hidden", animation: "fadeUp 0.3s ease", zIndex: 999 },
  chatHeader: { background: "linear-gradient(135deg, #7B2FBE, #5B21B6)", padding: "14px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" },
  chatHeaderLeft: { display: "flex", alignItems: "center", gap: 10 },
  chatAvatar: { width: 40, height: 40, backgroundColor: "#ffffff22", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 22, border: "2px solid #a855f7" },
  chatName: { color: "#fff", fontWeight: 700, fontSize: 15 },
  chatStatus: { display: "flex", alignItems: "center", gap: 5, color: "#c4b5fd", fontSize: 12 },
  greenDot: { width: 7, height: 7, backgroundColor: "#22c55e", borderRadius: "50%", display: "inline-block", boxShadow: "0 0 6px #22c55e" },
  closeBtn: { background: "#ffffff22", border: "none", color: "#fff", width: 30, height: 30, borderRadius: "50%", cursor: "pointer", fontSize: 14, display: "flex", alignItems: "center", justifyContent: "center" },

  messages: { flex: 1, overflowY: "auto", padding: "14px 12px" },
  botIcon: { width: 28, height: 28, backgroundColor: "#1e1e1e", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, flexShrink: 0, border: "1px solid #333" },
  botBubble: { backgroundColor: "#1a1a1a", border: "1px solid #2a2a2a", borderRadius: "4px 16px 16px 16px", padding: "10px 14px", maxWidth: "78%", fontSize: 13, lineHeight: 1.6, color: "#e5e5e5" },
  userBubble: { background: "linear-gradient(135deg, #7B2FBE, #9B59E8)", borderRadius: "16px 4px 16px 16px", padding: "10px 14px", maxWidth: "78%", fontSize: 13, lineHeight: 1.6, color: "#fff", boxShadow: "0 4px 12px #7B2FBE44" },
  typingDots: { display: "flex", gap: 4, alignItems: "center", height: 18 },
  dot: { width: 6, height: 6, backgroundColor: "#a855f7", borderRadius: "50%", display: "inline-block", animation: "bounce 1s infinite" },

  suggestions: { display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8 },
  suggBtn: { backgroundColor: "#1e1e1e", border: "1px solid #7c3aed55", color: "#c4b5fd", padding: "6px 12px", borderRadius: 16, fontSize: 12, cursor: "pointer" },

  inputRow: { display: "flex", gap: 8, padding: "10px 12px 14px", borderTop: "1px solid #1e1e1e", alignItems: "center" },
  input: { flex: 1, backgroundColor: "#1a1a1a", border: "1px solid #2a2a2a", borderRadius: 20, padding: "9px 14px", color: "#fff", fontSize: 13, outline: "none" },
  sendBtn: { width: 38, height: 38, borderRadius: "50%", border: "none", background: "linear-gradient(135deg, #7B2FBE, #9B59E8)", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, boxShadow: "0 4px 12px #7B2FBE55" },

  // FAB
  fab: { position: "fixed", bottom: 24, right: 24, width: 65, height: 65, borderRadius: "50%", border: "none", background: "linear-gradient(135deg, #7B2FBE, #2DD4BF)", cursor: "pointer", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", boxShadow: "0 8px 25px #6d28d966", animation: "pulse 2s infinite", zIndex: 1000 },
  fabLabel: { fontSize: 9, color: "#fff", fontWeight: 700, marginTop: 1, letterSpacing: 0.5 }
}