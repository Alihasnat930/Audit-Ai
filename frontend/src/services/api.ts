import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface ApiConfig {
  baseURL: string;
  timeout: number;
  headers: Record<string, string>;
}

class ApiClient {
  private client: AxiosInstance;

  constructor(config?: Partial<ApiConfig>) {
    const defaultConfig: ApiConfig = {
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {},
    };

    this.client = axios.create({ ...defaultConfig, ...config });

    // Add request interceptor for auth token
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const response = await this.client.post('/auth/login', { email, password });
    return response.data;
  }

  async register(userData: any) {
    const response = await this.client.post('/auth/register', userData);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  async logout() {
    await this.client.post('/auth/logout');
    localStorage.removeItem('access_token');
  }

  // Upload endpoints
  async uploadCSV(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await this.client.post('/upload/csv', formData);
    return response.data;
  }

  async uploadInvoice(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await this.client.post('/upload/invoice', formData);
    return response.data;
  }

  async getUploadStatus() {
    const response = await this.client.get('/upload/status');
    return response.data;
  }

  // Audit endpoints
  async runAudit(filePath: string, organizationId: string) {
    const response = await this.client.post('/audit/run', { file_path: filePath, organization_id: organizationId });
    return response.data;
  }

  async getTransactions(organizationId: string, riskLevel?: string, skip = 0, limit = 20) {
    const params = { organization_id: organizationId, skip, limit };
    if (riskLevel) Object.assign(params, { risk_level: riskLevel });
    const response = await this.client.get('/audit/transactions', { params });
    return response.data;
  }

  async getTransactionDetail(transactionId: string) {
    const response = await this.client.get(`/audit/transaction/${transactionId}`);
    return response.data;
  }

  async getAuditSummary(organizationId: string) {
    const response = await this.client.get('/audit/summary', { params: { organization_id: organizationId } });
    return response.data;
  }

  async getVendorRisks(organizationId: string) {
    const response = await this.client.get('/audit/vendors', { params: { organization_id: organizationId } });
    return response.data;
  }

  async getAlerts(organizationId: string, limit = 10) {
    const response = await this.client.get('/audit/alerts', {
      params: { organization_id: organizationId, limit },
    });
    return response.data;
  }

  // Chatbot endpoints
  async chatMessage(transactionId: string, question: string, context?: string) {
    const response = await this.client.post('/chat/message', {
      question,
      context: {
        transaction_id: transactionId,
        ...(context ? { note: context } : {}),
      },
    });
    return response.data;
  }

  async explainTransaction(transactionId: string, amount = 0, details?: Record<string, unknown>) {
    const response = await this.client.post('/chat/explain', {
      transaction_id: transactionId,
      amount,
      details: details || {},
    });
    return response.data;
  }

  async summarizeTransactions(organizationId: string, timePeriod = '7d', stats?: Record<string, unknown>) {
    const response = await this.client.post('/chat/summarize', {
      organization_id: organizationId,
      period: timePeriod,
      ...(stats || {}),
    });
    return response.data;
  }

  // Report endpoints
  async generateReport(reportType: string, organizationId: string, payload?: Record<string, unknown>) {
    const response = await this.client.post(`/reports/generate/${reportType}`, {
      organization_id: organizationId,
      ...(payload || {}),
    });
    return response.data;
  }

  async listReports(organizationId: string, skip = 0, limit = 20) {
    const response = await this.client.get('/reports/list', {
      params: { organization_id: organizationId, skip, limit },
    });
    return response.data;
  }

  async getReport(reportId: string) {
    const response = await this.client.get(`/reports/${reportId}`);
    return response.data;
  }

  async deleteReport(reportId: string) {
    await this.client.delete(`/reports/${reportId}`);
  }
}

export default new ApiClient();
