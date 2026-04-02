import React, { useState } from 'react';
import { Save } from 'lucide-react';
import toast from 'react-hot-toast';

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    organizationName: 'Acme Corporation',
    email: 'admin@acme.com',
    timezone: 'UTC',
    language: 'English',
    fraudThreshold: 0.7,
    riskThreshold: 70,
    emailNotifications: true,
    reportFrequency: 'weekly',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleSave = () => {
    toast.success('Settings saved successfully!');
  };

  return (
    <div className="space-y-8 max-w-3xl">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-2">Manage your application settings and preferences</p>
      </div>

      {/* Organization Settings */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Organization</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Organization Name</label>
            <input
              type="text"
              name="organizationName"
              value={settings.organizationName}
              onChange={handleInputChange}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
        </div>
      </div>

      {/* Account Settings */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Account</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              name="email"
              value={settings.email}
              onChange={handleInputChange}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Timezone</label>
            <select
              name="timezone"
              value={settings.timezone}
              onChange={handleInputChange}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            >
              <option>UTC</option>
              <option>EST</option>
              <option>CST</option>
              <option>PST</option>
            </select>
          </div>
        </div>
      </div>

      {/* Audit Thresholds */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Audit Thresholds</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Fraud Score Threshold</label>
            <input
              type="number"
              name="fraudThreshold"
              min="0"
              max="1"
              step="0.1"
              value={settings.fraudThreshold}
              onChange={handleInputChange}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
            <p className="text-xs text-gray-500 mt-1">Values above this threshold are flagged (0-1)</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Risk Score Threshold</label>
            <input
              type="number"
              name="riskThreshold"
              min="0"
              max="100"
              value={settings.riskThreshold}
              onChange={handleInputChange}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
            <p className="text-xs text-gray-500 mt-1">Values above this threshold are flagged (0-100)</p>
          </div>
        </div>
      </div>

      {/* Notifications */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Notifications</h2>
        <div className="space-y-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="emailNotifications"
              name="emailNotifications"
              checked={settings.emailNotifications}
              onChange={handleInputChange}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded"
            />
            <label htmlFor="emailNotifications" className="ml-2 text-sm text-gray-700">
              Enable email notifications
            </label>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Report Frequency</label>
            <select
              name="reportFrequency"
              value={settings.reportFrequency}
              onChange={handleInputChange}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            >
              <option>Daily</option>
              <option>Weekly</option>
              <option>Monthly</option>
              <option>Never</option>
            </select>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          className="flex items-center space-x-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          <Save size={18} />
          <span>Save Changes</span>
        </button>
      </div>
    </div>
  );
}
