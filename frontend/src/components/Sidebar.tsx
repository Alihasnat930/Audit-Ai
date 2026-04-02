import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Upload,
  Search,
  BarChart3,
  AlertCircle,
  Settings,
  X,
  LogOut,
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const menuItems = [
  { label: 'Dashboard', icon: LayoutDashboard, href: '/' },
  { label: 'Upload', icon: Upload, href: '/upload' },
  { label: 'Audit', icon: Search, href: '/audit' },
  { label: 'Reports', icon: BarChart3, href: '/reports' },
  { label: 'Alerts', icon: AlertCircle, href: '/alerts' },
  { label: 'Settings', icon: Settings, href: '/settings' },
];

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const location = useLocation();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-20 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed md:relative inset-y-0 left-0 w-64 bg-gray-900 text-white transition-transform duration-300 ease-in-out z-30 ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        } md:translate-x-0 flex flex-col`}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-800">
          <h1 className="text-2xl font-bold text-blue-400">AuditAI</h1>
          <button
            onClick={onClose}
            className="md:hidden hover:bg-gray-800 p-2 rounded"
          >
            <X size={20} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                to={item.href}
                onClick={onClose}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800'
                }`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-gray-800">
          <button className="w-full flex items-center space-x-3 px-4 py-3 text-gray-300 hover:bg-gray-800 rounded-lg transition-colors">
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>
    </>
  );
}
