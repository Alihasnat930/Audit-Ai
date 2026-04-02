import React, { useState } from 'react';
import { Menu, Bell, User, LogOut } from 'lucide-react';

interface NavbarProps {
  onMenuClick: () => void;
}

export default function Navbar({ onMenuClick }: NavbarProps) {
  const [showUserMenu, setShowUserMenu] = useState(false);

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="flex items-center justify-between h-16 px-6">
        {/* Left side - Menu button */}
        <button
          onClick={onMenuClick}
          className="md:hidden hover:bg-gray-100 p-2 rounded"
        >
          <Menu size={24} />
        </button>

        {/* Right side - Notifications and user menu */}
        <div className="flex items-center space-x-4 ml-auto">
          {/* Notifications */}
          <button className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <Bell size={20} className="text-gray-600" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          {/* User menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                A
              </div>
              <span className="hidden sm:inline text-gray-700">Admin User</span>
            </button>

            {/* Dropdown menu */}
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl z-50">
                <div className="p-4 border-b border-gray-200">
                  <p className="text-sm font-semibold text-gray-800">admin@auditai.com</p>
                  <p className="text-xs text-gray-500">Administrator</p>
                </div>
                <button className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center space-x-2 text-gray-700 text-sm">
                  <User size={16} />
                  <span>Profile</span>
                </button>
                <button className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center space-x-2 text-gray-700 text-sm border-t border-gray-200">
                  <LogOut size={16} />
                  <span>Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
