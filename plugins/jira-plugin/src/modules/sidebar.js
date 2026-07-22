/**
 * Sidebar Module
 *
 * Displays:
 * 1. List of orphaned features (without OKR)
 * 2. Trust Score for project
 * 3. Quick link to modal "Link OKR"
 * 4. Risk levels (HIGH/MED/LOW)
 *
 * Referenced by: SPEC.md Seção 4.1 (Plugin Jira Sidebar)
 */

import React, { useEffect, useState } from 'react';
import { log, logError } from '../utils/logger';
import './sidebar.css';

/**
 * Setup sidebar module
 *
 * Called on plugin init to render sidebar in Jira UI
 * @param {APIService} apiService - Unified API service
 */
export async function setupSidebar(apiService) {
  log('📊 Setting up Sidebar module...');

  // Mount React component to Jira sidebar DOM
  const sidebarContainer = document.getElementById('apos-sidebar');

  if (!sidebarContainer) {
    console.warn('Sidebar container not found');
    return;
  }

  // Render Sidebar component
  const root = ReactDOM.createRoot(sidebarContainer);
  root.render(<Sidebar apiService={apiService} />);

  log('✅ Sidebar rendered');
}

/**
 * Sidebar React Component
 *
 * Main UI for APOS plugin in Jira
 */
function Sidebar({ apiService }) {
  const [orphans, setOrphans] = useState([]);
  const [trustScore, setTrustScore] = useState(null);
  const [loading, setLoading] = useState(true);
  const [projectKey, setProjectKey] = useState(null);
  const [selectedOrphan, setSelectedOrphan] = useState(null);
  const [showModal, setShowModal] = useState(false);

  /**
   * Load data on mount
   */
  useEffect(() => {
    loadData();

    // Refresh every 30 seconds
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  /**
   * Fetch orphans and trust score
   */
  async function loadData() {
    try {
      setLoading(true);

      // Get current project
      const currentIssue = await apiService.getCurrentIssue();
      const project = currentIssue.project_id;
      setProjectKey(project);

      // Fetch orphans
      const orphanData = await apiService.getOrphans(project);
      setOrphans(orphanData.data || []);

      // Fetch trust score
      const scoreData = await apiService.getTrustScore(project);
      setTrustScore(scoreData.score);

      log(`✅ Sidebar data loaded (${orphanData.data.length} orphans, score ${(scoreData.score * 100).toFixed(1)}%)`);
    } catch (error) {
      logError('Failed to load sidebar data', error);
    } finally {
      setLoading(false);
    }
  }

  /**
   * Handle orphan click - show link modal
   */
  function handleOrphanClick(orphan) {
    setSelectedOrphan(orphan);
    setShowModal(true);
  }

  /**
   * Handle link OKR action
   */
  async function handleLinkOKR(okrId) {
    try {
      await apiService.linkTaskToOKR(selectedOrphan.task_id, okrId);
      log(`✅ Linked ${selectedOrphan.task_id} → ${okrId}`);

      // Refresh sidebar data
      await loadData();

      // Close modal
      setShowModal(false);
      setSelectedOrphan(null);
    } catch (error) {
      logError('Failed to link OKR', error);
    }
  }

  // UI: Trust Score Header
  const scorePercentage = trustScore ? (trustScore * 100).toFixed(1) : '—';
  const scoreClass = trustScore ? (trustScore >= 0.8 ? 'high' : trustScore >= 0.6 ? 'medium' : 'low') : '';

  return (
    <div className="apos-sidebar">
      {/* Header: Trust Score */}
      <div className="apos-header">
        <h2>🔗 APOS</h2>
        <div className={`apos-score ${scoreClass}`}>
          <span className="score-label">Trust Score</span>
          <span className="score-value">{scorePercentage}%</span>
        </div>
      </div>

      {/* Loading State */}
      {loading && <div className="apos-loading">⏳ Loading...</div>}

      {/* Orphans List */}
      {!loading && (
        <>
          <div className="apos-section">
            <h3>🚨 Orphaned Features</h3>
            <span className="apos-count">{orphans.length} found</span>

            {orphans.length === 0 ? (
              <div className="apos-empty">✅ All features are linked to OKRs!</div>
            ) : (
              <ul className="apos-orphan-list">
                {orphans.map(orphan => (
                  <li
                    key={orphan.task_id}
                    className={`apos-orphan apos-risk-${orphan.risk_level.toLowerCase()}`}
                    onClick={() => handleOrphanClick(orphan)}
                  >
                    <div className="orphan-header">
                      <span className="orphan-id">{orphan.task_id}</span>
                      <span className={`orphan-risk apos-risk-${orphan.risk_level.toLowerCase()}`}>
                        {orphan.risk_level}
                      </span>
                    </div>
                    <div className="orphan-title">{orphan.title}</div>
                    <div className="orphan-status">{orphan.status}</div>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Link Modal */}
          {showModal && selectedOrphan && (
            <LinkOKRModal
              orphan={selectedOrphan}
              onLink={handleLinkOKR}
              onClose={() => {
                setShowModal(false);
                setSelectedOrphan(null);
              }}
              apiService={apiService}
            />
          )}

          {/* Footer: Info */}
          <div className="apos-footer">
            <p className="apos-hint">💡 Click orphan to link to OKR</p>
            <p className="apos-help">Need help? <a href="#" target="_blank">Docs</a></p>
          </div>
        </>
      )}
    </div>
  );
}

/**
 * Link OKR Modal Component
 *
 * Dialog to select which OKR to link the orphan task to
 */
function LinkOKRModal({ orphan, onLink, onClose, apiService }) {
  const [okrs, setOkrs] = useState([]);
  const [selectedOKR, setSelectedOKR] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOKRs();
  }, []);

  async function loadOKRs() {
    try {
      const data = await apiService.getOKRs(orphan.project_id);
      setOkrs(data.data || []);
    } catch (error) {
      logError('Failed to load OKRs', error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="apos-modal-overlay" onClick={onClose}>
      <div className="apos-modal" onClick={e => e.stopPropagation()}>
        <div className="apos-modal-header">
          <h3>Link to OKR</h3>
          <button className="apos-close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="apos-modal-body">
          <p className="apos-modal-subtitle">
            Link <strong>{orphan.task_id}</strong> to an OKR:
          </p>

          {loading ? (
            <div className="apos-modal-loading">⏳ Loading OKRs...</div>
          ) : (
            <select
              className="apos-okr-select"
              onChange={e => setSelectedOKR(e.target.value)}
              value={selectedOKR || ''}
            >
              <option value="">-- Select OKR --</option>
              {okrs.map(okr => (
                <option key={okr.id} value={okr.id}>
                  {okr.name} ({okr.id})
                </option>
              ))}
            </select>
          )}
        </div>

        <div className="apos-modal-footer">
          <button className="apos-btn apos-btn-cancel" onClick={onClose}>
            Cancel
          </button>
          <button
            className="apos-btn apos-btn-primary"
            onClick={() => {
              if (selectedOKR) {
                onLink(selectedOKR);
              }
            }}
            disabled={!selectedOKR}
          >
            Link OKR
          </button>
        </div>
      </div>
    </div>
  );
}

export { setupSidebar, Sidebar };
