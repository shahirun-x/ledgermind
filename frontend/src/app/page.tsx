"use client";

import { useState } from "react";

type Message = {
  role: "user" | "bot";
  content: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

  async function sendMessage() {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      if (!API_BASE_URL) {
        throw new Error("API base URL not configured");
      }

      const res = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage.content }),
      });

      if (!res.ok) {
        throw new Error("Backend error");
      }

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { role: "bot", content: data.answer },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "Sorry can not find the answer" },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 flex justify-center">
      <div className="w-full max-w-4xl flex flex-col border-x border-neutral-800">

        {/* Header */}
        <header className="h-14 flex items-center px-6 border-b border-neutral-800 bg-neutral-950">
          <h1 className="text-lg font-semibold tracking-tight">
            LedgerMind
          </h1>
          <span className="ml-3 text-sm text-neutral-500">
            Financial intelligence grounded in your data
          </span>
        </header>

        {/* Chat area */}
        <main className="flex-1 px-6 py-6 space-y-6 overflow-y-auto bg-neutral-950">
          {messages.length === 0 && (
            <div className="text-neutral-500 text-sm">
              Ask questions about trades, holdings, or fund performance.
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-xl px-4 py-3 rounded-lg text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-neutral-800 text-neutral-100"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-neutral-800 px-4 py-3 rounded-lg text-sm text-neutral-400">
                LedgerMind is thinking…
              </div>
            </div>
          )}
        </main>

        {/* Input */}
        <footer className="px-6 py-4 border-t border-neutral-800 bg-neutral-950">
          <div className="flex gap-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Ask a question…"
              className="flex-1 bg-neutral-900 border border-neutral-700 rounded-md px-4 py-2 text-sm outline-none focus:border-neutral-500"
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              className="px-4 py-2 rounded-md bg-blue-600 text-sm font-medium hover:bg-blue-500 disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </footer>

      </div>
    </div>
  );
}
