import React, { useEffect, useMemo, useState } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, TrendingUp, Users, DollarSign } from 'lucide-react';
import api from '../services/api';

interface SummaryStats {
  total_transactions: number;
  high_risk_count: number;
  fraud_detections: number;
  avg_fraud_score: number;
  avg_risk_score: number;
}

interface TrendPoint {
  name: string;
  transactions: number;
  fraud: number;
}

interface AlertItem {
  transaction_id: string;
  vendor?: string;
  message?: string;
  timestamp?: string;
  fraud_score?: number;
  risk_score?: number;
  risk_level?: string;
}

export default function Dashboard() {
  const [summary, setSummary] = useState<SummaryStats | null>(null);
  const [trendData, setTrendData] = useState<TrendPoint[]>([]);
  const [riskDistribution, setRiskDistribution] = useState<{ name: string; value: number }[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const organizationId = localStorage.getItem('organization_id') || 'demo-org';
        const payload = await api.getAuditSummary(organizationId);
        setSummary(payload.summary || null);
        setTrendData(payload.trends || []);
        setRiskDistribution(payload.risk_distribution || []);
        setAlerts(payload.alerts || []);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const chartTrends = useMemo(() => trendData.length ? trendData : [], [trendData]);
  const distribution = useMemo(() => riskDistribution.length ? riskDistribution : [], [riskDistribution]);
  const COLORS = ['#10b981', '#f59e0b', '#ef4444'];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome back! Here's your audit overview.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total Transactions</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{summary?.total_transactions || 0}</p>
            </div>
            <DollarSign className="text-blue-500" size={32} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">High Risk Items</p>
              <p className="text-3xl font-bold text-red-600 mt-2">{summary?.high_risk_count || 0}</p>
            </div>
            <AlertCircle className="text-red-500" size={32} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Fraud Detections</p>
              <p className="text-3xl font-bold text-orange-600 mt-2">{summary?.fraud_detections || 0}</p>
            </div>
            <TrendingUp className="text-orange-500" size={32} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Avg Risk Score</p>
              <p className="text-3xl font-bold text-purple-600 mt-2">{summary?.avg_risk_score?.toFixed(1) || 0}</p>
            </div>
            <Users className="text-purple-500" size={32} />
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Transaction Trend */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Transaction Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="transactions" stroke="#3b82f6" />
              <Line type="monotone" dataKey="fraud" stroke="#ef4444" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Distribution */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Risk Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={distribution}
                cx="40%"
                cy="50%"
                labelLine={false}
                label={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {distribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend verticalAlign="middle" align="right" layout="vertical" />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Alerts */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Alerts</h2>
        <div className="space-y-4">
          {alerts.length === 0 ? (
            <p className="text-sm text-gray-500">No alerts available for this organization yet.</p>
          ) : (
            alerts.map((alert) => (
              <div
                key={alert.transaction_id}
                className="flex items-start space-x-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <AlertCircle className="text-red-500 flex-shrink-0" size={20} />
                <div className="flex-1">
                  <p className="font-semibold text-gray-900">
                    {alert.vendor || 'Unknown vendor'} · {alert.risk_level} risk
                  </p>
                  <p className="text-sm text-gray-600">
                    {alert.message || `Fraud ${alert.fraud_score?.toFixed(2) ?? 0}`} · Risk {alert.risk_score?.toFixed(1)}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">{alert.timestamp || 'Recent'}</p>
                </div>
                <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">Review</button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
