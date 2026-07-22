/**
 * APOS API Client
 *
 * Handles all HTTP calls to backend:
 * - GET /tasks, /okrs, /relationships, /trust-score, /orphans
 * - POST /relationships (link task to OKR)
 *
 * References: SPEC.md Seção 4.2 + API_DESIGN.md
 */

import axios from 'axios';

class APISClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to all requests
    this.client.interceptors.request.use(config => {
      const token = this._getAuthToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle errors
    this.client.interceptors.response.use(
      response => response,
      error => this._handleError(error)
    );
  }

  /**
   * Health check - verify backend is running
   */
  async health() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Backend API unreachable');
    }
  }

  /**
   * GET /tasks - List all tasks with pagination
   *
   * @param {string} projectId - e.g. "R0"
   * @param {object} options - { status: "in_progress", page: 1, limit: 50 }
   * @returns {Promise<Array>} Tasks with id, title, okr_id, orphan, trust_score
   */
  async getTasks(projectId, options = {}) {
    const params = {
      project_id: projectId,
      page: options.page || 1,
      limit: options.limit || 50,
      ...options,
    };

    const response = await this.client.get('/tasks', { params });
    return response.data;
  }

  /**
   * GET /okrs - List all OKRs
   *
   * @param {string} projectId
   * @returns {Promise<Array>} OKRs with id, name, key_results, target_date
   */
  async getOKRs(projectId) {
    const response = await this.client.get('/okrs', {
      params: { project_id: projectId },
    });
    return response.data;
  }

  /**
   * GET /relationships - List Task→OKR mappings
   *
   * @param {string} projectId
   * @returns {Promise<Array>} Relationships with task_id, okr_id, confidence
   */
  async getRelationships(projectId) {
    const response = await this.client.get('/relationships', {
      params: { project_id: projectId },
    });
    return response.data;
  }

  /**
   * POST /relationships - Link task to OKR
   *
   * @param {string} taskId - e.g. "JIRA-123"
   * @param {string} okrId - e.g. "OKR-2026-Q3-001"
   * @param {number} confidence - 0.0-1.0 (1.0 = manual, 0.7+ = auto)
   * @returns {Promise<Object>} Created relationship
   */
  async linkTaskToOKR(taskId, okrId, confidence = 1.0) {
    const response = await this.client.post('/relationships', {
      task_id: taskId,
      okr_id: okrId,
      confidence,
    });
    return response.data;
  }

  /**
   * GET /trust-score - Calculate overall trust score
   *
   * @param {string} projectId
   * @returns {Promise<Object>} Score with value (0.0-1.0), components, issues
   */
  async getTrustScore(projectId) {
    const response = await this.client.get('/trust-score', {
      params: { project_id: projectId },
    });
    return response.data;
  }

  /**
   * GET /orphans - List features without OKR
   *
   * @param {string} projectId
   * @returns {Promise<Object>} Orphans with task_id, title, risk_level, suggestion
   */
  async getOrphans(projectId) {
    const response = await this.client.get('/orphans', {
      params: { project_id: projectId },
    });
    return response.data;
  }

  /**
   * Internal: Get auth token from storage
   */
  _getAuthToken() {
    // In real implementation, retrieve from localStorage or sessionStorage
    // For now, using Jira OAuth token
    return localStorage.getItem('apos_api_token') || null;
  }

  /**
   * Internal: Handle API errors
   */
  _handleError(error) {
    const status = error.response?.status;
    const message = error.response?.data?.error || error.message;

    switch (status) {
      case 400:
        console.error('❌ Bad request:', message);
        break;
      case 401:
        console.error('❌ Unauthorized - re-authenticate');
        this._clearAuth();
        break;
      case 404:
        console.error('❌ Resource not found:', message);
        break;
      case 429:
        console.warn('⏳ Rate limited - retrying...');
        break;
      case 500:
        console.error('❌ Server error:', message);
        break;
      default:
        console.error('❌ API error:', message);
    }

    return Promise.reject(error);
  }

  /**
   * Internal: Clear auth on 401
   */
  _clearAuth() {
    localStorage.removeItem('apos_api_token');
    // Redirect to login or trigger re-auth
  }
}

export default APISClient;
