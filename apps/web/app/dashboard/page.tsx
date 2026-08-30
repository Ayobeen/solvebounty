'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { fetchApi } from '@/lib/api';
import {
  Trophy,
  PlusCircle,
  FileText,
  CreditCard,
  CheckCircle,
  ExternalLink,
  DollarSign,
  Award,
  AlertCircle
} from 'lucide-react';

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const [activeTab, setActiveTab] = useState<'challenges' | 'submissions' | 'payouts'>('challenges');
  const [myChallenges, setMyChallenges] = useState<any[]>([]);
  const [mySubmissions, setMySubmissions] = useState<any[]>([]);
  const [payoutAccount, setPayoutAccount] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Bank Account Setup Form State
  const [bankCode, setBankCode] = useState('058');
  const [bankName, setBankName] = useState('Guaranty Trust Bank (GTBank)');
  const [accountNumber, setAccountNumber] = useState('');
  const [accountName, setAccountName] = useState('');
  const [bankSavedMsg, setBankSavedMsg] = useState('');

  const loadDashboardData = async () => {
    try {
      // Load user challenges
      const cRes = await fetchApi('/challenges/');
      const allC = cRes.results || cRes || [];
      if (user) {
        setMyChallenges(allC.filter((c: any) => c.poster?.id === user.id));
      }

      // Load user submissions
      try {
        const sRes = await fetchApi('/me/submissions/');
        setMySubmissions(sRes || []);
      } catch (e) { }

      // Load payout account
      try {
        const pRes = await fetchApi('/payouts/account/');
        setPayoutAccount(pRes);
        if (pRes.account_number) setAccountNumber(pRes.account_number);
        if (pRes.account_name) setAccountName(pRes.account_name);
      } catch (e) { }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      loadDashboardData();
    }
  }, [user]);

  const handleSaveBankAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetchApi('/payouts/account/', {
        method: 'POST',
        body: JSON.stringify({
          bank_code: bankCode,
          bank_name: bankName,
          account_number: accountNumber,
          account_name: accountName,
        }),
      });
      setPayoutAccount(res);
      setBankSavedMsg('Bank payout account saved successfully!');
    } catch (err: any) {
      alert(err.message || 'Failed to save bank account.');
    }
  };

  if (authLoading || loading) {
    return <div className="max-w-7xl mx-auto px-4 py-16 text-center text-sm text-slate-500">Loading your dashboard...</div>;
  }

  if (!user) {
    return (
      <div className="max-w-md mx-auto px-4 py-16 text-center space-y-4">
        <p className="text-base font-bold text-slate-900">Please sign in to access your dashboard.</p>
        <Link href="/auth/login" className="inline-block px-5 py-2.5 bg-emerald-600 text-white text-xs font-semibold rounded-lg">
          Log in
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Dashboard Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900">Welcome, {user.first_name} {user.last_name}</h1>
          <div className="flex items-center space-x-3 text-xs text-slate-500 mt-1">
            <span>{user.email}</span>
            <span>•</span>
            <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
              Role: {user.role}
            </span>
          </div>
        </div>
        <Link
          href="/challenges/create"
          className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-sm flex items-center space-x-1.5 self-start sm:self-auto"
        >
          <PlusCircle className="w-4 h-4" />
          <span>Post New Challenge</span>
        </Link>
      </div>

      {/* Tabs */}
      <div className="flex space-x-2 border-b border-slate-200 pb-2 text-xs font-semibold">
        {[
          { id: 'challenges', label: `My Challenges (${myChallenges.length})` },
          { id: 'submissions', label: `My Submissions (${mySubmissions.length})` },
          { id: 'payouts', label: 'Payouts & Banking' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 rounded-lg transition-colors ${activeTab === tab.id
              ? 'bg-slate-900 text-white'
              : 'text-slate-600 hover:bg-slate-100'
              }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'challenges' && (
        <div className="space-y-4">
          {myChallenges.length === 0 ? (
            <div className="p-12 text-center bg-white rounded-xl border border-slate-200 space-y-3">
              <p className="text-sm text-slate-600">You haven&apos;t posted any challenges yet.</p>
              <Link
                href="/challenges/create"
                className="inline-block px-4 py-2 bg-emerald-600 text-white text-xs font-semibold rounded-lg"
              >
                Post Your First Problem
              </Link>
            </div>
          ) : (
            myChallenges.map((c) => (
              <div
                key={c.id}
                className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between"
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-bold border border-emerald-200">
                      {c.status}
                    </span>
                    <span className="text-xs text-slate-500">{c.category}</span>
                  </div>
                  <h3 className="text-base font-bold text-slate-900">
                    <Link href={`/challenges/${c.id}`} className="hover:text-emerald-600">
                      {c.title}
                    </Link>
                  </h3>
                  <div className="text-xs text-slate-500">
                    Budget: <strong>{c.currency} {Number(c.budget).toLocaleString()}</strong>
                  </div>
                </div>
                <Link
                  href={`/challenges/${c.id}`}
                  className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded-lg transition-colors"
                >
                  Manage
                </Link>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'submissions' && (
        <div className="space-y-4">
          {mySubmissions.length === 0 ? (
            <div className="p-12 text-center bg-white rounded-xl border border-slate-200 space-y-3">
              <p className="text-sm text-slate-600">You haven&apos;t submitted any solutions yet.</p>
              <Link
                href="/challenges"
                className="inline-block px-4 py-2 bg-emerald-600 text-white text-xs font-semibold rounded-lg"
              >
                Browse Active Bounties
              </Link>
            </div>
          ) : (
            mySubmissions.map((s) => (
              <div
                key={s.id}
                className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between"
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className={`text-xs px-2 py-0.5 rounded font-bold ${s.status === 'WINNER' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-700'
                      }`}>
                      {s.status}
                    </span>
                    <span className="text-xs text-slate-500">Submitted on {new Date(s.submitted_at).toLocaleDateString()}</span>
                  </div>
                  <h3 className="text-base font-bold text-slate-900">{s.title}</h3>
                  <p className="text-xs text-slate-600 line-clamp-1">{s.content}</p>
                </div>
                <Link
                  href={`/challenges/${s.challenge}`}
                  className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded-lg transition-colors"
                >
                  View Challenge
                </Link>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'payouts' && (
        <div className="max-w-2xl bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center">
              <CreditCard className="w-4 h-4 mr-2 text-emerald-600" />
              Nigerian Commercial Bank Payout Details
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              When you win a challenge bounty, earnings will be transferred directly to this NUBAN account.
            </p>
          </div>

          {bankSavedMsg && (
            <div className="p-3 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-lg text-xs font-medium">
              {bankSavedMsg}
            </div>
          )}

          <form onSubmit={handleSaveBankAccount} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Bank Name</label>
              <select
                value={bankCode}
                onChange={(e) => {
                  setBankCode(e.target.value);
                  setBankName(e.target.options[e.target.selectedIndex].text);
                }}
                className="w-full px-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="058">Guaranty Trust Bank (GTBank)</option>
                <option value="011">First Bank of Nigeria</option>
                <option value="033">United Bank for Africa (UBA)</option>
                <option value="057">Zenith Bank</option>
                <option value="044">Access Bank</option>
                <option value="214">First City Monument Bank (FCMB)</option>
                <option value="035">Wema Bank</option>
                <option value="070">Fidelity Bank</option>
                <option value="101">Providus Bank</option>
                <option value="50211">Kuda Microfinance Bank</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">10-Digit NUBAN Account Number</label>
              <input
                type="text"
                maxLength={10}
                placeholder="0123456789"
                value={accountNumber}
                onChange={(e) => setAccountNumber(e.target.value)}
                className="w-full px-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Account Holder Full Name</label>
              <input
                type="text"
                placeholder="As shown on your bank statement"
                value={accountName}
                onChange={(e) => setAccountName(e.target.value)}
                className="w-full px-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>

            <button
              type="submit"
              className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg shadow-sm transition-colors"
            >
              Save Payout Account
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
