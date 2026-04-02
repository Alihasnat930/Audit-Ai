import React, { useEffect, useMemo, useState } from 'react';
import { AlertCircle, CheckCircle, Clock } from 'lucide-react';
import toast from 'react-hot-toast';

import api from '../services/api';

interface AlertItem {
  alert_id: string;
  transaction_id: string;
  alert_type: string;
  message: string;
  resolved: boolean;
  created_at: string;
  fraud_score?: number;
  risk_score?: number;
  risk_level?: string;
  vendor?: string;
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [filter, setFilter] = useState<'all' | 'unresolved' | 'resolved'>('unresolved');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlerts = async () => {
      setLoading(true);
      try {
        const organizationId = localStorage.getItem('organization_id') || 'demo-org';
        const response = await api.getAlerts(organizationId, 12);
        const normalized: AlertItem[] = (response.alerts || []).map((alert: any, index: number) => ({
          alert_id: alert.transaction_id || `alert-${index}`,
          transaction_id: alert.transaction_id || 'unknown',
          alert_type: alert.risk_level ? `${String(alert.risk_level).toLowerCase()}_risk` : 'audit_alert',
          message: alert.message || 'Potential issue detected',
          resolved: false,
          created_at: alert.timestamp || 'Recent',
          fraud_score: alert.fraud_score,
          risk_score: alert.risk_score,
          risk_level: alert.risk_level,
          vendor: alert.vendor,
        }));
        setAlerts(normalized);
      } catch (error) {
        console.error('Failed to fetch alerts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  const handleResolveAlert = (alertId: string) => {
    setAlerts((previous) =>
      previous.map((alert) => (alert.alert_id === alertId ? { ...alert, resolved: true } : alert)),
    );
    toast.success('Alert resolved');
  };

  const filteredAlerts = useMemo(
    () =>
      alerts.filter((alert) => {
        if (filter === 'unresolved') return !alert.resolved;
        if (filter === 'resolved') return alert.resolved;
        return true;
      }),
    [alerts, filter],
  );

  const getRiskBorder = (riskLevel?: string) => {
    switch (riskLevel) {
      case 'High':
        return 'border-l-red-500';
      case 'Medium':
        return 'border-l-yellow-500';
      case 'Low':
        return 'border-l-blue-500';
      default:
        return 'border-l-gray-400';
    }
  };

  const getSeverityIcon = (fraudScore = 0) => {
    if (fraudScore > 0.75) return <AlertCircle className="text-red-500" size={20} />;
    if (fraudScore > 0.45) return <Clock className="text-yellow-500" size={20} />;
    return <CheckCircle className="text-blue-500" size={20} />;
  };

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-b-2 border-blue-500" />
          <p className="mt-4 text-gray-600">Loading alerts...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Alerts</h1>
        <p className="mt-2 text-gray-600">Manage and track the most important findings.</p>
      </div>

      <div className="rounded-lg bg-white p-4 shadow">
        <div className="flex flex-wrap gap-2">
          {(['all', 'unresolved', 'resolved'] as const).map((value) => (
            <button
              key={value}
              onClick={() => setFilter(value)}
              className={`rounded-lg px-4 py-2 font-medium capitalize transition-colors ${
                filter === value
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {value}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        {filteredAlerts.length === 0 ? (
          <div className="rounded-lg bg-white p-8 text-center shadow">
            <CheckCircle className="mx-auto h-12 w-12 text-green-500" />
            <p className="mt-4 text-gray-600">No alerts in this category.</p>
          </div>
        ) : (
          filteredAlerts.map((alert) => (
            <div
              key={alert.alert_id}
              className={`rounded-lg border-l-4 bg-white p-6 shadow ${
                alert.resolved ? 'border-l-green-500 opacity-75' : getRiskBorder(alert.risk_level)
              }`}
            >
              <div className="flex items-start gap-4">
                {getSeverityIcon(alert.fraud_score)}
                <div className="flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="font-semibold text-gray-900">
                      {alert.alert_type.replace(/_/g, ' ').toUpperCase()}
                    </h3>
                    {alert.resolved && (
                      <span className="rounded bg-green-100 px-2 py-1 text-xs text-green-800">
                        Resolved
                      </span>
                    )}
                  </div>
                  <p className="mt-2 text-gray-600">{alert.message}</p>
                  <p className="mt-2 text-sm text-gray-500">
                    Vendor: {alert.vendor || 'Unknown'} | Transaction:{' '}
                    <span className="font-mono text-blue-600">{alert.transaction_id}</span>
                  </p>
                  <p className="mt-1 text-xs text-gray-500">
                    Created: {alert.created_at} | Risk {alert.risk_level || 'Low'} | Fraud{' '}
                    {((alert.fraud_score || 0) * 100).toFixed(0)}%
                  </p>
                </div>
                {!alert.resolved && (
                  <button
                    onClick={() => handleResolveAlert(alert.alert_id)}
                    className="whitespace-nowrap rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-700"
                  >
                    Resolve
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
