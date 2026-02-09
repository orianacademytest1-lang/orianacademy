/**
 * Oriana Academy AI Chatbot - Powered by RAG with Vector Search
 */

// RAG Backend API URL
const RAG_API_URL = '/api/chat';
const RAG_STREAM_URL = '/api/chat/stream';

class OrianaChatbot {
    constructor() {
        this.isOpen = false;
        this.isRootPage = !window.location.pathname.includes('/courses/');
        // Small delay to ensure body is ready
        setTimeout(() => this.init(), 100);
    }

    init() {
        this.createChatWidget();
        this.attachEventListeners();
        this.addWelcomeMessage();
    }

    getAssetPath(asset) {
        const path = this.isRootPage ? asset : `../${asset}`;
        return `${path}?v=${Date.now()}`; // Cache busting
    }

    createChatWidget() {
        const avatarPath = this.getAssetPath('assets/images/chatbot-avatar.png');

        const chatHTML = `
            <!-- Chatbot Toggle Button -->
            <div id="oriana-chat-toggle" class="chat-toggle" aria-label="Open chat">
                <img src="${avatarPath}" alt="Oriana AI" class="chat-toggle-image">
            </div>

            <!-- Chatbot Window -->
            <div id="oriana-chat-window" class="chat-window">
                <div class="chat-header">
                    <div class="chat-header-info">
                        <div class="chat-avatar">
                            <img src="${avatarPath}" alt="Oriana AI" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
                        </div>
                        <div>
                            <div class="chat-title">Oriana AI Assistant</div>
                            <div class="chat-status">Online • Ask me anything!</div>
                        </div>
                    </div>
                    <button id="oriana-chat-close" class="chat-close" aria-label="Close chat">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
                <div id="oriana-chat-messages" class="chat-messages"></div>
                <div class="chat-input-container">
                    <input 
                        type="text" 
                        id="oriana-chat-input" 
                        class="chat-input" 
                        placeholder="Ask about courses, placements..." 
                        autocomplete="off"
                    />
                    <button id="oriana-chat-send" class="chat-send" aria-label="Send message">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                        </svg>
                    </button>
                </div>
                <div class="chat-suggestions">
                    <button class="suggestion-chip">Tell me about courses</button>
                    <button class="suggestion-chip">What's Data Science?</button>
                    <button class="suggestion-chip">Placement support?</button>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatHTML);
    }

    attachEventListeners() {
        const toggle = document.getElementById('oriana-chat-toggle');
        const close = document.getElementById('oriana-chat-close');
        const send = document.getElementById('oriana-chat-send');
        const input = document.getElementById('oriana-chat-input');
        const suggestions = document.querySelectorAll('.suggestion-chip');

        toggle.addEventListener('click', () => this.toggleChat());
        close.addEventListener('click', () => this.toggleChat());
        send.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        suggestions.forEach(chip => {
            chip.addEventListener('click', (e) => {
                input.value = e.target.textContent;
                this.sendMessage();
            });
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('oriana-chat-window');
        const toggle = document.getElementById('oriana-chat-toggle');

        if (this.isOpen) {
            chatWindow.classList.add('open');
            toggle.classList.add('hidden');
            document.getElementById('oriana-chat-input').focus();
        } else {
            chatWindow.classList.remove('open');
            toggle.classList.remove('hidden');
        }
    }

    addWelcomeMessage() {
        const welcomeMsg = "👋 Hi! I'm Oriana, your AI assistant powered by semantic search. I can help you learn about our courses, placements, and more. What would you like to know?";
        this.addMessage(welcomeMsg, 'bot');
    }

    addMessage(text, sender = 'user') {
        const messagesContainer = document.getElementById('oriana-chat-messages');
        const messageDiv = document.createElement('div');
        const avatarPath = this.getAssetPath('assets/images/chatbot-avatar.png');
        messageDiv.className = `chat-message ${sender}-message`;

        if (sender === 'bot') {
            messageDiv.innerHTML = `
                <div class="message-avatar">
                    <img src="${avatarPath}" alt="Oriana AI" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
                </div>
                <div class="message-bubble">${this.formatMessage(text)}</div>
            `;
        } else {
            messageDiv.innerHTML = `<div class="message-bubble">${this.escapeHtml(text)}</div>`;
        }

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    formatMessage(text) {
        // Convert markdown-style formatting to HTML
        return this.escapeHtml(text)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
    }

    updateLastMessage(text, isChunk = false, isDone = false) {
        const messagesContainer = document.getElementById('oriana-chat-messages');
        const lastMessage = messagesContainer.lastElementChild;
        if (lastMessage && lastMessage.classList.contains('bot-message')) {
            const bubble = lastMessage.querySelector('.message-bubble');

            if (isChunk) {
                // For chunks, we store raw text and re-format
                if (!lastMessage.dataset.rawText) lastMessage.dataset.rawText = '';
                lastMessage.dataset.rawText += text;

                // Add a streaming cursor if not already there, and it's not done
                let content = this.formatMessage(lastMessage.dataset.rawText);
                if (!isDone) {
                    content += '<span class="streaming-cursor"></span>';
                }
                bubble.innerHTML = content;
            } else {
                bubble.innerHTML = this.formatMessage(text);
            }
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    addTypingIndicator() {
        const messagesContainer = document.getElementById('oriana-chat-messages');
        const typingDiv = document.createElement('div');
        const avatarPath = this.getAssetPath('assets/images/chatbot-avatar.png');
        typingDiv.className = 'chat-message bot-message typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <img src="${avatarPath}" alt="Oriana AI" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
            </div>
            <div class="message-bubble">
                <span></span><span></span><span></span>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    async sendMessage() {
        const input = document.getElementById('oriana-chat-input');
        const message = input.value.trim();

        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        this.addTypingIndicator();

        // Get AI response from RAG backend using STREAMING
        try {
            await this.getStreamingRAGResponse(message);
        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage("I'm sorry, I'm having trouble connecting right now. Please try again or contact us at info@orianaacademy.com", 'bot');
            console.error('Chatbot error:', error);
        }
    }

    async getStreamingRAGResponse(userMessage) {
        try {
            console.log('🔄 Calling Streaming RAG API:', RAG_STREAM_URL);

            const response = await fetch(RAG_STREAM_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: userMessage
                })
            });

            if (!response.ok) {
                this.removeTypingIndicator();
                this.addMessage("⚠️ I'm currently unable to connect to the knowledge base.", 'bot');
                return;
            }

            this.removeTypingIndicator();
            // Start a new bot message for the stream
            this.addMessage("", 'bot');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                buffer += chunk;

                // Process SSE protocol (data: {json}\n\n)
                const lines = buffer.split('\n');
                buffer = lines.pop(); // Keep the last partial line in buffer

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.slice(6).trim();
                        if (dataStr === '[DONE]') {
                            this.updateLastMessage('', true, true);
                            continue;
                        }

                        try {
                            const data = JSON.parse(dataStr);
                            if (data.text) {
                                this.updateLastMessage(data.text, true, false);
                            } else if (data.error) {
                                this.updateLastMessage(`\n\nError: ${data.error}`, true, true);
                            }
                        } catch (e) {
                            console.warn('Failed to parse chunk:', dataStr);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Streaming API error:', error);
            throw error;
        }
    }

    async getRAGResponse(userMessage) {
        /**
         * NEW: RAG-powered response using vector search backend
         * Replaces static context with semantic search
         */
        try {
            console.log('🔄 Calling RAG API:', RAG_API_URL);
            const response = await fetch(RAG_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: userMessage
                })
            });

            console.log('📡 Response status:', response.status, response.ok);

            if (!response.ok) {
                // Backend not running - provide helpful error
                console.warn('RAG backend not available');
                return "⚠️ I'm currently unable to connect to the knowledge base.\n\n" +
                    "Please make sure the backend server is running:\n" +
                    "1. Open terminal in backend folder\n" +
                    "2. Run: python app_local.py\n\n" +
                    "Or contact us at info@orianaacademy.com or +91 98765 43210";
            }

            const data = await response.json();

            // Return the RAG-generated answer
            return data.answer;

        } catch (error) {
            console.error('RAG API error:', error);
            throw error;
        }
    }
}

// Initialize chatbot when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new OrianaChatbot());
} else {
    new OrianaChatbot();
}
