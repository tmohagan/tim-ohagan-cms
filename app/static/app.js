// app.js - Frontend Logic for Tim O'Hagan CMS

const terminal = document.getElementById('terminal-output');

function appendLog(message, type = 'info') {
    const timestamp = new Date().toISOString().split('T')[1].slice(0, 12);
    const line = document.createElement('div');
    line.className = `log-line ${type}`;
    line.innerHTML = `<span style="color: #8b949e">[${timestamp}]</span> ${message}`;
    
    terminal.appendChild(line);
    terminal.scrollTop = terminal.scrollHeight;
}

async function triggerFault(faultType) {
    appendLog(`Initiating chaos vector: /playground/fault/${faultType}`, 'warning');
    
    try {
        const response = await fetch(`/playground/fault/${faultType}`);
        
        if (!response.ok) {
            appendLog(`Target application crashed with status ${response.status}`, 'error');
            appendLog(`GhostMachineMiddleware intercepted crash. Dispatching webhook to control plane...`, 'info');
            simulateGhostMachineWorkflow(faultType);
        } else {
            appendLog(`Unexpected: Target application survived the fault vector.`, 'warning');
        }
    } catch (error) {
        appendLog(`Network error or severe crash: ${error.message}`, 'error');
        simulateGhostMachineWorkflow(faultType);
    }
}

function triggerTotalSiteCrash() {
    // Navigate to playground
    document.querySelector('[data-target="view-playground"]').click();
    
    // Add crash CSS to body
    document.body.classList.add('site-crashed');
    
    appendLog(`FATAL ERROR: Total site crash initiated by user. Cascading failure...`, 'error');
    
    // Simulate GhostMachine fixing it
    simulateGhostMachineWorkflow('total-crash');
}

function resetStepper() {
    document.querySelectorAll('.step-indicator, .step-line').forEach(el => el.classList.remove('active'));
    document.getElementById('inspect-patch-btn').classList.add('hidden');
}

function activateStep(stepId) {
    const el = document.getElementById(stepId);
    if (el) {
        el.classList.add('active');
        const prevLine = el.previousElementSibling;
        if (prevLine && prevLine.classList.contains('step-line')) {
            prevLine.classList.add('active');
        }
    }
}

// Simulated WebSocket stream from GhostMachine.dev
function simulateGhostMachineWorkflow(faultType) {
    resetStepper();
    const events = [
        { msg: "> [GHOSTMACHINE] Webhook received. Trace ID generated.", delay: 800, type: "info", step: "step-ingest" },
        { msg: "> [GHOSTMACHINE] Analyzing traceback and local variables...", delay: 1500, type: "info" },
        { msg: "> [GHOSTMACHINE] Synthesizing reproduction test in Docker sandbox...", delay: 3000, type: "warning", step: "step-repro" },
        { msg: "> [GHOSTMACHINE] Sandbox execution failed as expected. Bug confirmed.", delay: 4500, type: "success" },
        { msg: "> [GHOSTMACHINE] LLM Agent drafting patch...", delay: 6000, type: "info", step: "step-patch" },
        { msg: "> [GHOSTMACHINE] Patch generated. Running AST Static Analysis...", delay: 7500, type: "info" },
        { msg: "> [GHOSTMACHINE] AST Guardrails Passed. No protected paths modified.", delay: 8500, type: "success" },
        { msg: "> [GHOSTMACHINE] Running full regression suite against patched sandbox...", delay: 10500, type: "warning", step: "step-regress" },
        { msg: "> [GHOSTMACHINE] Regression tests PASSED. Exit Code 0.", delay: 12500, type: "success" },
        { msg: "> [GHOSTMACHINE] Remediation complete. Pull Request opened on GitHub.", delay: 13500, type: "success", step: "step-pr" },
        { msg: "> [GHOSTMACHINE] SRE Post-Mortem generated in /incidents.", delay: 14000, type: "info" },
        { msg: "System fully recovered. Ready for next event.", delay: 15000, type: "info", onComplete: true }
    ];
    
    events.forEach(event => {
        setTimeout(() => {
            appendLog(event.msg, event.type);
            if (event.step) activateStep(event.step);
            if (event.onComplete) {
                document.getElementById('inspect-patch-btn').classList.remove('hidden');
                document.body.classList.remove('site-crashed'); // Restore site!
            }
        }, event.delay);
    });
}

function showPatchModal() {
    document.getElementById('pr-modal').classList.remove('hidden');
}

function closePatchModal() {
    document.getElementById('pr-modal').classList.add('hidden');
}

