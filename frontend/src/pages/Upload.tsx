import React, { useMemo, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  AlertCircle,
  ArrowRight,
  CheckCircle,
  Download,
  File,
  ShieldAlert,
  Sparkles,
  Upload,
} from 'lucide-react';
import toast from 'react-hot-toast';

import api from '../services/api';

const LATEST_AUDIT_RESULT_KEY = 'latest_audit_result';
const DEMO_ORGANIZATION_ID = 'demo-org';

interface UploadStatus {
  fileName: string;
  status: 'pending' | 'uploading' | 'analyzing' | 'success' | 'error';
  progress: number;
  error?: string;
  detail?: string;
}

interface AuditSummary {
  total_records: number;
  high_risk_count: number;
  medium_risk_count: number;
  fraud_detections: number;
  avg_fraud_score: number;
  avg_risk_score: number;
}

interface AuditTransaction {
  transaction_id: string;
  amount: number;
  category?: string;
  vendor_name?: string;
  vendor_id?: string;
  fraud_score?: number;
  risk_score?: number;
  risk_level?: string;
  description?: string;
}

interface AuditResult {
  status: string;
  organization_id: string;
  summary: AuditSummary;
  data?: AuditTransaction[];
  validation_errors?: string[];
}

export default function UploadPage() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploads, setUploads] = useState<UploadStatus[]>([]);
  const [dragActive, setDragActive] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AuditResult | null>(null);
  const [analysisFileName, setAnalysisFileName] = useState<string>('');

  const topTransactions = useMemo(() => {
    if (!analysisResult?.data?.length) {
      return [];
    }

    return [...analysisResult.data]
      .sort((left, right) => {
        const riskDelta = (right.risk_score || 0) - (left.risk_score || 0);
        if (riskDelta !== 0) {
          return riskDelta;
        }
        return (right.fraud_score || 0) - (left.fraud_score || 0);
      })
      .slice(0, 5);
  }, [analysisResult]);

  const updateUpload = (fileName: string, updates: Partial<UploadStatus>) => {
    setUploads((previous) =>
      previous.map((item) => (item.fileName === fileName ? { ...item, ...updates } : item)),
    );
  };

  const ensureDemoOrganization = () => {
    const existing = localStorage.getItem('organization_id');
    if (existing) {
      return existing;
    }

    localStorage.setItem('organization_id', DEMO_ORGANIZATION_ID);
    return DEMO_ORGANIZATION_ID;
  };

  const persistLatestAudit = (result: AuditResult, fileName: string) => {
    localStorage.setItem(
      LATEST_AUDIT_RESULT_KEY,
      JSON.stringify({
        ...result,
        source_file: fileName,
        analyzed_at: new Date().toISOString(),
      }),
    );
  };

  const analyzeTransactionFile = async (fileName: string, path: string) => {
    const organizationId = ensureDemoOrganization();

    updateUpload(fileName, {
      status: 'analyzing',
      progress: 68,
      detail: 'Running AI audit analysis...',
    });

    const result: AuditResult = await api.runAudit(path, organizationId);
    setAnalysisResult(result);
    setAnalysisFileName(fileName);
    persistLatestAudit(result, fileName);

    updateUpload(fileName, {
      status: 'success',
      progress: 100,
      detail: `${result.summary.high_risk_count} high-risk items detected`,
    });
  };

  const handleFileSelect = async (files: FileList) => {
    for (let index = 0; index < files.length; index += 1) {
      const file = files[index];
      const isTransactionFile = /\.(csv|xlsx|xls)$/i.test(file.name);
      const isDocumentFile = /\.(pdf|jpg|jpeg|png)$/i.test(file.name);

      if (!isTransactionFile && !isDocumentFile) {
        toast.error(`Unsupported file type: ${file.name}`);
        continue;
      }

      const upload: UploadStatus = {
        fileName: file.name,
        status: 'pending',
        progress: 0,
      };

      setUploads((previous) => [upload, ...previous.filter((item) => item.fileName !== file.name)]);

      try {
        updateUpload(file.name, {
          status: 'uploading',
          progress: 32,
          detail: 'Uploading file...',
        });

        if (isTransactionFile) {
          const response = await api.uploadCSV(file);
          updateUpload(file.name, {
            progress: 58,
            detail: 'Upload complete. Preparing analysis...',
          });

          await analyzeTransactionFile(file.name, response.path);
          toast.success(`${file.name} uploaded and analyzed successfully.`);
        } else {
          await api.uploadInvoice(file);
          updateUpload(file.name, {
            status: 'success',
            progress: 100,
            detail: 'Document uploaded for supporting evidence.',
          });
          toast.success(`${file.name} uploaded successfully.`);
        }
      } catch (error: any) {
        const message = error?.response?.data?.detail || error?.message || 'Upload failed';
        updateUpload(file.name, {
          status: 'error',
          progress: 100,
          error: message,
        });
        toast.error(`Failed to process ${file.name}`);
      }
    }
  };

  const handleDrag = (event: React.DragEvent) => {
    event.preventDefault();
    event.stopPropagation();
    if (event.type === 'dragenter' || event.type === 'dragover') {
      setDragActive(true);
    } else if (event.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(false);
    handleFileSelect(event.dataTransfer.files);
  };

  const formatCurrency = (amount: number | undefined) =>
    new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(amount || 0);

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 lg:items-end lg:justify-between">
        <div>
          <h1 className="mt-3 text-3xl font-bold text-gray-900">Upload and Run Analysis</h1>
          <p className="mt-2 max-w-2xl text-gray-600">
            Upload transactions or supporting documents to run analysis.
          </p>
        </div>
      </div>

      <div className="grid gap-6">
        <div className="rounded-2xl bg-white shadow-sm">
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`rounded-2xl border-2 border-dashed p-12 text-center transition-colors ${
              dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <Upload className="mx-auto mb-4 h-12 w-12 text-gray-400" />
            <p className="text-lg font-semibold text-gray-900">Drag and drop a file here</p>
            <p className="mt-2 text-gray-600">CSV and Excel files trigger automatic analysis.</p>
            <p className="mt-4 text-sm text-gray-500">Supported formats: CSV, XLSX, XLS, PDF, JPG, PNG</p>

            <input
              ref={fileInputRef}
              type="file"
              multiple
              onChange={(event) => event.target.files && handleFileSelect(event.target.files)}
              className="hidden"
            />

            <button
              onClick={() => fileInputRef.current?.click()}
              className="mt-6 rounded-lg bg-blue-600 px-6 py-2 font-medium text-white transition-colors hover:bg-blue-700"
            >
              Select files
            </button>
          </div>
        </div>

        {/* Demo panel removed per request */}
      </div>

      {uploads.length > 0 && (
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-900">Upload activity</h2>
          <div className="mt-4 space-y-4">
            {uploads.map((upload) => (
              <div
                key={upload.fileName}
                className="flex items-center gap-4 rounded-xl border border-gray-200 p-4"
              >
                <File className="flex-shrink-0 text-gray-400" size={28} />

                <div className="flex-1">
                  <div className="flex items-center justify-between gap-4">
                    <p className="font-semibold text-gray-900">{upload.fileName}</p>
                    <span className="text-sm text-gray-500">{upload.progress}%</span>
                  </div>

                  <div className="mt-2 h-2 w-full rounded-full bg-gray-100">
                    <div
                      className={`h-2 rounded-full transition-all ${
                        upload.status === 'error' ? 'bg-red-500' : 'bg-blue-600'
                      }`}
                      style={{ width: `${upload.progress}%` }}
                    />
                  </div>

                  {upload.detail && <p className="mt-2 text-sm text-gray-600">{upload.detail}</p>}
                  {upload.error && <p className="mt-2 text-sm text-red-600">{upload.error}</p>}
                </div>

                {upload.status === 'success' && <CheckCircle className="text-green-500" size={22} />}
                {upload.status === 'error' && <AlertCircle className="text-red-500" size={22} />}
                {(upload.status === 'uploading' || upload.status === 'analyzing') && (
                  <div className="h-6 w-6 animate-spin rounded-full border-b-2 border-blue-500" />
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {analysisResult ? (
        <div className="space-y-6 rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1 text-sm font-medium text-emerald-700">
                <ShieldAlert size={16} />
                Analysis complete
              </p>
              <h2 className="mt-3 text-2xl font-bold text-gray-900">{analysisFileName}</h2>
              <p className="mt-2 text-gray-600">
                AuditAI finished scoring this file and saved the latest run for the Audit workspace.
              </p>
            </div>

            <Link
              to="/audit"
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-slate-900 px-4 py-2 font-medium text-white transition-colors hover:bg-slate-800"
            >
              Inspect full results
              <ArrowRight size={16} />
            </Link>
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <div className="rounded-xl border border-gray-200 p-4">
              <p className="text-sm text-gray-500">Records processed</p>
              <p className="mt-2 text-3xl font-bold text-gray-900">{analysisResult.summary.total_records}</p>
            </div>
            <div className="rounded-xl border border-red-200 bg-red-50 p-4">
              <p className="text-sm text-red-600">High-risk items</p>
              <p className="mt-2 text-3xl font-bold text-red-700">{analysisResult.summary.high_risk_count}</p>
            </div>
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
              <p className="text-sm text-amber-700">Fraud detections</p>
              <p className="mt-2 text-3xl font-bold text-amber-700">{analysisResult.summary.fraud_detections}</p>
            </div>
            <div className="rounded-xl border border-blue-200 bg-blue-50 p-4">
              <p className="text-sm text-blue-700">Average risk score</p>
              <p className="mt-2 text-3xl font-bold text-blue-700">
                {analysisResult.summary.avg_risk_score.toFixed(1)}
              </p>
            </div>
          </div>

          {analysisResult.validation_errors && analysisResult.validation_errors.length > 0 && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
              <p className="font-semibold text-amber-900">Validation notes</p>
              <div className="mt-2 space-y-1 text-sm text-amber-800">
                {analysisResult.validation_errors.map((error) => (
                  <p key={error}>- {error}</p>
                ))}
              </div>
            </div>
          )}

          <div className="rounded-2xl border border-gray-200">
            <div className="border-b border-gray-200 px-6 py-4">
              <h3 className="text-lg font-semibold text-gray-900">Top flagged transactions</h3>
              <p className="mt-1 text-sm text-gray-500">
                Highest risk items from the latest upload, sorted for a quick walkthrough.
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full min-w-[720px]">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                      Transaction
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                      Vendor
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                      Category
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                      Fraud
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                      Risk
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {topTransactions.map((transaction) => (
                    <tr key={transaction.transaction_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm font-medium text-slate-900">
                        {transaction.transaction_id}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {transaction.vendor_name || transaction.vendor_id || 'Unknown vendor'}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">{transaction.category || 'General'}</td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {formatCurrency(transaction.amount)}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {((transaction.fraud_score || 0) * 100).toFixed(0)}%
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span
                          className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
                            transaction.risk_level === 'High'
                              ? 'bg-red-100 text-red-700'
                              : transaction.risk_level === 'Medium'
                                ? 'bg-amber-100 text-amber-700'
                                : 'bg-emerald-100 text-emerald-700'
                          }`}
                        >
                          {(transaction.risk_level || 'Low').toUpperCase()} {(transaction.risk_score || 0).toFixed(1)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-8 text-center shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">No analysis yet</h2>
          <p className="mt-2 text-gray-600">
            Upload a CSV or Excel file to run the scoring pipeline automatically.
          </p>
        </div>
      )}
    </div>
  );
}
