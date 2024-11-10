import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-hot-toast';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [ws, setWs] = useState(null);
  const messagesEndRef = useRef(null);
  const { token } = useAuth();

  useEffect(() => {
    const websocket = new WebSocket(`ws://localhost:8000/chat/ws?token=${token}`);

    websocket.onopen = () => {
      console.log('Connected to chat');
    };

    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, message]);
    };

    websocket.onerror = (error) => {
      toast.error('Chat connection error');
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, [token]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    ws.send(JSON.stringify({ content: newMessage }));
    setNewMessage('');
  };

  return (
    <div className="max-w-4xl mx-auto h-[80vh] flex flex-col">
      <div className="flex-1 overflow-y-auto bg-white p-4 rounded-t-lg shadow">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`my-2 p-3 rounded-lg ${
              message.is_bot
                ? 'bg-gray-100 mr-auto'
                : 'bg-blue-100 ml-auto'
            } max-w-[80%]`}
          >
            <p>{message.content}</p>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSubmit} className="bg-white p-4 rounded-b-lg shadow">
        <div className="flex gap-2">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chat;
