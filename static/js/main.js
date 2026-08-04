/**
 * MyPath Client-Side Controller
 * Architecture: Vanilla JavaScript (Frontend UI) <-> Flask API (/api/evaluate)
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
 * Sanitizes input, constructs payload, and posts to Flask API endpoint (/api/evaluate)
 * @param {Event} event 
 */
async function submitProfile(event) {
    event.preventDefault();

    const submitBtn = document.getElementById("submit-btn");
    const spinner = document.getElementById("spinner");
    
    // Extract basic fields
    const nameVal = document.getElementById("name") ? document.getElementById("name").value.trim() : "";
    const incomeVal = parseFloat(document.getElementById("income")?.value) || 0.0;
    const locationVal = document.getElementById("location")?.value || "Any";
    const hasDisability = document.getElementById("has_disability")?.checked || false;
    const isSassa = document.getElementById("is_sassa_recipient")?.checked || false;
    
    // Parse user interests array
    const interestsElem = document.getElementById("interests");
    const interestsRaw = interestsElem ? interestsElem.value : "";
    const interestsList = interestsRaw
        .split(",")
        .map(i => i.trim())
        .filter(i => i.length > 0);

    // Build & sanitize subjects dictionary
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

    // Payload formatted to match /api/evaluate endpoint payload parameters
    const payload = {
        name: nameVal,
        user_interests: interestsList,
        household_income: incomeVal,
        location: locationVal,
        has_disability: hasDisability,
        is_sassa_recipient: isSassa,
        subjects: subjectsDict
    };

    // UI Loading state
    if (submitBtn) submitBtn.disabled = true;
    if (spinner) spinner.classList.remove("hidden");

    try {
        const response = await fetch("/api/evaluate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const rawText = await response.text();

        // Safe JSON parse handling
        let responseData;
        try {
            responseData = JSON.parse(rawText);
        } catch (parseError) {
            console.error("Non-JSON Server Output Received:", rawText);
            throw new Error(`Server returned HTML error (${response.status}). Check backend console.`);
        }

        if (!response.ok) {
            const errorMessage = responseData.message || responseData.error || `HTTP ${response.status} Error`;
            throw new Error(errorMessage);
        }

        // Render dashboard using response metrics and guidance object
        renderDashboard(responseData);

    } catch (error) {
        console.error("[MyPath Client Error]:", error);
        alert(`Failed to compute profile recommendations:\n${error.message}`);
    } finally {
        if (submitBtn) submitBtn.disabled = false;
        if (spinner) spinner.classList.add("hidden");
    }
}

/**
 * Updates UI Dashboard with calculated APS, NSFAS eligibility, and guidance schemas
 * @param {Object} data 
 */
function renderDashboard(data) {
    const emptyState = document.getElementById("empty-state");
    const dashboardContent = document.getElementById("dashboard-content");

    if (emptyState) emptyState.classList.add("hidden");
    if (dashboardContent) dashboardContent.classList.remove("hidden");

    const metrics = data.metrics || {};
    const guidance = data.guidance || {};

    // 1. Top Metric Cards
    // Total APS score calculated excluding LO
    const totalAps = metrics.aps ? metrics.aps.total_aps : "--";
    const apsElem = document.getElementById("res-aps");
    if (apsElem) apsElem.innerText = totalAps;
    
    // Top Career Title
    const topCareers = guidance.top_careers || [];
    const topCareerTitle = topCareers.length > 0 ? topCareers[0].career_title : "N/A";
    const careerElem = document.getElementById("res-top-career");
    if (careerElem) careerElem.innerText = topCareerTitle;

    // Funding Status & NSFAS R350,000 threshold indicator
    const fundingInfo = metrics.funding || {};
    const fundingElem = document.getElementById("res-funding-count");
    if (fundingElem) {
        fundingElem.innerText = fundingInfo.nsfas_eligible ? "NSFAS Eligible" : "Missing Middle / Bursaries";
    }

    // 2. ✨ AI Counselor Brief & Roadmap Narrative
    const aiGuidanceElem = document.getElementById("res-ai-guidance");
    if (aiGuidanceElem) {
        aiGuidanceElem.innerText = guidance.counselor_brief || "Your personalized roadmap is ready.";
    }

    // 3. Render Categorized Response Tabs
    renderTabCareers(guidance.top_careers || []);
    renderTabUniversities(guidance.top_universities || []);
    renderTabTVET(guidance.top_tvet_courses || []);
    renderTabFunding(guidance.top_bursaries || []);
}

/**
 * Render Top 3 Careers
 */
function renderTabCareers(careers) {
    const container = document.getElementById("tab-careers");
    if (!container) return;

    if (careers.length === 0) {
        container.innerHTML = `<p class="item-sub">No matching careers found for your selected interests.</p>`;
        return;
    }
    
    container.innerHTML = careers.map(c => `
        <div class="item-card">
            <div>
                <div class="item-title">${escapeHtml(c.career_title)}</div>
                <div class="item-sub">${escapeHtml(c.fit_reasoning)}</div>
                ${c.skill_targets && c.skill_targets.length > 0 
                    ? `<div class="item-tags" style="margin-top: 6px;">
                        ${c.skill_targets.map(s => `<span class="tag-badge">${escapeHtml(s)}</span>`).join(" ")}
                       </div>` 
                    : ''}
            </div>
        </div>
    `).join("");
}

/**
 * Render Top 3 Universities + Course & App Fee
 */
function renderTabUniversities(unis) {
    const container = document.getElementById("tab-universities");
    if (!container) return;

    if (unis.length === 0) {
        container.innerHTML = `<p class="item-sub">No eligible university degree programmes found matching your APS.</p>`;
        return;
    }

    container.innerHTML = unis.map(u => `
        <div class="item-card">
            <div>
                <div class="item-title">${escapeHtml(u.degree_or_diploma)}</div>
                <div class="item-sub">${escapeHtml(u.university_name)}</div>
            </div>
            <div class="badge-score">App Fee: ${escapeHtml(u.application_fee)}</div>
        </div>
    `).join("");
}

/**
 * Render Top 3 TVET Colleges + NQF Level
 */
function renderTabTVET(tvets) {
    const container = document.getElementById("tab-tvet");
    if (!container) return;

    if (tvets.length === 0) {
        container.innerHTML = `<p class="item-sub">No eligible TVET college courses found matching your APS.</p>`;
        return;
    }

    container.innerHTML = tvets.map(t => `
        <div class="item-card">
            <div>
                <div class="item-title">${escapeHtml(t.course_name)}</div>
                <div class="item-sub">${escapeHtml(t.tvet_college)}</div>
            </div>
            <div class="badge-score">${escapeHtml(t.nqf_level)}</div>
        </div>
    `).join("");
}

/**
 * Render Top 3 Eligible Bursaries
 */
function renderTabFunding(bursaries) {
    const container = document.getElementById("tab-funding");
    if (!container) return;

    if (bursaries.length === 0) {
        container.innerHTML = `<p class="item-sub">No eligible bursaries found matching your APS and income threshold.</p>`;
        return;
    }

    container.innerHTML = bursaries.map(f => `
        <div class="item-card">
            <div>
                <div class="item-title">${escapeHtml(f.bursary_name)}</div>
                <div class="item-sub">${escapeHtml(f.eligibility_notes)}</div>
                <div class="item-sub" style="font-size: 0.825rem; color: #666; margin-top: 4px;">Coverage: ${escapeHtml(f.coverage_details)}</div>
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