// SPA Navigation Logic
document.querySelectorAll('.nav-item').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Update active nav link
        document.querySelectorAll('.nav-item').forEach(l => l.classList.remove('active'));
        this.classList.add('active');
        
        // Switch visible view
        document.querySelectorAll('.spa-view').forEach(view => {
            view.classList.remove('active');
        });
        
        const targetId = this.getAttribute('data-target');
        const targetView = document.getElementById(targetId);
        if (targetView) {
            targetView.classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to top smoothly
        }
    });
});

function getPostTags(title, content) {
    const text = (title + " " + content).toLowerCase();
    const tags = [];
    if (text.includes("ast") || text.includes("guardrail") || text.includes("security")) tags.push("AST Security");
    if (text.includes("langgraph") || text.includes("state machine")) tags.push("LangGraph");
    if (text.includes("economics") || text.includes("mttr") || text.includes("roi") || text.includes("savings")) tags.push("SRE Economics");
    if (text.includes("sandbox") || text.includes("docker") || text.includes("pytest")) tags.push("Sandboxing");
    if (text.includes("webhook") || text.includes("telemetry") || text.includes("opentelemetry")) tags.push("Telemetry");
    if (text.includes("ghostmachine") && tags.length < 3) tags.push("Autonomous SRE");
    if (tags.length === 0) tags.push("Engineering");
    return tags.slice(0, 3);
}

function parseMarkdownToHTML(markdown) {
    return markdown
        .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .split('\n\n')
        .map(block => {
            const trimmed = block.trim();
            if (trimmed.startsWith('1.') || trimmed.startsWith('2.') || trimmed.startsWith('3.') || trimmed.startsWith('4.') || trimmed.startsWith('5.')) {
                const items = trimmed.split('\n').map(line => {
                    const cleanLine = line.replace(/^\d+\.\s*/, '');
                    return `<li>${cleanLine}</li>`;
                }).join('');
                return `<ol class="post-ordered-list">${items}</ol>`;
            } else if (trimmed.startsWith('•') || trimmed.startsWith('-')) {
                const items = trimmed.split('\n').map(line => {
                    const cleanLine = line.replace(/^[•\-]\s*/, '');
                    return `<li>${cleanLine}</li>`;
                }).join('');
                return `<ul class="post-bullet-list">${items}</ul>`;
            } else {
                return `<p>${trimmed.replace(/\n/g, '<br>')}</p>`;
            }
        })
        .join('');
}

async function fetchPosts() {
    try {
        const response = await fetch('/posts/?limit=20');
        if (response.ok) {
            const posts = await response.json();
            const container = document.getElementById('posts-container');
            container.innerHTML = '';
            
            posts.forEach(post => {
                const card = document.createElement('article');
                card.className = 'post-card glass-panel';
                
                const tags = getPostTags(post.title, post.content);
                const tagPills = tags.map(tag => `<span class="post-tag">${tag}</span>`).join('');
                
                const words = post.content.split(/\s+/).length;
                const readMinutes = Math.max(1, Math.ceil(words / 180));
                
                const formattedDate = post.created_at 
                    ? new Date(post.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
                    : 'System Transmission';

                const htmlContent = parseMarkdownToHTML(post.content);

                card.innerHTML = `
                    <div class="post-meta">
                        <div class="post-tags-group">${tagPills}</div>
                        <div class="post-time-meta">
                            <span>${formattedDate}</span> • <span>${readMinutes} min read</span>
                        </div>
                    </div>
                    <h3 class="post-title">${post.title}</h3>
                    <div class="post-content">
                        ${htmlContent}
                    </div>
                `;
                container.appendChild(card);
            });
        }
} catch (e) {
        console.error("Failed to load posts", e);
    }
}

fetchPosts();
appendLog("GhostMachine telemetry stream initialized. Waiting for fault events...", "info");

// Contact Modal Logic
function openContactModal() {
    document.getElementById('contact-modal').classList.remove('hidden');
    document.getElementById('contact-success').classList.add('hidden');
    document.getElementById('contact-form').reset();
}

function closeContactModal() {
    document.getElementById('contact-modal').classList.add('hidden');
}

const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = contactForm.querySelector('button[type="submit"]');
        const originalText = btn.innerText;
        btn.innerText = 'Sending...';
        btn.disabled = true;

        const payload = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            message: document.getElementById('message').value
        };

        try {
            const res = await fetch('/api/contact/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                document.getElementById('contact-form').reset();
                document.getElementById('contact-success').classList.remove('hidden');
            } else {
                alert('Failed to send message.');
            }
        } catch (err) {
            console.error(err);
            alert('Error sending message.');
        } finally {
            btn.innerText = originalText;
            btn.disabled = false;
        }
    });
}
