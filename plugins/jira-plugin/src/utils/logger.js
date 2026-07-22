/**
 * Logger Utility
 *
 * Structured logging for plugin debugging
 * Logs go to browser console + backend (for monitoring)
 */

const LOG_LEVELS = {
  DEBUG: 'DEBUG',
  INFO: 'INFO',
  WARN: 'WARN',
  ERROR: 'ERROR',
};

/**
 * Log info message
 * @param {string} message
 * @param {any} data - Optional data to log
 */
export function log(message, data = null) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level: LOG_LEVELS.INFO,
    message,
    data,
  };

  console.log(`[APOS] ${message}`, data || '');

  // Send to backend (optional, for monitoring)
  sendToBackend(logEntry);
}

/**
 * Log error
 * @param {string} message
 * @param {Error} error
 */
export function logError(message, error) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level: LOG_LEVELS.ERROR,
    message,
    error: {
      name: error.name,
      message: error.message,
      stack: error.stack,
      response: error.response?.data,
    },
  };

  console.error(`[APOS ERROR] ${message}`, error);

  // Send to backend
  sendToBackend(logEntry);
}

/**
 * Log warning
 * @param {string} message
 */
export function logWarn(message) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level: LOG_LEVELS.WARN,
    message,
  };

  console.warn(`[APOS WARN] ${message}`);

  sendToBackend(logEntry);
}

/**
 * Send log entry to backend for monitoring
 * (Optional: depends on backend support)
 */
function sendToBackend(logEntry) {
  try {
    // POST to backend /logs endpoint (if implemented)
    // For now, just log to console
    // await fetch('http://localhost:5000/api/v1/logs', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(logEntry),
    // });
  } catch (e) {
    // Don't crash on logging error
    console.warn('Failed to send log to backend', e);
  }
}

export { log, logError, logWarn };
