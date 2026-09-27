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

const PATCH_TEMPLATES = {
    'cpu-500': {
        title: "PR #42: Automated Remediation for CPU Fault (ZeroDivisionError)",
        mttr: "~52s",
        cost: "$0.0263",
        diff: `--- a/app/api/routes/playground.py\n+++ b/app/api/routes/playground.py\n@@ -10,2 +10,4 @@\n-    fault = 1 / 0\n+    divisor = request.query_params.get("divisor", 1)\n+    fault = 1 / (int(divisor) if int(divisor) != 0 else 1)\n     return {"result": fault}`
    },
    'schema-422': {
        title: "PR #43: Automated Schema Fallback & Validation Normalization",
        mttr: "~48s",
        cost: "$0.0241",
        diff: `--- a/app/schemas/pydantic_schemas.py\n+++ b/app/schemas/pydantic_schemas.py\n@@ -12,2 +12,4 @@\n-    trace_id: str\n+    trace_id: Optional[str] = Field(default_factory=lambda: uuid.uuid4().hex)`
    },
    'db-deadlock': {
        title: "PR #44: Dynamic Backoff & Lock Timeout for Deadlock Prevention",
        mttr: "~64s",
        cost: "$0.0289",
        diff: `--- a/app/core/database.py\n+++ b/app/core/database.py\n@@ -15,2 +15,5 @@\n+    connect_args={"command_timeout": 5},\n+    execution_options={"isolation_level": "READ COMMITTED"}`
    },
    'memory-asset': {
        title: "PR #45: Stream Backpressure Buffer for Asset Processing",
        mttr: "~59s",
        cost: "$0.0274",
        diff: `--- a/app/core/storage.py\n+++ b/app/core/storage.py\n@@ -25,2 +25,4 @@\n-    raw = file.read()\n+    raw = await stream_with_backpressure(file, chunk_size=65536)`
    },
    'total-crash': {
        title: "PR #46: Full Fault Isolation & Circuit Breaker Engagement",
        mttr: "~38s",
        cost: "$0.0195",
        diff: `--- a/app/main.py\n+++ b/app/main.py\n@@ -18,2 +18,4 @@\n-    app.add_middleware(GhostMachineMiddleware)\n+    app.add_middleware(GhostMachineMiddleware, circuit_breaker=True)`
    }
};

let currentFaultType = 'cpu-500';

// Simulated WebSocket stream from GhostMachine.dev
function simulateGhostMachineWorkflow(faultType) {
    currentFaultType = faultType;
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
    const patchData = PATCH_TEMPLATES[currentFaultType] || PATCH_TEMPLATES['cpu-500'];
    const modalHeader = document.querySelector('#pr-modal .modal-header h2');
    const modalMetrics = document.querySelector('#pr-modal .modal-metrics');
    const modalCode = document.querySelector('#pr-modal pre code');
    
    if (modalHeader) modalHeader.innerHTML = `<span style="color: #238636;">✓</span> ${escapeHtml(patchData.title)}`;
    if (modalMetrics) {
        modalMetrics.innerHTML = `
            <div class="metric"><span class="label">MTTR</span><span class="value">${patchData.mttr}</span></div>
            <div class="metric"><span class="label">Cost</span><span class="value" style="color: #0f0;">${patchData.cost}</span></div>
            <div class="metric"><span class="label">AST Pass</span><span class="value" style="color: #0f0;">True</span></div>
        `;
    }
    if (modalCode) modalCode.textContent = patchData.diff;

    document.getElementById('pr-modal').classList.remove('hidden');
}

function closePatchModal() {
    document.getElementById('pr-modal').classList.add('hidden');
}

// Escape key to close modals
window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closePatchModal();
        closeContactModal();
    }
});

// Centralized SPA View Navigation
function switchView(targetId, updateHash = true) {
    const targetView = document.getElementById(targetId);
    if (!targetView) return;

    // Update active nav links
    document.querySelectorAll('.nav-item').forEach(l => {
        if (l.getAttribute('data-target') === targetId) {
            l.classList.add('active');
        } else {
            l.classList.remove('active');
        }
    });

    // Update visible views
    document.querySelectorAll('.spa-view').forEach(view => {
        view.classList.remove('active');
    });
    targetView.classList.add('active');

    if (updateHash) {
        const hash = targetId.replace('view-', '');
        history.pushState(null, null, `#${hash}`);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Bind click handlers to nav items
document.querySelectorAll('.nav-item').forEach(link => {
    link.addEventListener('click', function(e) {
        const targetId = this.getAttribute('data-target');
        if (targetId) {
            e.preventDefault();
            switchView(targetId, true);
        }
    });
});

// Hash Routing on initial load and back/forward navigation
function handleHashRoute() {
    const rawHash = (window.location.hash || '').replace('#', '').toLowerCase();
    const validTargets = {
        'about': 'view-about',
        'posts': 'view-posts',
        'transmissions': 'view-posts',
        'playground': 'view-playground',
        'chaos': 'view-playground'
    };

    const targetId = validTargets[rawHash] || 'view-about';
    switchView(targetId, false);
}

window.addEventListener('DOMContentLoaded', handleHashRoute);
window.addEventListener('hashchange', handleHashRoute);

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
