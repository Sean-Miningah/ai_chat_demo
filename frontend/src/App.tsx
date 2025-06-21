import './App.css';
import { useState } from 'react';

interface Message {
  sender: 'user' | 'assistant';
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { sender: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError('');

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input }),
      });

      const data = await res.json();
      const assistantMessage: Message = {
        sender: 'assistant',
        content: data.answer || "No response",
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setError(`Something went wrong. Please try again. ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="max-w-2xl w-full bg-white p-6 rounded shadow flex flex-col h-[80vh]">
        <h1 className="text-2xl font-bold mb-4 text-center">Chat with Assistant</h1>

        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded max-w-[80%] ${
                msg.sender === 'user'
                  ? 'bg-blue-100 self-end text-right'
                  : 'bg-gray-200 self-start text-left'
              }`}
            >
              <p className="text-sm text-gray-700">{msg.content}</p>
            </div>
          ))}

          {loading && (
            <div className="bg-gray-100 p-3 rounded text-sm text-gray-500 self-start">
              Assistant is typing...
            </div>
          )}
        </div>

        <form onSubmit={sendMessage} className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={2}
            className="flex-1 p-2 border rounded resize-none"
            placeholder="Type your message..."
            required
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            disabled={loading}
          >
            Send
          </button>
        </form>

        {error && (
          <div className="mt-2 text-sm text-red-500 text-center">{error}</div>
        )}
      </div>
    </div>
  );
}

export default App;
