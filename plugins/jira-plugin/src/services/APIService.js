/**
 * API Service Layer
 *
 * Orquestrates calls to both Jira API and APOS backend API with:
 * - Intelligent caching (TTL-based)
 * - Retry logic (exponential backoff)
 * - Error handling + logging
 * - Request deduplication
 *
 * This is the single source of truth for all external API calls.
 * Referenced by: sidebar.js, contextMenu.js, webhooks.js
 */

import { log, logWarn, logError } from '../utils/logger';

const CACHE_CONFIG = {
  ORPHANS_TTL: 300000, // 5 min
  OKRS_TTL: 600000, // 10 min
  TRUST_SCORE_TTL: 120000, // 2 min
  RELATIONSHIPS_TTL: 300000, // 5 min
};

const RETRY_CONFIG = {
  MAX_RETRIES: 3,
  INITIAL_DELAY: 1000, // 1s
  MAX_DELAY: 10000, // 10s
  BACKOFF_FACTOR: 2,
};

class APIService {
  constructor(jiraAPI, apisClient) {
    this.jiraAPI = jiraAPI;
    this.apisClient = apisClient;
    this.cache = new Map();
    this.pendingRequests = new Map(); // For deduplication
  }

  /**
   * Get orphans with caching
   */
  async getOrphans(projectId) {
    const cacheKey = `orphans:${projectId}`;
    return this._getCachedOrFetch(cacheKey, CACHE_CONFIG.ORPHANS_TTL, async () => {
      log(`📥 Fetching orphans for ${projectId}...`);
      return this.apisClient.getOrphans(projectId);
    });
  }

  /**
   * Get OKRs with caching
   */
  async getOKRs(projectId) {
    const cacheKey = `okrs:${projectId}`;
    return this._getCachedOrFetch(cacheKey, CACHE_CONFIG.OKRS_TTL, async () => {
      log(`📥 Fetching OKRs for ${projectId}...`);
      return this.apisClient.getOKRs(projectId);
    });
  }

  /**
   * Get trust score with caching
   */
  async getTrustScore(projectId) {
    const cacheKey = `trust-score:${projectId}`;
    return this._getCachedOrFetch(cacheKey, CACHE_CONFIG.TRUST_SCORE_TTL, async () => {
      log(`📥 Fetching trust score for ${projectId}...`);
      return this.apisClient.getTrustScore(projectId);
    });
  }

  /**
   * Get relationships (cache longer, refresh on link)
   */
  async getRelationships(projectId) {
    const cacheKey = `relationships:${projectId}`;
    return this._getCachedOrFetch(cacheKey, CACHE_CONFIG.RELATIONSHIPS_TTL, async () => {
      log(`📥 Fetching relationships for ${projectId}...`);
      return this.apisClient.getRelationships(projectId);
    });
  }

  /**
   * Link task to OKR (invalidates caches on success)
   */
  async linkTaskToOKR(taskId, okrId, confidence = 1.0) {
    try {
      log(`🔗 Linking ${taskId} → ${okrId}...`);

      // Call backend API with retry
      const relationship = await this._retryWithBackoff(async () => {
        return this.apisClient.linkTaskToOKR(taskId, okrId, confidence);
      });

      // Update Jira issue (add custom field)
      await this._retryWithBackoff(async () => {
        return this.jiraAPI.updateIssueOKRField(taskId, okrId);
      });

      // Invalidate caches (orphans, relationships changed)
      this._invalidateCache('orphans:*');
      this._invalidateCache('relationships:*');
      this._invalidateCache('trust-score:*');

      log(`✅ Linked ${taskId} → ${okrId}`);
      return relationship;
    } catch (error) {
      logError('Failed to link task to OKR', error);
      throw error;
    }
  }

  /**
   * Get current issue context
   */
  async getCurrentIssue() {
    try {
      return await this._retryWithBackoff(async () => {
        return this.jiraAPI.getCurrentIssue();
      });
    } catch (error) {
      logError('Failed to get current issue', error);
      throw error;
    }
  }

  /**
   * Update issue field (for marking as strategic, etc)
   */
  async updateIssueField(issueKey, fieldName, value) {
    try {
      log(`📝 Updating ${issueKey}.${fieldName}...`);
      return await this._retryWithBackoff(async () => {
        return this.jiraAPI.updateIssueField(issueKey, fieldName, value);
      });
    } catch (error) {
      logError(`Failed to update ${issueKey}.${fieldName}`, error);
      throw error;
    }
  }

  /**
   * Health check
   */
  async healthCheck() {
    try {
      return await this._retryWithBackoff(async () => {
        return this.apisClient.health();
      });
    } catch (error) {
      logError('Health check failed', error);
      return { status: 'error' };
    }
  }

  /**
   * ========================================
   * INTERNAL: Caching + Retry Logic
   * ========================================
   */

  /**
   * Get from cache OR fetch + cache
   */
  async _getCachedOrFetch(key, ttl, fetchFn) {
    // Check cache
    const cached = this.cache.get(key);
    if (cached && Date.now() < cached.expiresAt) {
      log(`✓ Cache hit: ${key}`);
      return cached.value;
    }

    // Check if request already pending (dedup)
    if (this.pendingRequests.has(key)) {
      log(`✓ Request in flight, reusing: ${key}`);
      return this.pendingRequests.get(key);
    }

    // Fetch with retry
    const promise = this._retryWithBackoff(fetchFn);
    this.pendingRequests.set(key, promise);

    try {
      const value = await promise;
      this.cache.set(key, {
        value,
        expiresAt: Date.now() + ttl,
      });
      log(`✓ Cached: ${key} (TTL: ${ttl / 1000}s)`);
      return value;
    } finally {
      this.pendingRequests.delete(key);
    }
  }

  /**
   * Retry with exponential backoff
   */
  async _retryWithBackoff(fn, attempt = 0) {
    try {
      return await fn();
    } catch (error) {
      if (attempt < RETRY_CONFIG.MAX_RETRIES) {
        const delay = Math.min(
          RETRY_CONFIG.INITIAL_DELAY * Math.pow(RETRY_CONFIG.BACKOFF_FACTOR, attempt),
          RETRY_CONFIG.MAX_DELAY
        );

        const isRetryable = this._isRetryable(error);
        if (isRetryable) {
          logWarn(`Retry ${attempt + 1}/${RETRY_CONFIG.MAX_RETRIES} in ${delay}ms`);
          await this._sleep(delay);
          return this._retryWithBackoff(fn, attempt + 1);
        }
      }

      throw error;
    }
  }

  /**
   * Check if error is retryable
   */
  _isRetryable(error) {
    const status = error.response?.status;
    // Retry on: 429 (rate limit), 503 (service unavailable), 504 (gateway timeout), network errors
    return !status || status === 429 || status === 503 || status === 504;
  }

  /**
   * Invalidate cache by pattern
   */
  _invalidateCache(pattern) {
    if (pattern.endsWith('*')) {
      const prefix = pattern.slice(0, -1);
      for (const key of this.cache.keys()) {
        if (key.startsWith(prefix)) {
          this.cache.delete(key);
          log(`🗑️  Invalidated: ${key}`);
        }
      }
    } else {
      this.cache.delete(pattern);
      log(`🗑️  Invalidated: ${pattern}`);
    }
  }

  /**
   * Sleep utility
   */
  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Clear all caches (debugging)
   */
  clearAllCaches() {
    this.cache.clear();
    this.pendingRequests.clear();
    log('🗑️  All caches cleared');
  }
}

export default APIService;
