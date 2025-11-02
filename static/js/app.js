// TATA Nexon Manual Assistant - JavaScript functionality

class ChatAssistant {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.messageInput = document.getElementById('messageInput');
        this.chatForm = document.getElementById('chatForm');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.checkHealth();
        this.setupQuickQuestions();
    }
    
    setupEventListeners() {
        // Chat form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Clear chat button
        document.getElementById('clearChatBtn').addEventListener('click', () => {
            this.clearChat();
        });
        
        // Textarea auto-resize and submit handling
        this.messageInput.addEventListener('input', (e) => {
            this.autoResizeTextarea(e.target);
        });
        
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Smooth scroll to bottom when new messages arrive
        this.setupScrollObserver();
    }
    
    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
    
    setupScrollObserver() {
        // Auto-scroll to bottom when new content is added
        this.scrollObserver = new MutationObserver(() => {
            this.scrollToBottomSmooth();
        });
        
        this.scrollObserver.observe(this.chatContainer, {
            childList: true,
            subtree: true
        });
    }
    
    setupQuickQuestions() {
        document.querySelectorAll('.quick-question').forEach(btn => {
            btn.addEventListener('click', () => {
                const question = btn.getAttribute('data-question');
                this.messageInput.value = question;
                this.sendMessage();
            });
        });
    }
    
    async checkHealth() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            if (data.status === 'healthy' && data.assistant_available) {
                this.updateStatus('Ready', 'success');
            } else {
                this.updateStatus('Assistant Unavailable', 'warning');
            }
        } catch (error) {
            this.updateStatus('Offline', 'danger');
        }
    }
    
    updateStatus(text, type) {
        this.statusText.textContent = text;
        
        // Update status dot color
        this.statusDot.className = 'status-dot';
        if (type === 'success') {
            this.statusDot.style.background = '#28a745';
        } else if (type === 'warning') {
            this.statusDot.style.background = '#ffc107';
        } else if (type === 'danger') {
            this.statusDot.style.background = '#dc3545';
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Clear input and hide welcome message
        this.messageInput.value = '';
        this.hideWelcomeMessage();
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Show typing indicator
        const typingId = this.showTypingIndicator();
        
        try {
            const isStreaming = document.getElementById('streamingMode').checked;
            
            if (isStreaming) {
                await this.sendStreamingMessage(message, typingId);
            } else {
                await this.sendRegularMessage(message, typingId);
            }
        } catch (error) {
            this.removeTypingIndicator(typingId);
            this.showError('Failed to send message: ' + error.message);
        }
    }
    
    async sendRegularMessage(message, typingId) {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message, stream: false })
        });
        
        const data = await response.json();
        this.removeTypingIndicator(typingId);
        
        if (data.success) {
            this.addMessage(data.response, 'assistant');
        } else {
            this.showError(data.error || 'Unknown error occurred');
        }
    }
    
    async sendStreamingMessage(message, typingId) {
        const response = await fetch('/chat/stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message, stream: true })
        });
        
        this.removeTypingIndicator(typingId);
        
        const messageId = this.addMessage('', 'assistant');
        const messageElement = document.querySelector(`[data-message-id="${messageId}"] .message-content`);
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.slice(6);
                    if (data.trim()) {
                        try {
                            const parsed = JSON.parse(data);
                            if (parsed.content === '[DONE]') {
                                break;
                            }
                            
                            // Update content with proper HTML formatting
                            const currentContent = messageElement.innerHTML;
                            messageElement.innerHTML = this.formatMessage(currentContent + parsed.content);
                            
                            // Smooth scroll to bottom during streaming
                            this.scrollToBottomSmooth();
                        } catch (e) {
                            console.error('Error parsing streaming data:', e);
                        }
                    }
                }
            }
        }
    }
    
    addMessage(content, sender) {
        const messageId = 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        const timestamp = new Date().toLocaleTimeString();
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message-container mb-4';
        messageDiv.setAttribute('data-message-id', messageId);
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="d-flex justify-content-end align-items-start gap-3">
                    <div class="message-bubble user-message-bubble rounded-4 p-3 shadow-sm" style="max-width: 80%;">
                        <div class="message-content">${this.formatMessage(content)}</div>
                        <div class="message-time text-end mt-2 opacity-75">${timestamp}</div>
                    </div>
                    <div class="avatar-circle user-avatar flex-shrink-0">
                        <i class="fas fa-user"></i>
                    </div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="d-flex justify-content-start align-items-start gap-3">
                    <div class="avatar-circle assistant-avatar flex-shrink-0">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-bubble assistant-message-bubble rounded-4 p-3 shadow-sm" style="max-width: 80%;">
                        <div class="message-content">${this.formatMessage(content)}</div>
                        <div class="message-time mt-2 opacity-75">${timestamp}</div>
                    </div>
                </div>
            `;
        }
        
        this.chatContainer.appendChild(messageDiv);
        
        // Force scroll to bottom after message is rendered
        setTimeout(() => {
            this.scrollToBottomSmooth();
        }, 100);
        
        return messageId;
    }
    
    formatMessage(content) {
        if (!content) return '';
        
        // Convert line breaks to HTML
        content = content.replace(/\n/g, '<br>');
        
        // Simple markdown-like formatting
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        content = content.replace(/`(.*?)`/g, '<code>$1</code>');
        
        return content;
    }
    
    showTypingIndicator() {
        const typingId = 'typing_' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-container';
        typingDiv.setAttribute('data-typing-id', typingId);
        typingDiv.innerHTML = `
            <div class="assistant-message-wrapper">
                <div class="message-avatar-container">
                    <div class="message-avatar assistant-message-avatar">
                        <i class="fas fa-car"></i>
                    </div>
                </div>
                <div class="typing-bubble">
                    <div class="typing-animation">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                    <span class="typing-text">Assistant is typing...</span>
                </div>
            </div>
        `;
        
        this.chatContainer.appendChild(typingDiv);
        this.scrollToBottom();
        
        return typingId;
    }
    
    removeTypingIndicator(typingId) {
        const typingElement = document.querySelector(`[data-typing-id="${typingId}"]`);
        if (typingElement) {
            typingElement.remove();
        }
    }
    
    hideWelcomeMessage() {
        const welcomeSection = document.querySelector('.welcome-section');
        if (welcomeSection) {
            welcomeSection.style.display = 'none';
        }
        
        // Also hide hero section in fullscreen mode
        this.hideHeroSection();
    }
    
    clearChat() {
        this.chatContainer.innerHTML = '';
        this.showHeroSection();
    }
    
    displayWelcomeMessage() {
        this.chatContainer.innerHTML = `
            <div class="welcome-section">
                <div class="welcome-content">
                    <div class="welcome-icon">
                        <i class="fas fa-car"></i>
                    </div>
                    <h2 class="welcome-title">Your TATA Nexon Expert Assistant</h2>
                    <p class="welcome-subtitle">Get comprehensive answers about your TATA Nexon SUV. I'm here to help with everything from technical specifications to maintenance advice, troubleshooting, and more!</p>
                    
                    <div class="features-grid">
                        <div class="feature-card">
                            <i class="fas fa-shield-alt"></i>
                            <h6>🛡️ Safety Features</h6>
                            <p>5-Star NCAP rating, airbags, ABS, ESC and all safety technologies explained in detail</p>
                        </div>
                        <div class="feature-card">
                            <i class="fas fa-tools"></i>
                            <h6>🔧 Maintenance Guide</h6>
                            <p>Complete service schedules, preventive care tips, and cost-effective maintenance advice</p>
                        </div>
                        <div class="feature-card">
                            <i class="fas fa-cog"></i>
                            <h6>⚙️ Engine & Performance</h6>
                            <p>Detailed specifications for both petrol and diesel engines with performance insights</p>
                        </div>
                        <div class="feature-card">
                            <i class="fas fa-mobile-alt"></i>
                            <h6>📱 Features & Tech</h6>
                            <p>Infotainment, connectivity, smart features and how to use them effectively</p>
                        </div>
                        <div class="feature-card">
                            <i class="fas fa-question-circle"></i>
                            <h6>🔍 Troubleshooting</h6>
                            <p>Step-by-step solutions for common issues and when to visit service center</p>
                        </div>
                        <div class="feature-card">
                            <i class="fas fa-balance-scale"></i>
                            <h6>📊 Comparisons</h6>
                            <p>Variant comparisons, feature differences, and value propositions</p>
                        </div>
                    </div>
                    
                    <div class="quick-questions">
                        <h6>💬 Popular Questions - Click to Ask:</h6>
                        <div class="question-chips">
                            <button class="question-chip quick-question" data-question="What makes TATA Nexon's 5-Star safety rating special and what safety features does it include?">
                                <i class="fas fa-shield-alt me-2"></i>5-Star Safety Features
                            </button>
                            <button class="question-chip quick-question" data-question="Give me the complete maintenance schedule for TATA Nexon with service intervals and what's included">
                                <i class="fas fa-calendar-check me-2"></i>Complete Maintenance Schedule
                            </button>
                            <button class="question-chip quick-question" data-question="Compare TATA Nexon petrol vs diesel engine specifications, performance and which one should I choose?">
                                <i class="fas fa-car-battery me-2"></i>Petrol vs Diesel Comparison
                            </button>
                            <button class="question-chip quick-question" data-question="How do I use the infotainment system, connect my phone, and access all the smart features?">
                                <i class="fas fa-mobile-alt me-2"></i>Infotainment & Connectivity
                            </button>
                            <button class="question-chip quick-question" data-question="What is the real-world fuel efficiency of TATA Nexon and tips to improve mileage?">
                                <i class="fas fa-gas-pump me-2"></i>Fuel Efficiency Guide
                            </button>
                            <button class="question-chip quick-question" data-question="Compare all TATA Nexon variants (XE, XM, XT, XZ, XZ+) and help me choose the best one">
                                <i class="fas fa-layer-group me-2"></i>Variant Comparison
                            </button>
                            <button class="question-chip quick-question" data-question="My car has a warning light/unusual sound/performance issue - help me troubleshoot step by step">
                                <i class="fas fa-tools me-2"></i>Troubleshooting Help
                            </button>
                            <button class="question-chip quick-question" data-question="What are all the interior and exterior features of TATA Nexon and how do they work?">
                                <i class="fas fa-list-ul me-2"></i>Complete Features List
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        this.setupQuickQuestions();
    }
    

    
    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }
    
    scrollToBottomSmooth() {
        this.chatContainer.scrollTo({
            top: this.chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }
    
    hideHeroSection() {
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            heroSection.style.display = 'none';
        }
    }
    
    showHeroSection() {
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            heroSection.style.display = 'block';
        }
    }
    
    showSuccess(message) {
        document.getElementById('successMessage').textContent = message;
        const toast = new bootstrap.Toast(document.getElementById('successToast'));
        toast.show();
    }
    
    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        const toast = new bootstrap.Toast(document.getElementById('errorToast'));
        toast.show();
    }
}

// Initialize the chat application when the page loads
let chatApp;
document.addEventListener('DOMContentLoaded', () => {
    chatApp = new ChatAssistant();
});

