/**
 * Context Menu Module
 *
 * Provides right-click menu on Jira issues:
 * - "Link to OKR"
 * - "View Trust Score"
 * - "Mark as Strategic"
 *
 * Referenced by: SPEC.md Seção 4.1 (Context menu feature)
 */

import { log, logError } from '../utils/logger';

/**
 * Setup context menu
 *
 * Registers context menu handlers for Jira issues
 * @param {JiraAPI} jiraAPI
 * @param {APISClient} apisClient
 */
export async function setupContextMenu(jiraAPI, apisClient) {
  log('📋 Setting up Context Menu module...');

  // Register Jira context menu API
  if (window.AP?.jira?.issues?.context?.getSelectedIssues) {
    // Use Jira's context menu system
    registerJiraContextMenu(jiraAPI, apisClient);
  } else {
    // Fallback: Manual right-click handler
    registerManualContextMenu(jiraAPI, apisClient);
  }

  log('✅ Context menu initialized');
}

/**
 * Register using Jira's built-in context menu API
 */
function registerJiraContextMenu(jiraAPI, apisClient) {
  // Jira API for context menu:
  // AP.jira.context.getSelectedIssues()
  // AP.jira.navContext.onIssuePageView()

  document.addEventListener('contextmenu', e => {
    const issueElement = e.target.closest('[data-issue-key]');

    if (issueElement) {
      const issueKey = issueElement.getAttribute('data-issue-key');
      handleContextMenu(e, issueKey, jiraAPI, apisClient);
    }
  });
}

/**
 * Fallback: Manual context menu handler
 */
function registerManualContextMenu(jiraAPI, apisClient) {
  document.addEventListener('contextmenu', async e => {
    // Check if right-clicked on issue summary or key
    const summaryElement = e.target.closest('.issue-summary, [data-testid="issue.views.issue-base.foundation.summary.breadcrumbs.context.issue-key"]');
    const keyElement = e.target.closest('[class*="issue-key"], [data-issue-key]');

    if (summaryElement || keyElement) {
      e.preventDefault();

      try {
        const issue = await jiraAPI.getCurrentIssue();
        showContextMenu(e.clientX, e.clientY, issue.id, jiraAPI, apisClient);
      } catch (error) {
        logError('Failed to get issue context', error);
      }
    }
  });
}

/**
 * Handle context menu event
 */
function handleContextMenu(e, issueKey, jiraAPI, apisClient) {
  e.preventDefault();
  showContextMenu(e.clientX, e.clientY, issueKey, jiraAPI, apisClient);
}

/**
 * Display context menu at position
 */
function showContextMenu(x, y, issueKey, jiraAPI, apisClient) {
  // Remove existing menu
  const existing = document.getElementById('apos-context-menu');
  if (existing) {
    existing.remove();
  }

  // Create menu
  const menu = document.createElement('div');
  menu.id = 'apos-context-menu';
  menu.className = 'apos-context-menu';
  menu.style.top = `${y}px`;
  menu.style.left = `${x}px`;

  menu.innerHTML = `
    <div class="apos-menu-item" data-action="link-okr">
      <span class="apos-menu-icon">🔗</span>
      <span class="apos-menu-text">Link to OKR</span>
    </div>
    <div class="apos-menu-item" data-action="view-score">
      <span class="apos-menu-icon">📊</span>
      <span class="apos-menu-text">View Trust Score</span>
    </div>
    <div class="apos-menu-separator"></div>
    <div class="apos-menu-item" data-action="mark-strategic">
      <span class="apos-menu-icon">⭐</span>
      <span class="apos-menu-text">Mark as Strategic</span>
    </div>
  `;

  document.body.appendChild(menu);

  // Handle menu item clicks
  menu.querySelectorAll('.apos-menu-item').forEach(item => {
    item.addEventListener('click', async () => {
      const action = item.getAttribute('data-action');
      await handleMenuAction(action, issueKey, jiraAPI, apisClient);
      menu.remove();
    });
  });

  // Close menu on click outside
  document.addEventListener('click', () => {
    const m = document.getElementById('apos-context-menu');
    if (m) m.remove();
  }, { once: true });
}

