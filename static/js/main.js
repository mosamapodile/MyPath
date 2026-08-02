/**
 * MyPath Client-Side Controller
 * Architecture: Vanilla JavaScript (Frontend UI) <-> Flask API (/api/recommend)
 * Author: Mosa Mapodile
 */

// Default standard South African NSC subjects loaded on startup
const DEFAULT_SUBJECTS = [
    "Mathematics",
    "English First Additional Language",
    "Physical Sciences",
    "Life Sciences",
    "Accounting",
    "Life Orientation",
    "Geography"
];

document.addEventListener("DOMContentLoaded", () => {
    initSubjectRows();
});

/**
 * Populate initial subject input rows
 */
function initSubjectRows() {
    const container = document.getElementById("subject-list");
    if (!container) return;
    
    container.innerHTML = "";
    DEFAULT_SUBJECTS.forEach(subjectName => {
        addSubjectRow(subjectName);
    });
}

/**
 * Dynamically adds a new subject input row to the DOM
 * Allows 6, 7, 8+ customizable subjects
 * @param {string} initialName 
 */
function addSubjectRow(initialName = "") {
    const container = document.getElementById("subject-list");
    if (!container) return;

    const row = document.createElement("div");
    row.className = "subject-row";

    row.innerHTML = `
        <input type="text" value="${escapeHtml(initialName)}" placeholder="Subject Name" class="input-field subj-name" required>
        <input type="number" min="0" max="100" placeholder="%" class="input-field subj-mark" required>
        <button type="button" class="btn-remove" onclick="removeSubjectRow(this)" title="Remove subject">✕</button>
    `;

    container.appendChild(row);
}

/**
 * Removes a subject input row
 * @param {HTMLElement} button 
 */
function removeSubjectRow(button) {
    const container = document.getElementById("subject-list");
    if (container.children.length > 1) {
        button.closest(".subject-row").remove();
    } else {
        alert("At least one subject mark is required to calculate your APS.");
    }
}

/**
 * Main form submission handler
 * Sanitizes input, constructs the exact payload, and posts to Flask API
 * @param {Event} event 
 */
