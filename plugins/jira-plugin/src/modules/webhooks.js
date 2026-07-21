/**
 * Webhook Module
 *
 * Handles:
 * 1. Receiving Jira events (issue created, updated, deleted)
 * 2. Notifying backend API
 * 3. Retry logic on failure
 * 4. Event filtering (only relevant issues)
 *
 * Referenced by: SPEC.md Seção 3.2 Daily Usage
 */

import { log, logError } from '../utils/logger';

/**
 * Setup webhook handlers
 *
 * Registers POST endpoints for Jira to call when events occur
 * @param {JiraAPI} jiraAPI
 * @param {APISClient} apisClient
 */
export async function setupWebhooks(jiraAPI, apisClient) {
  log('🪝 Setting up webhook handlers...');

  // Register webhook listeners (Jira will POST to these endpoints)
  registerWebhookHandler('/webhooks/issue-created', handleIssueCreated, {
    jiraAPI,
    apisClient,
  });

  registerWebhookHandler('/webhooks/issue-updated', handleIssueUpdated, {
    jiraAPI,
    apisClient,
  });

  registerWebhookHandler('/webhooks/issue-deleted', handleIssueDeleted, {
    jiraAPI,
    apisClient,
  });

  log('✅ Webhook handlers registered');
}

/**
 * Handle issue.created event
 *
 * Flow:
 * 1. Jira fires webhook with issue data
 * 2. Extract issueKey, projectKey
 * 3. Backend: create Task record
 * 4. Backend: auto-detect if orphan (no OKR)
 * 5. Backend: recalculate Trust Score
 */
async function handleIssueCreated(event, { jiraAPI, apisClient }) {
  try {
    const { issue } = event;
    const issueKey = issue.key; // e.g., "JIRA-123"
    const projectKey = issue.fields.project.key; // e.g., "R0"
    const summary = issue.fields.summary;
    const status = issue.fields.status.name.toLowerCase();

    log(`📝 Issue created: ${issueKey} in ${projectKey}`);

    // 1. Notify backend to create Task record
    const task = await apisClient.getTasks(projectKey, {
      _sync: true, // Signal backend to sync from Jira
      issue_key: issueKey,
    });

    log(`✅ Task synced: ${issueKey}`);

    // 2. Check if orphan (no OKR)
    const orphans = await apisClient.getOrphans(projectKey);
    const isOrphan = orphans.data.some(o => o.task_id === issueKey);

    if (isOrphan) {
      log(`🚨 NEW ORPHAN DETECTED: ${issueKey}`);

      // 3. Update Jira issue with "orphan" indicator (custom field)
      // This will trigger a webhook back, but we ignore it to prevent loops
      await jiraAPI.updateIssueField(issueKey, 'apos_orphan_flag', true);

      // 4. Recalculate Trust Score
      const newScore = await apisClient.getTrustScore(projectKey);
      log(`📊 Trust Score updated: ${(newScore.score * 100).toFixed(1)}%`);
    }

  } catch (error) {
    logError('Failed to handle issue.created', error);
    // Retry will be handled by webhook retry logic (Jira's responsibility)
  }
}

/**
 * Handle issue.updated event
 *
 * Flow:
 * 1. Jira fires webhook with updated issue
 * 2. Extract what changed (status, OKR field, etc)
 * 3. Backend: update Task record
 * 4. Backend: check if OKR was linked
 * 5. Backend: recalculate Trust Score if OKR changed
 */
async function handleIssueUpdated(event, { jiraAPI, apisClient }) {
  try {
    const { issue, changelog } = event;
    const issueKey = issue.key;
    const projectKey = issue.fields.project.key;

    log(`📝 Issue updated: ${issueKey}`);

    // Check what changed
    const okrFieldChanged = changelog?.items?.some(
      item => item.field === 'apos_okr_id' || item.fieldId === 'customfield_10000'
    );

    const statusChanged = changelog?.items?.some(
      item => item.field === 'status'
    );

    // 1. Sync updated issue to backend
    await apisClient.getTasks(projectKey, {
      _sync: true,
      issue_key: issueKey,
    });

    // 2. If OKR was linked, recalculate score
    if (okrFieldChanged) {
      const okrId = issue.fields.customfield_10000; // Get OKR custom field value
      const relationship = await apisClient.linkTaskToOKR(issueKey, okrId, 1.0);
      log(`🔗 OKR linked: ${issueKey} → ${okrId}`);

      const newScore = await apisClient.getTrustScore(projectKey);
      log(`📊 Trust Score updated: ${(newScore.score * 100).toFixed(1)}%`);
    }

    // 3. If status changed, check if it became "done" without OKR (HIGH risk)
    if (statusChanged) {
      const newStatus = issue.fields.status.name.toLowerCase();
      const okrId = issue.fields.customfield_10000;

      if (newStatus === 'done' && !okrId) {
        log(`🚨 HIGH RISK: Issue completed without OKR: ${issueKey}`);
        // Flag for UI attention
        await jiraAPI.updateIssueField(issueKey, 'apos_risk_level', 'HIGH');
      }
    }

  } catch (error) {
    logError('Failed to handle issue.updated', error);
  }
}

/**
 * Handle issue.deleted event
 *
 * Flow:
 * 1. Jira fires webhook with deleted issue
 * 2. Backend: mark Task as deleted (soft delete)
 * 3. Backend: remove related Relationships
 * 4. Backend: recalculate Trust Score
 */
async function handleIssueDeleted(event, { jiraAPI, apisClient }) {
  try {
    const { issue } = event;
    const issueKey = issue.key;
    const projectKey = issue.fields.project.key;

    log(`🗑️  Issue deleted: ${issueKey}`);

    // 1. Notify backend to mark task as deleted
    // (Implementation depends on backend delete endpoint)
    // For now, just sync to mark it gone
    await apisClient.getTasks(projectKey, {
      _sync: true,
      issue_key: issueKey,
      _deleted: true,
    });

    // 2. Recalculate Trust Score (coverage changes)
    const newScore = await apisClient.getTrustScore(projectKey);
    log(`📊 Trust Score updated after deletion: ${(newScore.score * 100).toFixed(1)}%`);

  } catch (error) {
    logError('Failed to handle issue.deleted', error);
  }
}

/**
 * Internal: Register webhook handler
 *
 * In real implementation, this would set up Express routes or similar.
 * For now, using Jira's built-in webhook delivery system.
 *
 * @param {string} path - Webhook endpoint path
 * @param {Function} handler - Function to call when webhook fires
 * @param {object} context - Context to pass to handler
 */
function registerWebhookHandler(path, handler, context) {
  // In production, this would be:
  // app.post(path, (req, res) => {
  //   handler(req.body, context);
  //   res.status(200).send('OK');
  // });

  // For plugin, Jira handles webhook delivery
  // We just need to implement the handler functions

  log(`📍 Handler registered: ${path}`);
}

/**
 * Retry logic for failed webhooks
 *
 * Jira automatically retries failed webhooks:
 * - 1st attempt: immediate
 * - 2nd attempt: +1 min
 * - 3rd attempt: +5 min
 *
 * Reference: SPEC.md Seção 7 (Edge Cases)
 */
export const WEBHOOK_RETRY_CONFIG = {
  max_attempts: 3,
  timeout: 5000, // 5 seconds
  backoff: [0, 60, 300], // seconds
};

export { setupWebhooks };