/**
 * Handle context menu actions
 */
async function handleMenuAction(action, issueKey, jiraAPI, apisClient) {
  try {
    switch (action) {
      case 'link-okr':
        await handleLinkOKR(issueKey, apisClient);
        break;

      case 'view-score':
        await handleViewScore(issueKey, apisClient);
        break;

      case 'mark-strategic':
        await handleMarkStrategic(issueKey, jiraAPI);
        break;

      default:
        console.warn('Unknown action:', action);
    }
  } catch (error) {
    logError(`Failed to handle action: ${action}`, error);
  }
}

/**
 * Action: Link to OKR
 */
async function handleLinkOKR(issueKey, apisClient) {
  log(`🔗 Link to OKR: ${issueKey}`);

  // Get current project
  const issue = await jiraAPI.getCurrentIssue();
  const projectKey = issue.project_id;

  // Fetch OKRs
  const okrsData = await apisClient.getOKRs(projectKey);
  const okrs = okrsData.data || [];

  if (okrs.length === 0) {
    alert('No OKRs found for this project');
    return;
  }

  // Show OKR selection dialog
  const selectedOKR = await showOKRSelectionDialog(okrs);

  if (selectedOKR) {
    // Link task to OKR
    await apisClient.linkTaskToOKR(issueKey, selectedOKR.id, 1.0);
    alert(`✅ Linked ${issueKey} to ${selectedOKR.name}`);
  }
}

/**
 * Action: View Trust Score
 */
async function handleViewScore(issueKey, apisClient) {
  log(`📊 View Trust Score: ${issueKey}`);

  // Get current project
  const issue = await jiraAPI.getCurrentIssue();
  const projectKey = issue.project_id;

  // Fetch trust score
  const scoreData = await apisClient.getTrustScore(projectKey);

  const message = `
📊 Trust Score: ${(scoreData.score * 100).toFixed(1)}%

Components:
  • Coverage: ${(scoreData.components.coverage * 100).toFixed(1)}%
  • Quality: ${(scoreData.components.quality * 100).toFixed(1)}%
  • Consistency: ${(scoreData.components.consistency * 100).toFixed(1)}%

Issues:
${scoreData.issues.map(i => `  • ${i}`).join('\n')}
  `;

  alert(message);
}

/**
 * Action: Mark as Strategic
 */
async function handleMarkStrategic(issueKey, jiraAPI) {
  log(`⭐ Mark as Strategic: ${issueKey}`);

  // Update Jira issue (add label or custom field)
  await jiraAPI.updateIssueField(issueKey, 'labels', ['apos-strategic']);

  alert(`✅ Marked ${issueKey} as strategic`);
}

/**
 * Show OKR selection dialog
 */
function showOKRSelectionDialog(okrs) {
  return new Promise((resolve) => {
    // Create simple HTML dialog
    const dialog = document.createElement('div');
    dialog.className = 'apos-okr-dialog';

    let options = '<option value="">-- Select OKR --</option>';
    okrs.forEach((okr, idx) => {
      options += `<option value="${idx}">${okr.name}</option>`;
    });

    dialog.innerHTML = `
      <div class="apos-dialog-overlay">
        <div class="apos-dialog-box">
          <h3>Select OKR</h3>
          <select id="apos-okr-select" autofocus>
            ${options}
          </select>
          <div class="apos-dialog-buttons">
            <button id="apos-cancel-btn">Cancel</button>
            <button id="apos-select-btn" disabled>Select</button>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(dialog);

    const select = dialog.querySelector('#apos-okr-select');
    const selectBtn = dialog.querySelector('#apos-select-btn');
    const cancelBtn = dialog.querySelector('#apos-cancel-btn');

    select.addEventListener('change', () => {
      selectBtn.disabled = !select.value;
    });

    selectBtn.addEventListener('click', () => {
      const idx = parseInt(select.value);
      dialog.remove();
      resolve(okrs[idx]);
    });

    cancelBtn.addEventListener('click', () => {
      dialog.remove();
      resolve(null);
    });
  });
}

export { setupContextMenu };
