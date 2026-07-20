/**
 * Jira API Wrapper
 *
 * Handles:
 * - OAuth2 authentication
 * - Issue queries (GET /issues, etc)
 * - Custom field updates
 * - Issue status changes
 */

import axios from 'axios';

class JiraAPI {
  constructor() {
    this.baseUrl = window.location.origin; // Jira base URL
    this.accessToken = null;
    this.cloudId = null;
  }

  /**
   * OAuth2 authentication
   */
  async authenticate() {
    try {
      // Get access token from Jira OAuth flow
      const response = await axios.get('/plugins/servlet/oauth/authorize', {
        params: {
          client_id: process.env.REACT_APP_JIRA_CLIENT_ID,
          redirect_uri: `${window.location.origin}/plugins/jira-plugin/callback`,
          response_type: 'code',
          scope: 'read:jira-work write:jira-work read:jira-user',
        },
      });

      this.accessToken = response.data.access_token;
      this.cloudId = response.data.cloud_id;

      return true;
    } catch (error) {
      console.error('Jira authentication failed:', error);
      throw error;
    }
  }

  /**
   * Re-authenticate if token expired
   */
  async reauthenticate() {
    console.warn('Token expired, re-authenticating...');
    this.accessToken = null;
    return this.authenticate();
  }

  /**
   * Get all issues in current project
   *
   * @param {string} projectKey - e.g. "R0"
   * @param {object} options - { status: "in_progress", assignee: "user@..." }
   * @returns {Promise<Array>} Issues with id, key, summary, status, etc
   */
  async getIssues(projectKey, options = {}) {
    const jql = this._buildJQL(projectKey, options);

    const response = await this._request('GET', '/rest/api/3/issues/search', {
      jql,
      fields: ['key', 'summary', 'status', 'assignee', 'created', 'updated'],
      maxResults: 100,
    });

    return response.data.issues.map(issue => ({
      id: issue.key, // JIRA-123
      title: issue.fields.summary,
      status: issue.fields.status.name.toLowerCase(),
      assignee: issue.fields.assignee?.displayName,
      created_at: issue.fields.created,
      updated_at: issue.fields.updated,
    }));
  }

  /**
   * Get single issue details
   */
  async getIssue(issueKey) {
    const response = await this._request('GET', `/rest/api/3/issues/${issueKey}`, {
      fields: ['key', 'summary', 'description', 'status', 'project'],
    });

    return {
      id: response.data.key,
      title: response.data.fields.summary,
      description: response.data.fields.description,
      status: response.data.fields.status.name.toLowerCase(),
      project_id: response.data.fields.project.key,
    };
  }

  /**
   * Get current issue from browser context
   */
  async getCurrentIssue() {
    // Extract from URL or Jira global context
    const url = new URL(window.location);
    const issueKey = this._parseIssueKeyFromURL(url.pathname);

    if (issueKey) {
      return this.getIssue(issueKey);
    }

    throw new Error('No issue in context');
  }

  /**
   * Update issue's OKR custom field
   *
   * @param {string} issueKey - e.g. "JIRA-123"
   * @param {string} okrId - e.g. "OKR-2026-Q3-001"
   */
  async updateIssueOKRField(issueKey, okrId) {
    // Get custom field ID for OKR
    const customFieldId = await this._getCustomFieldId('apos_okr_id');

    return this._request('PUT', `/rest/api/3/issues/${issueKey}`, {
      fields: {
        [customFieldId]: okrId,
      },
    });
  }

  /**
   * Create a new issue
   */
  async createIssue(projectKey, summary, description = '') {
    const response = await this._request('POST', '/rest/api/3/issues', {
      fields: {
        project: { key: projectKey },
        summary,
        description,
        issuetype: { name: 'Task' },
      },
    });

    return {
      id: response.data.key,
      title: summary,
    };
  }

  /**
   * Internal: Build JQL query
   */
  _buildJQL(projectKey, options) {
    let jql = `project = "${projectKey}"`;

    if (options.status) {
      jql += ` AND status = "${options.status}"`;
    }
    if (options.assignee) {
      jql += ` AND assignee = "${options.assignee}"`;
    }

    return jql;
  }

  /**
   * Internal: Parse issue key from URL
   */
  _parseIssueKeyFromURL(pathname) {
    const match = pathname.match(/browse\/([A-Z]+-\d+)/);
    return match ? match[1] : null;
  }

  /**
   * Internal: Get custom field ID by name
   */
  async _getCustomFieldId(fieldName) {
    const response = await this._request('GET', '/rest/api/3/fields');
    const field = response.data.find(f => f.name === fieldName);
    return field?.id || null;
  }

  /**
   * Internal: Make HTTP request to Jira API
   */
  async _request(method, path, data = null) {
    const headers = {
      'Authorization': `Bearer ${this.accessToken}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    };

    try {
      const response = await axios({
        method,
        url: `${this.baseUrl}${path}`,
        data,
        headers,
        timeout: 5000,
      });

      return response;
    } catch (error) {
      if (error.response?.status === 401) {
        // Token expired
        await this.reauthenticate();
        return this._request(method, path, data);
      }

      throw error;
    }
  }
}

export default JiraAPI;