async function submitProfile(event) {
    event.preventDefault();

    const submitBtn = document.getElementById("submit-btn");
    const spinner = document.getElementById("spinner");
    
    // Extract basic fields
    const nameVal = document.getElementById("name").value.trim();
    const gradeVal = parseInt(document.getElementById("grade").value, 10);
    const incomeVal = parseFloat(document.getElementById("income").value) || 0.0;
    
    // Parse interests array
    const interestsRaw = document.getElementById("interests").value;
    const interestsList = interestsRaw
        .split(",")
        .map(i => i.trim())
        .filter(i => i.length > 0);

    // Build & sanitize subjects key-value object
    const subjectsDict = {};
    const subjectRows = document.querySelectorAll(".subject-row");

    subjectRows.forEach(row => {
        const nameInput = row.querySelector(".subj-name");
        const markInput = row.querySelector(".subj-mark");

        if (nameInput && markInput) {
            const subjName = nameInput.value.trim();
            const rawMark = parseInt(markInput.value, 10);

            if (subjName !== "" && !isNaN(rawMark)) {
                // Clamp percentage between 0 and 100
                subjectsDict[subjName] = Math.min(100, Math.max(0, rawMark));
            }
        }
    });

    // Client-side validation guard
    if (Object.keys(subjectsDict).length === 0) {
        alert("Please enter at least one valid subject name and percentage.");
        return;
    }

    // Construct request payload matching student_request schema
    const payload = {
        name: nameVal,
        grade: gradeVal,
        household_income: incomeVal,
        subjects: subjectsDict,
        interests: interestsList
    };

    // UI Loading state
    if (submitBtn) submitBtn.disabled = true;
    if (spinner) spinner.classList.remove("hidden");

    try {
        const response = await fetch("/api/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const responseData = await response.json();

        // Handle bad request (HTTP 400) or server errors (HTTP 500)
        if (!response.ok) {
            const errorMessage = responseData.error || responseData.message || `HTTP ${response.status} Bad Request`;
            throw new Error(errorMessage);
        }

        // Render response dashboard
        renderDashboard(responseData);

    } catch (error) {
        console.error("[MyPath API Error]:", error);
        alert(`Failed to compute profile recommendations:\n${error.message}`);
    } finally {
        if (submitBtn) submitBtn.disabled = false;
        if (spinner) spinner.classList.add("hidden");
    }
}

/**
 * Updates UI Dashboard with calculated APS and AI narrative facts
 * @param {Object} data 
 */
function renderDashboard(data) {
    const emptyState = document.getElementById("empty-state");
    const dashboardContent = document.getElementById("dashboard-content");

    if (emptyState) emptyState.classList.add("hidden");
    if (dashboardContent) dashboardContent.classList.remove("hidden");

    // Top Header Metrics
    document.getElementById("res-aps").innerText = data.aps_score ?? "--";
    
    const topCareer = (data.recommended_careers && data.recommended_careers.length > 0)
        ? data.recommended_careers[0].title
        : "N/A";
    document.getElementById("res-top-career").innerText = topCareer;

    const fundingCount = data.funding_matches ? data.funding_matches.length : 0;
    document.getElementById("res-funding-count").innerText = fundingCount;

    // AI Narrative Output
    const aiGuidanceElem = document.getElementById("res-ai-guidance");
    if (aiGuidanceElem) {
        aiGuidanceElem.innerText = data.ai_guidance || "Your personalized roadmap is ready.";
    }

    // Tab Contents
    renderTabCareers(data.recommended_careers || []);
    renderTabUniversities(data.eligible_universities || []);
    renderTabTVET(data.eligible_tvet || []);
    renderTabFunding(data.funding_matches || []);
}

function renderTabCareers(careers) {
    const container = document.getElementById("tab-careers");
    if (!container) return;

    if (careers.length === 0) {
        container.innerHTML = `<p class="item-sub">No explicit career matches found for the selected interests.</p>`;
        return;
    }
    
    container.innerHTML = careers.map(c => `
        <div class="item-card">
            <div>
                <div class="item-title">${escapeHtml(c.title)}</div>
                <div class="item-sub">Category: ${escapeHtml(c.category || 'General')} | Growth: ${escapeHtml(c.industry_growth || 'High')}</div>
            </div>
            <div class="badge-score">${c.fit_score ?? 85}% Fit</div>
        </div>
    `).join("");
}

function renderTabUniversities(unis) {
    const container = document.getElementById("tab-universities");
    if (!container) return;

    if (unis.length === 0) {
        container.innerHTML = `<p class="item-sub">No university degree programmes matched current APS score.</p>`;
        return;
    }

    container.innerHTML = unis.map(u => `
        <div class="item-card">
            <div>
                <div class="item-title">${escapeHtml(u.programme || u.name)}</div>
                <div class="item-sub">${escapeHtml(u.institution || 'University')}</div>
            </div>
            <div class="badge-score">Min APS: ${u.min_aps ?? '--'}</div>
        </div>
    `).join("");
}

function renderTabTVET(tvets) {
    const container = document.getElementById("tab-tvet");
    if (!container) return;

    if (tvets.length === 0) {
        container.innerHTML = `<p class="item-sub">No TVET college programmes found.</p>`;
        return;
    }

    container.innerHTML = tvets.map(t => `
        <div class="item-card">
            <div>
                <div class="item-title">${escapeHtml(t.programme || t.name)}</div>
                <div class="item-sub">${escapeHtml(t.institution || 'TVET College')}</div>
            </div>
            <div class="badge-score">Min APS: ${t.min_aps ?? '--'}</div>
        </div>
    `).join("");
}

function renderTabFunding(funding) {
    const container = document.getElementById("tab-funding");
    if (!container) return;

    if (funding.length === 0) {
        container.innerHTML = `<p class="item-sub">No bursaries found matching this income threshold.</p>`;
        return;
    }

    container.innerHTML = funding.map(f => `
        <div class="item-card">
            <div>
                <div class="item-title">${escapeHtml(f.name)}</div>
                <div class="item-sub">Coverage: ${escapeHtml(f.coverage || 'Tuition & Accommodation')}</div>
            </div>
            <div class="badge-score">Eligible</div>
        </div>
    `).join("");
}

/**
 * Tab switching controller
 */
function switchTab(event, tabName) {
    document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
    document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.add("hidden"));

    if (event && event.currentTarget) {
        event.currentTarget.classList.add("active");
    }
    
    const activePane = document.getElementById(`tab-${tabName}`);
    if (activePane) {
        activePane.classList.remove("hidden");
    }
}

/**
 * Utility helper to sanitize HTML strings to avoid XSS issues
 */
function escapeHtml(str) {
    if (typeof str !== 'string') return str;
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}