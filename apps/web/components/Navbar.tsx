'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { Sparkles, Trophy, PlusCircle, User as UserIcon, LogOut, Search } from 'lucide-react';

export function Navbar() {
  const { user, logout, loading } = useAuth();

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <Link href="/" className="flex items-center space-x-2.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-sm">
                <Trophy className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold tracking-tight text-slate-900">
                SOLVE<span className="text-emerald-600">Bounty</span>
              </span>
            </Link>
            <span className="hidden md:inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              Where Problems Meet solvers
            </span>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-600">
            <Link href="/challenges" className="hover:text-emerald-600 transition-colors">
              Browse Challenges
            </Link>
            <Link href="/#how-it-works" className="hover:text-emerald-600 transition-colors">
              How It Works
            </Link>
          </nav>

          {/* Action / Auth Buttons */}
          <div className="flex items-center space-x-3">
            <Link
              href="/challenges/create"
              className="inline-flex items-center px-3.5 py-2 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm transition-colors"
            >
              <PlusCircle className="w-4 h-4 mr-1.5" />
              Post a Problem
            </Link>

            {!loading && (
              <>
                {user ? (
                  <div className="flex items-center space-x-3 pl-2 border-l border-slate-200">
                    <Link
                      href="/dashboard"
                      className="inline-flex items-center text-sm font-medium text-slate-700 hover:text-emerald-600"
                    >
                      <UserIcon className="w-4 h-4 mr-1 text-slate-400" />
                      {user.first_name || 'Dashboard'}
                    </Link>
                    <button
                      onClick={logout}
                      title="Logout"
                      className="p-1.5 text-slate-400 hover:text-rose-600 transition-colors rounded"
                    >
                      <LogOut className="w-4 h-4" />
                    </button>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <Link
                      href="/auth/login"
                      className="px-3.5 py-2 text-sm font-medium text-slate-700 hover:text-slate-900 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors"
                    >
                      Log in
                    </Link>
                    <Link
                      href="/auth/register"
                      className="px-3.5 py-2 text-sm font-medium text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 rounded-lg transition-colors"
                    >
                      Register
                    </Link>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
