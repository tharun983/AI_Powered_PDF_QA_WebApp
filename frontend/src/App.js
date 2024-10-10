import React, { useState } from 'react';
import './App.css';
import './normal.css';

function App() {
  const [query, setQuery] = useState('');
  const [useVectorDB, setUseVectorDB] = useState(false);
  const [chatLog, setChatLog] = useState([]);
  const [people, setPeople] = useState([]);
  const [username, setUsername] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [commentText, setCommentText] = useState({});
  const [comments, setComments] = useState({});
  const [showComments, setShowComments] = useState({}); // Track visibility of comments

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query) return;

    const response = await fetch('http://localhost:8000/agent/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, use_vectordb: useVectorDB }),
    });

    const data = await response.json();

    setChatLog((prevLog) => [
      ...prevLog,
      { source: useVectorDB ? 'VectorDB' : 'Cohere', text: query, type: 'user', id: prevLog.length },
      { source: useVectorDB ? 'VectorDB' : 'Cohere', text: data.answer, type: 'response', id: prevLog.length + 1 },
    ]);
    setQuery('');
  };

  const handleAddPeople = () => {
    if (username.trim()) {
      setPeople([...people, username]);
      setUsername('');
      setIsModalOpen(false);
    }
  };

  const handleCommentChange = (id, value) => {
    setCommentText({ ...commentText, [id]: value });
  };

  const handleCommentSubmit = (id) => {
    if (!commentText[id]) return;

    setComments({
      ...comments,
      [id]: [...(comments[id] || []), commentText[id]],
    });
    setCommentText({ ...commentText, [id]: '' });
  };

  const toggleCommentSection = (id) => {
    setShowComments((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const handleModalOutsideClick = (e) => {
    if (e.target.className === 'modal') {
      setIsModalOpen(false);
    }
  };

  return (
    <div className="App">
      <aside className="sidemenu">
        <div className="sidemenubutton" onClick={() => setIsModalOpen(true)}>
          <span>+</span>
          Add people
        </div>
        <div className="people-list">
          {people.map((person, index) => (
            <div key={index} className="person-item">{person}</div>
          ))}
        </div>
      </aside>

      <section className="chatbox">
        <div className="checkbox-holder">
          <label htmlFor="filter" className="switch" aria-label="Toggle VectorDB/Agent">
            <input
              type="checkbox"
              id="filter"
              checked={useVectorDB}
              onChange={(e) => setUseVectorDB(e.target.checked)}
            />
            <span>Use VectorDB</span>
            <span>Use Agent</span>
          </label>
        </div>

        <div className="chat-log">
          {chatLog.map((message, index) => (
            <div key={index}>
              <div className="chat-message">
                <div className="avatar"></div>
                <div className="message-content">
                  {message.type === 'user' ? (
                    <strong>{message.text}</strong>
                  ) : (
                    message.text
                  )}
                </div>
              </div>
              {message.type === 'response' && (
                <>
                  <span
                    className="comment-toggle-icon"
                    onClick={() => toggleCommentSection(message.id)}
                  >
                    {showComments[message.id] ? '🔽' : '💬'} {/* Comment toggle icon */}
                  </span>
                  {showComments[message.id] && (
                    <div className="comment-section">
                      {comments[message.id] && comments[message.id].map((comment, idx) => (
                        <div key={idx} className="comment">
                          <p>{comment}</p>
                        </div>
                      ))}
                      <div className="comment-input">
                        <input
                          type="text"
                          value={commentText[message.id] || ''}
                          onChange={(e) => handleCommentChange(message.id, e.target.value)}
                          placeholder="Add a comment..."
                        />
                        <button onClick={() => handleCommentSubmit(message.id)}>Comment</button>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          ))}
        </div>

        <div className="chat-input-holder">
          <form onSubmit={handleSubmit} className="chat-form">
            <input
              className="chat-input-textarea"
              type="text"
              placeholder="Type input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button type="submit" className="send-button">Send</button>
          </form>
        </div>
      </section>

      {isModalOpen && (
        <div className="modal" onClick={handleModalOutsideClick}>
          <div className="modal-content">
            <h2>Add People</h2>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
            />
            <button onClick={handleAddPeople}>Add</button>
            <button onClick={() => setIsModalOpen(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
