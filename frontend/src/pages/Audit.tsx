import React, { useEffect, useMemo, useState } from 'react';
import { AlertCircle, TrendingDown, TrendingUp } from 'lucide-react';

import api from '../services/api';

const LATEST_AUDIT_RESULT_KEY = 'latest_audit_result';

interface Transaction {
  transaction_id: string;
  amount: number;
  vendor_id?: string;
  vendor_name?: string;
  category: string;
  fraud_score: number;
  risk_score: number;
  risk_level: string;
}

interface AuditResponse {
  total: number;
  transactions: Transaction[];
  risk_level_filter?: string;
}

interface StoredAuditResult {
  data?: Transaction[];
  source_file?: string;
}

export default function AuditPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [latestRunTransactions, setLatestRunTransactions] = useState<Transaction[] | null | undefined>(undefined);
  const [latestRunFile, setLatestRunFile] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<string | undefined>();

  useEffect(() => {
    const stored = localStorage.getItem(LATEST_AUDIT_RESULT_KEY);
    if (!stored) {
      setLatestRunTransactions(null);
      return;
    }

    try {
      const parsed: StoredAuditResult = JSON.parse(stored);
      if (parsed.data?.length) {
        setLatestRunTransactions(parsed.data);
        setLatestRunFile(parsed.source_file || '');
        return;
      }
    } catch (error) {
      console.warn('Unable to parse latest audit result:', error);
    }

    setLatestRunTransactions(null);
  }, []);

  useEffect(() => {
    if (latestRunTransactions === undefined) {
      return;
    }

    const fetchTransactions = async () => {
      setLoading(true);

      try {
        if (latestRunTransactions) {
          const filtered = riskFilter
            ? latestRunTransactions.filter((transaction) => transaction.risk_level === riskFilter)
            : latestRunTransactions;
          setTransactions(filtered.slice(0, 20));
          return;
        }

        const organizationId = localStorage.getItem('organization_id') || 'demo-org';
        const data: AuditResponse = await api.getTransactions(organizationId, riskFilter, 0, 20);
        setTransactions(data.transactions || []);
      } catch (error) {
        console.error('Failed to fetch transactions:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTransactions();
  }, [latestRunTransactions, riskFilter]);

  const highRiskCount = useMemo(
    () => transactions.filter((transaction) => transaction.risk_level === 'High').length,
    [transactions],
  );

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'High':
        return 'bg-red-100 text-red-800';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'Low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRiskIcon = (score: number) => {
    if (score > 0.7) return <AlertCircle className="text-red-500" size={16} />;
    if (score > 0.4) return <TrendingDown className="text-yellow-500" size={16} />;
    return <TrendingUp className="text-green-500" size={16} />;
  };

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-b-2 border-blue-500" />
          <p className="mt-4 text-gray-600">Loading transactions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Audit Results</h1>
          <p className="mt-2 text-gray-600">Review transactions and their risk assessments.</p>
        </div>

        {latestRunTransactions && (
          <div className="rounded-xl border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-800">
            Showing latest uploaded run{latestRunFile ? ` from ${latestRunFile}` : ''}. High-risk items
            in view: {highRiskCount}
          </div>
        )}
      </div>

      <div className="rounded-lg bg-white p-4 shadow">
        <label className="mb-2 block text-sm font-medium text-gray-700">Filter by Risk Level</label>
        <div className="flex flex-wrap gap-2">
          {['All', 'High', 'Medium', 'Low'].map((level) => (
            <button
              key={level}
              onClick={() => setRiskFilter(level === 'All' ? undefined : level)}
              className={`rounded-lg px-4 py-2 font-medium transition-colors ${
                (!riskFilter && level === 'All') || riskFilter === level
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      <div className="overflow-hidden rounded-lg bg-white shadow">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-gray-200 bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-700">
                  Transaction ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-700">
                  Vendor
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-700">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-700">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-700">
                  Fraud Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-700">
                  Risk Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-700">
                  Risk Level
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {transactions.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-8 text-center text-gray-500">
                    No transactions found for this filter.
                  </td>
                </tr>
              ) : (
                transactions.map((transaction) => (
                  <tr key={transaction.transaction_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-blue-600">
                      {transaction.transaction_id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {transaction.vendor_name || transaction.vendor_id || 'Unknown vendor'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      ${transaction.amount.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{transaction.category}</td>
                    <td className="px-6 py-4 text-sm">
                      <div className="flex items-center space-x-1">
                        {getRiskIcon(transaction.fraud_score)}
                        <span>{(transaction.fraud_score * 100).toFixed(0)}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm font-medium">
                      {transaction.risk_score.toFixed(1)}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-medium ${getRiskColor(transaction.risk_level)}`}
                      >
                        {transaction.risk_level}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
