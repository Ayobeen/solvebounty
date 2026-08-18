import React from 'react';
import Link from 'next/link';
import { Trophy, ShieldCheck } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4 md:col-span-2">
            <div className="flex items-center space-x-2.5">
              <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
                <Trophy className="w-4 h-4" />
              </div>
              <span className="text-lg font-bold text-slate-900">
                SOLVE<span className="text-emerald-600">Bounty</span>
              </span>
            </div>
            <p className="text-sm text-slate-600 max-w-sm">
              Have a problem? Put a prize on it. The Nigerian marketplace for high-stakes problem solving, verified bounties, and secure escrow payouts.
            </p>
            <div className="flex items-center text-xs text-slate-500 space-x-1">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Secured with Paystack escrow & ledger audit trails</span>
            </div>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wider mb-3">Marketplace</h4>
            <ul className="space-y-2 text-sm text-slate-600">
              <li><Link href="/challenges" className="hover:text-emerald-600">Browse Challenges</Link></li>
              <li><Link href="/challenges/create" className="hover:text-emerald-600">Post a Bounty</Link></li>
              <li><Link href="/#how-it-works" className="hover:text-emerald-600">How It Works</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wider mb-3">Account</h4>
            <ul className="space-y-2 text-sm text-slate-600">
              <li><Link href="/auth/login" className="hover:text-emerald-600">Sign In</Link></li>
              <li><Link href="/auth/register" className="hover:text-emerald-600">Register</Link></li>
              <li><Link href="/dashboard" className="hover:text-emerald-600">Dashboard</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-100 mt-10 pt-6 flex flex-col md:flex-row items-center justify-between text-xs text-slate-500">
          <p>© 2026 SolveBounty. Built for Nigeria.</p>
          <p>Engineered with Django + Next.js + PostgreSQL</p>
        </div>
      </div>
    </footer>
  );
}
