import React, { useMemo, useState } from 'react';
import { ArrowRight, FileText, Sparkles } from 'lucide-react';
import toast from 'react-hot-toast';

import api from '../services/api';

const LATEST_AUDIT_RESULT_KEY = 'latest_audit_result';

interface AuditTransaction {
  transaction_id: string;
  vendor_name?: string;
  amount: number;
  category?: string;
  fraud_score?: number;
  risk_score?: number;
  risk_level?: string;
  anomaly_flag?: number;
}

interface GeneratedReport {
  report_type: string;
  generated_at: string;
  summary?: Record<string, number | string>;
  totals?: Record<string, number | string>;
  recommendations?: string[];
  top_fraud_transactions?: AuditTransaction[];
  high_risk_transactions?: AuditTransaction[];
  top_vendors?: Array<Record<string, number | string>>;
}

interface LatestAuditResult {
  data?: AuditTransaction[];
}

const reportTypes = [
  { id: 'fraud_analysis', label: 'Fraud Analysis', description: 'Summarize suspicious activity and top fraud indicators.' },
  { id: 'risk_assessment', label: 'Risk Assessment', description: 'Highlight high-risk transactions and control weaknesses.' },
  { id: 'transaction_summary', label: 'Transaction Summary', description: 'Roll up volume, spend, and top vendor activity.' },
  { id: 'vendor_analysis', label: 'Vendor Analysis', description: 'Aggregate vendors from the latest upload and rank them by exposure.' },
  { id: 'compliance', label: 'Compliance', description: 'Create a lightweight compliance log from the latest audit run.' },
];

function readLatestAuditTransactions(): AuditTransaction[] {
  const stored = localStorage.getItem(LATEST_AUDIT_RESULT_KEY);
  if (!stored) {
    return [];
  }

  try {
    const parsed: LatestAuditResult = JSON.parse(stored);
    return parsed.data || [];
  } catch (error) {
    console.warn('Unable to parse latest audit result for reports:', error);
    return [];
  }
}

function buildReportPayload(type: string, transactions: AuditTransaction[]) {
  if (!transactions.length) {
    return null;
  }

  const vendorsMap = new Map<string, { vendor_name: string; risk_score: number; transaction_count: number }>();
  transactions.forEach((transaction) => {
    const vendorName = transaction.vendor_name || 'Unknown vendor';
    const current = vendorsMap.get(vendorName) || {
      vendor_name: vendorName,
      risk_score: 0,
      transaction_count: 0,
    };
    current.risk_score = Math.max(current.risk_score, transaction.risk_score || 0);
    current.transaction_count += 1;
    vendorsMap.set(vendorName, current);
  });

  const vendors = Array.from(vendorsMap.values());
  const auditLogs = transactions.map((transaction) => ({
    action_type:
      transaction.risk_level === 'High' ? 'flagged_high_risk_transaction' : 'logged_transaction_review',
    transaction_id: transaction.transaction_id,
    risk_level: transaction.risk_level || 'Low',
  }));

  return {
    report_type: type,
    transactions,
    vendors,
    audit_logs: auditLogs,
  };
}

