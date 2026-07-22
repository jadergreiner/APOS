/**
 * APOS Jira Plugin - Main Entry Point
 *
 * Responsibilities:
 * 1. Initialize Jira App
 * 2. Setup OAuth with backend API
 * 3. Wire up modules (sidebar, webhooks, context menu)
 * 4. Error handling + logging
 */

import JiraAPI from './api/JiraAPI';
import APISClient from './api/APISClient';
import APIService from './services/APIService';
import { setupSidebar } from './modules/sidebar';
import { setupWebhooks } from './modules/webhooks';
import { setupContextMenu } from './modules/contextMenu';
import { log, logError } from './utils/logger';

// Configuration
const CONFIG = {
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1',
  CACHE_TTL: 300, // 5 minutes
  WEBHOOK_TIMEOUT: 5000,
};

class APOSJiraPlugin {
  constructor() {
    this.jiraAPI = null;
    this.apisClient = null;
    this.apiService = null;
    this.initialized = false;
  }

  /**
   * Initialize plugin - called on page load
   */
  async init() {
    try {
      log('🚀 APOS Plugin initializing...');

      // 1. Setup Jira API wrapper
      this.jiraAPI = new JiraAPI();
      await this.jiraAPI.authenticate();
      log('✅ Jira API authenticated');

      // 2. Setup APOS backend client
      this.apisClient = new APISClient(CONFIG.API_BASE_URL);
      const health = await this.apisClient.health();
      log(`✅ Backend API connected (${health.status})`);

      // 3. Create unified API service (orchestrates all calls)
      this.apiService = new APIService(this.jiraAPI, this.apisClient);
      log('✅ API Service initialized');

      // 4. Setup UI modules with API service
      await setupSidebar(this.apiService);
      log('✅ Sidebar initialized');

      await setupContextMenu(this.apiService);
      log('✅ Context menu initialized');

      // 5. Setup webhook receivers (backend → plugin)
      await setupWebhooks(this.apiService);
      log('✅ Webhooks initialized');

      this.initialized = true;
      log('🎉 APOS Plugin ready!');

    } catch (error) {
      logError('Plugin initialization failed', error);
      this.handleInitError(error);
    }
  }

  /**
   * Error recovery
   */
  handleInitError(error) {
    const message = error.response?.data?.error || error.message;

    if (error.response?.status === 401) {
      // Re-auth needed
      console.warn('Re-authenticating...');
      this.jiraAPI.reauthenticate();
    } else if (error.response?.status === 503) {
      // Backend down
      console.warn('Backend unavailable. Retrying in 10s...');
      setTimeout(() => this.init(), 10000);
    } else {
      console.error('Unrecoverable error:', message);
    }
  }

  /**
   * Get current issue context
   */
  async getIssueContext() {
    if (!this.initialized) {
      throw new Error('Plugin not initialized');
    }
    return this.apiService.getCurrentIssue();
  }

  /**
   * Sync orphan features from backend
   */
  async syncOrphans(projectId) {
    if (!this.initialized) {
      throw new Error('Plugin not initialized');
    }

    try {
      const orphans = await this.apiService.getOrphans(projectId);
      log(`📊 Synced ${orphans.data.length} orphans`);
      return orphans;
    } catch (error) {
      logError('Failed to sync orphans', error);
      throw error;
    }
  }

  /**
   * Link task to OKR
   */
  async linkTaskToOKR(taskId, okrId) {
    if (!this.initialized) {
      throw new Error('Plugin not initialized');
    }

    try {
      const relationship = await this.apiService.linkTaskToOKR(taskId, okrId);
      log(`🔗 Linked ${taskId} → ${okrId}`);
      return relationship;
    } catch (error) {
      logError('Failed to link task', error);
      throw error;
    }
  }

  /**
   * Get trust score for project
   */
  async getTrustScore(projectId) {
    if (!this.initialized) {
      throw new Error('Plugin not initialized');
    }

    try {
      const score = await this.apiService.getTrustScore(projectId);
      log(`📈 Trust score: ${(score.score * 100).toFixed(1)}%`);
      return score;
    } catch (error) {
      logError('Failed to get trust score', error);
      throw error;
    }
  }

  /**
   * Get cached instance (for debugging)
   */
  getAPIService() {
    return this.apiService;
  }
}

// Global singleton
let plugin = null;

/**
 * Get plugin instance (lazy init)
 */
export function getPlugin() {
  if (!plugin) {
    plugin = new APOSJiraPlugin();
    plugin.init();
  }
  return plugin;
}

/**
 * Entry point - called by Jira on page load
 */
if (typeof window !== 'undefined') {
  window.APOSPlugin = getPlugin();
  console.log('APOS Plugin loaded');
}

export default getPlugin;
