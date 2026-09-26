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

// Smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

async function fetchPosts() {
    try {
        const response = await fetch('/posts/');
        if (response.ok) {
            const posts = await response.json();
            const container = document.getElementById('posts-container');
            container.innerHTML = '';
            
            posts.forEach(post => {
                const card = document.createElement('div');
                card.className = 'post-card glass-panel';
                
                // Simple markdown-to-html conversion for basic paragraphs and bold text
                let htmlContent = post.content
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .split('\n\n')
                    .map(para => `<p>${para.replace(/\n/g, '<br>')}</p>`)
                    .join('');

                card.innerHTML = `
                    <h3>${post.title}</h3>
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