export default function ReportsPage() {
  const [loading, setLoading] = useState(false);
  const [generatedReport, setGeneratedReport] = useState<GeneratedReport | null>(null);

  const reportPreviewRows = useMemo(() => {
    if (!generatedReport) {
      return [];
    }
    return (
      generatedReport.top_fraud_transactions ||
      generatedReport.high_risk_transactions ||
      generatedReport.top_vendors ||
      []
    );
  }, [generatedReport]);

  const reportSummary = useMemo(() => {
    if (!generatedReport) {
      return [];
    }
    return Object.entries(generatedReport.summary || generatedReport.totals || {});
  }, [generatedReport]);

  const handleGenerateReport = async (type: string) => {
    const transactions = readLatestAuditTransactions();
    if (!transactions.length) {
      toast.error('Upload and analyze the demo CSV first so reports have data to work with.');
      return;
    }

    const payload = buildReportPayload(type, transactions);
    if (!payload) {
      toast.error('No audit data available for report generation.');
      return;
    }

    setLoading(true);
    try {
      const organizationId = localStorage.getItem('organization_id') || 'demo-org';
      const response = await api.generateReport(type, organizationId, payload);
      if (response.status !== 'success' || !response.report) {
        throw new Error(response.message || 'Report generation failed');
      }
      setGeneratedReport(response.report);
      toast.success(`${type.replace(/_/g, ' ')} report generated.`);
    } catch (error: any) {
      toast.error(error?.message || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="inline-flex items-center gap-2 rounded-full bg-blue-50 px-3 py-1 text-sm font-medium text-blue-700">
            <Sparkles size={16} />
            Generate from latest analysis
          </p>
          <h1 className="mt-3 text-3xl font-bold text-gray-900">Reports</h1>
          <p className="mt-2 max-w-2xl text-gray-600">
            Turn the latest uploaded audit run into a sharable report preview for demos, internal
            reviews, or investor walkthroughs.
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {reportTypes.map((type) => (
          <div key={type.id} className="rounded-2xl bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900">{type.label}</h2>
            <p className="mt-2 text-sm text-gray-600">{type.description}</p>
            <button
              onClick={() => handleGenerateReport(type.id)}
              disabled={loading}
              className="mt-4 inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? 'Generating...' : 'Generate preview'}
              {!loading && <ArrowRight size={16} />}
            </button>
          </div>
        ))}
      </div>

      {generatedReport ? (
        <div className="space-y-6 rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-start gap-4">
            <div className="rounded-xl bg-slate-900 p-3 text-white">
              <FileText size={24} />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {generatedReport.report_type.replace(/_/g, ' ').toUpperCase()}
              </h2>
              <p className="mt-1 text-sm text-gray-500">
                Generated {new Date(generatedReport.generated_at).toLocaleString()}
              </p>
            </div>
          </div>

          {reportSummary.length > 0 && (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              {reportSummary.map(([key, value]) => (
                <div key={key} className="rounded-xl border border-gray-200 p-4">
                  <p className="text-sm capitalize text-gray-500">{key.replace(/_/g, ' ')}</p>
                  <p className="mt-2 text-2xl font-bold text-gray-900">{String(value)}</p>
                </div>
              ))}
            </div>
          )}

          {generatedReport.recommendations && generatedReport.recommendations.length > 0 && (
            <div className="rounded-xl border border-blue-200 bg-blue-50 p-4">
              <h3 className="font-semibold text-blue-900">Recommended next actions</h3>
              <div className="mt-2 space-y-1 text-sm text-blue-800">
                {generatedReport.recommendations.map((recommendation) => (
                  <p key={recommendation}>- {recommendation}</p>
                ))}
              </div>
            </div>
          )}

          {reportPreviewRows.length > 0 && (
            <div className="rounded-xl border border-gray-200">
              <div className="border-b border-gray-200 px-6 py-4">
                <h3 className="font-semibold text-gray-900">Preview rows</h3>
                <p className="mt-1 text-sm text-gray-500">
                  A quick slice of the report payload for demos and screenshots.
                </p>
              </div>
              <div className="space-y-3 px-6 py-4">
                {reportPreviewRows.slice(0, 5).map((row, index) => (
                  <pre
                    key={index}
                    className="overflow-x-auto rounded-lg bg-slate-950 p-4 text-xs text-slate-100"
                  >
                    {JSON.stringify(row, null, 2)}
                  </pre>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-8 text-center shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">No report preview yet</h2>
          <p className="mt-2 text-gray-600">
            Generate a report after you run the upload analysis flow. The latest run is used as the
            report source.
          </p>
        </div>
      )}
    </div>
  );
}
