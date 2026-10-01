// app.js - Frontend Logic for Tim O'Hagan CMS (v2.0 with Categorized Transmissions)

const terminal = document.getElementById('terminal-output');

function escapeHtml(unsafe) {
    return (unsafe || '').toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function appendLog(message, type = 'info') {
    if (!terminal) return;
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
    const playgroundNav = document.querySelector('[data-target="view-playground"]');
    if (playgroundNav) playgroundNav.click();
    
    document.body.classList.add('site-crashed');
    appendLog(`FATAL ERROR: Total site crash initiated by user. Cascading failure...`, 'error');
    simulateGhostMachineWorkflow('total-crash');
}

function resetStepper() {
    document.querySelectorAll('.step-indicator, .step-line').forEach(el => el.classList.remove('active'));
    const inspectBtn = document.getElementById('inspect-patch-btn');
    if (inspectBtn) inspectBtn.classList.add('hidden');
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
                const inspectBtn = document.getElementById('inspect-patch-btn');
                if (inspectBtn) inspectBtn.classList.remove('hidden');
                document.body.classList.remove('site-crashed');
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

    const prModal = document.getElementById('pr-modal');
    if (prModal) prModal.classList.remove('hidden');
}

function closePatchModal() {
    const prModal = document.getElementById('pr-modal');
    if (prModal) prModal.classList.add('hidden');
}

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
        if (targetId === 'view-posts') {
            const hash = currentCategory && currentCategory !== 'all' ? `posts/${currentCategory}` : 'posts';
            history.pushState(null, null, `#${hash}`);
        } else {
            const hash = targetId.replace('view-', '');
            history.pushState(null, null, `#${hash}`);
        }
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

// ============================================================================
// Posts & Category Pages Architecture
// ============================================================================

let cachedCategories = [];
let cachedPosts = [];
let currentCategory = 'all';

const CATEGORY_FALLBACK_META = {
    'autonomous-sre': {
        name: 'Autonomous SRE',
        icon: '⚡',
        description: 'Self-healing architectures, automated MTTR reduction, and production agent mechanics.'
    },
    'chaos-engineering': {
        name: 'Chaos Engineering',
        icon: '💥',
        description: 'Fault injection, synthetic reproduction sandboxes, and automated regression verification.'
    },
    'agentic-architecture': {
        name: 'Agentic Architecture',
        icon: '🧠',
        description: 'Stateful orchestration, cyclic graphs with LangGraph, and deterministic state reducers.'
    },
    'ai-security': {
        name: 'AI Security & Guardrails',
        icon: '🛡️',
        description: 'Compiler-level AST validation, bare except elimination, and zero-trust LLM patch synthesis.'
    }
};

function getCategoryMeta(categoryNameOrSlug) {
    if (!categoryNameOrSlug) return null;
    const lower = categoryNameOrSlug.toLowerCase();
    
    // Look in cached categories first
    const found = cachedCategories.find(c => c.slug === lower || c.name.toLowerCase() === lower);
    if (found) return found;

    // Look in fallback map
    for (const [slug, meta] of Object.entries(CATEGORY_FALLBACK_META)) {
        if (slug === lower || meta.name.toLowerCase() === lower) {
            return { slug, ...meta, count: 0 };
        }
    }

    return {
        name: categoryNameOrSlug,
        slug: lower.replace(/\s+/g, '-'),
        icon: '📁',
        description: `Transmissions and technical insights on ${categoryNameOrSlug}.`,
        count: 0
    };
}

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
            if (/^\d+\./.test(trimmed)) {
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

// Fetch categories from backend API
async function fetchCategories() {
    try {
        const response = await fetch('/posts/categories');
        if (response.ok) {
            cachedCategories = await response.json();
            renderCategoryTabs();
            renderCategoryCardsOverview();
        }
    } catch (err) {
        console.error("Failed to load categories", err);
    }
}

// Render the category pills/tabs
function renderCategoryTabs() {
    const tabsContainer = document.getElementById('dynamic-category-tabs');
    if (!tabsContainer) return;

    let totalPosts = 0;
    tabsContainer.innerHTML = cachedCategories.map(cat => {
        totalPosts += cat.count || 0;
        const isActive = currentCategory === cat.slug;
        return `
            <button class="cat-nav-tab ${isActive ? 'active' : ''}" 
                    data-category="${cat.slug}" 
                    role="tab" 
                    aria-selected="${isActive}"
                    onclick="selectCategory('${cat.slug}', event)">
                <span class="cat-tab-icon">${cat.icon || '📁'}</span>
                <span class="cat-tab-name">${escapeHtml(cat.name)}</span>
                <span class="cat-tab-count">${cat.count || 0}</span>
            </button>
        `;
    }).join('');

    const countAllEl = document.getElementById('count-all');
    if (countAllEl) {
        countAllEl.textContent = totalPosts || cachedPosts.length;
    }
}

// Render the 4-domain category shelf cards (shown on "All Transmissions" overview)
function renderCategoryCardsOverview() {
    const overviewContainer = document.getElementById('category-cards-overview');
    if (!overviewContainer) return;

    overviewContainer.innerHTML = cachedCategories.map(cat => `
        <div class="category-card" onclick="selectCategory('${cat.slug}', event)">
            <div class="category-card-top">
                <div class="category-card-icon">${cat.icon || '📁'}</div>
                <div class="category-card-count">${cat.count || 0} posts</div>
            </div>
            <h3 class="category-card-title">${escapeHtml(cat.name)}</h3>
            <p class="category-card-desc">${escapeHtml(cat.description || '')}</p>
            <div class="category-card-action">
                <span>Explore Category</span>
                <span>→</span>
            </div>
        </div>
    `).join('');
}

// Switch between Category Pages
function selectCategory(catSlug, event, updateHash = true) {
    if (event) event.preventDefault();
    currentCategory = catSlug || 'all';

    // Switch view to posts if not already on it
    const postsView = document.getElementById('view-posts');
    if (postsView && !postsView.classList.contains('active')) {
        switchView('view-posts', false);
    }

    // Update active tab buttons
    document.querySelectorAll('.cat-nav-tab').forEach(tab => {
        const tabCat = tab.getAttribute('data-category');
        if (tabCat === currentCategory) {
            tab.classList.add('active');
            tab.setAttribute('aria-selected', 'true');
        } else {
            tab.classList.remove('active');
            tab.setAttribute('aria-selected', 'false');
        }
    });

    // Update URL hash
    if (updateHash) {
        const hash = currentCategory === 'all' ? 'posts' : `posts/${currentCategory}`;
        history.pushState(null, null, `#${hash}`);
    }

    // Toggle category page views
    const breadcrumbs = document.getElementById('posts-breadcrumbs');
    const breadcrumbCat = document.getElementById('breadcrumb-current-cat');
    const titleWrapper = document.getElementById('posts-title-wrapper');
    const categoryBanner = document.getElementById('category-page-banner');
    const overviewCards = document.getElementById('category-cards-overview');
    const listHeading = document.getElementById('posts-list-heading');

    if (currentCategory === 'all') {
        if (breadcrumbs) breadcrumbs.classList.add('hidden');
        if (titleWrapper) titleWrapper.classList.remove('hidden');
        if (categoryBanner) categoryBanner.classList.add('hidden');
        if (overviewCards) overviewCards.classList.remove('hidden');
        if (listHeading) listHeading.textContent = 'All Recent Transmissions';
    } else {
        const catMeta = getCategoryMeta(currentCategory);
        if (breadcrumbs) {
            breadcrumbs.classList.remove('hidden');
            if (breadcrumbCat) breadcrumbCat.textContent = catMeta.name;
        }
        if (titleWrapper) titleWrapper.classList.add('hidden');
        if (overviewCards) overviewCards.classList.add('hidden');

        if (categoryBanner) {
            categoryBanner.classList.remove('hidden');
            const iconEl = document.getElementById('banner-cat-icon');
            const titleEl = document.getElementById('banner-cat-title');
            const descEl = document.getElementById('banner-cat-desc');
            const countEl = document.getElementById('banner-cat-count');

            if (iconEl) iconEl.textContent = catMeta.icon || '📁';
            if (titleEl) titleEl.textContent = catMeta.name;
            if (descEl) descEl.textContent = catMeta.description || '';
            if (countEl) countEl.textContent = `${catMeta.count || 0} Transmissions Available`;
        }

        if (listHeading) {
            const meta = getCategoryMeta(currentCategory);
            listHeading.textContent = `${meta ? meta.name : 'Category'} Transmissions`;
        }
    }

    renderPostsList();
}

// Fetch all posts from API
async function fetchPosts() {
    try {
        const response = await fetch('/posts/?limit=50');
        if (response.ok) {
            cachedPosts = await response.json();
            
            // Recount category badges if needed
            const countAllEl = document.getElementById('count-all');
            if (countAllEl) countAllEl.textContent = cachedPosts.length;

            renderPostsList();
        }
    } catch (e) {
        console.error("Failed to load posts", e);
        const container = document.getElementById('posts-container');
        if (container) {
            container.innerHTML = `<div class="glass-panel" style="padding: 24px; text-align: center; color: #f87171;">Failed to load transmissions.</div>`;
        }
    }
}

// Filter and render posts into container
function renderPostsList() {
    const container = document.getElementById('posts-container');
    const countTag = document.getElementById('posts-filtered-count');
    if (!container) return;

    let filtered = cachedPosts;
    if (currentCategory !== 'all') {
        const catMeta = getCategoryMeta(currentCategory);
        const targetName = catMeta ? catMeta.name.toLowerCase() : currentCategory.toLowerCase();
        const targetSlug = catMeta ? catMeta.slug : currentCategory.toLowerCase();

        filtered = cachedPosts.filter(p => {
            const postCat = (p.category || 'Autonomous SRE').toLowerCase();
            const postCatSlug = postCat.replace(/\s+/g, '-');
            return postCat === targetName || postCatSlug === targetSlug;
        });
    }

    if (countTag) {
        countTag.textContent = `Showing ${filtered.length} of ${cachedPosts.length} transmissions`;
    }

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="glass-panel" style="padding: 40px; text-align: center; border-radius: 14px;">
                <p style="color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 12px;">No transmissions found for this category yet.</p>
                <button class="btn secondary-btn" onclick="selectCategory('all', event)">View All Transmissions</button>
            </div>
        `;
        return;
    }

    container.innerHTML = '';
    filtered.forEach(post => {
        const card = document.createElement('article');
        card.className = 'post-card glass-panel animate-in';
        
        const catMeta = getCategoryMeta(post.category || 'Autonomous SRE');
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
                <div class="post-tags-group">
                    <button class="post-category-badge" onclick="selectCategory('${catMeta.slug}', event)" title="View all in ${escapeHtml(catMeta.name)}">
                        <span>${catMeta.icon}</span> ${escapeHtml(catMeta.name)}
                    </button>
                    ${tagPills}
                </div>
                <div class="post-time-meta">
                    <span>${formattedDate}</span> • <span>${readMinutes} min read</span>
                </div>
            </div>
            <h3 class="post-title">${escapeHtml(post.title)}</h3>
            <div class="post-content">
                ${htmlContent}
            </div>
        `;
        container.appendChild(card);
    });
}

// Hash Routing on initial load and back/forward navigation
function handleHashRoute() {
    const rawHash = (window.location.hash || '').replace('#', '').trim();
    
    // Check for posts category sub-routes e.g. #posts/autonomous-sre or #transmissions/chaos-engineering
    if (rawHash.startsWith('posts') || rawHash.startsWith('transmissions')) {
        switchView('view-posts', false);
        
        let categorySlug = 'all';
        if (rawHash.includes('/')) {
            const parts = rawHash.split('/');
            categorySlug = parts[1] || 'all';
        } else if (rawHash.includes('?category=')) {
            const parts = rawHash.split('?category=');
            categorySlug = parts[1] || 'all';
        }
        
        selectCategory(categorySlug, null, false);
        return;
    }

    const validTargets = {
        'about': 'view-about',
        'playground': 'view-playground',
        'chaos': 'view-playground'
    };

    const targetId = validTargets[rawHash] || 'view-about';
    switchView(targetId, false);
}

window.addEventListener('DOMContentLoaded', async () => {
    await fetchCategories();
    await fetchPosts();
    handleHashRoute();
});

window.addEventListener('hashchange', handleHashRoute);

// Contact Modal Logic
function openContactModal() {
    const modal = document.getElementById('contact-modal');
    const success = document.getElementById('contact-success');
    const form = document.getElementById('contact-form');
    if (modal) modal.classList.remove('hidden');
    if (success) success.classList.add('hidden');
    if (form) form.reset();
}

function closeContactModal() {
    const modal = document.getElementById('contact-modal');
    if (modal) modal.classList.add('hidden');
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
                contactForm.reset();
                const success = document.getElementById('contact-success');
                if (success) success.classList.remove('hidden');
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
