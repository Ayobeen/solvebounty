'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Search, Filter, Trophy, Clock, Tag, ChevronRight, AlertCircle } from 'lucide-react';
import { fetchApi } from '@/lib/api';

export default function ChallengesPage() {
  const [challenges, setChallenges] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [status, setStatus] = useState('');

  const loadChallenges = async () => {
    setLoading(true);
    try {
      let q = '/challenges/?';
      if (search) q += `search=${encodeURIComponent(search)}&`;
      if (category) q += `category=${encodeURIComponent(category)}&`;
      if (status) q += `status=${encodeURIComponent(status)}&`;
      const data = await fetchApi(q);
      setChallenges(data.results || data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadChallenges();
  }, [category, status]);

  const categories = ['All', 'Software Engineering', 'Data Analytics', 'Mobile Development', 'Design', 'AI & ML', 'General'];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900">Explore Active Bounties</h1>
          <p className="text-sm text-slate-600 mt-1">Discover high-value challenges, compete with proof of work, and win cash prizes.</p>
        </div>
        <Link
          href="/challenges/create"
          className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors self-start md:self-auto"
        >
          + Post a Challenge
        </Link>
      </div>

      {/* Search & Filter Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-3 items-center">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search problems by keywords (e.g. React, Power BI, Python)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && loadChallenges()}
            className="w-full pl-10 pr-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
          />
        </div>
        <button
          onClick={loadChallenges}
          className="w-full md:w-auto px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-sm font-medium rounded-lg transition-colors"
        >
          Search
        </button>
      </div>

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Sidebar Filter */}
        <div className="space-y-6">
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center">
              <Filter className="w-3.5 h-3.5 mr-1.5 text-emerald-600" />
              Categories
            </h3>
            <div className="space-y-1">
              {categories.map((c) => {
                const isActive = (c === 'All' && !category) || category === c;
                return (
                  <button
                    key={c}
                    onClick={() => setCategory(c === 'All' ? '' : c)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                      isActive ? 'bg-emerald-50 text-emerald-700 font-semibold' : 'text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    {c}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">Status</h3>
            <div className="space-y-1">
              {['All', 'OPEN', 'FUNDED', 'JUDGING', 'COMPLETED'].map((st) => {
                const isActive = (st === 'All' && !status) || status === st;
                return (
                  <button
                    key={st}
                    onClick={() => setStatus(st === 'All' ? '' : st)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                      isActive ? 'bg-emerald-50 text-emerald-700 font-semibold' : 'text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    {st === 'All' ? 'All Statuses' : st}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Challenges List */}
        <div className="lg:col-span-3 space-y-4">
          {loading ? (
            <div className="p-12 text-center text-sm text-slate-500 bg-white rounded-xl border border-slate-200">
              Loading active challenges...
            </div>
          ) : challenges.length === 0 ? (
            <div className="p-12 text-center bg-white rounded-xl border border-slate-200 space-y-3">
              <AlertCircle className="w-8 h-8 text-slate-400 mx-auto" />
              <p className="text-base font-semibold text-slate-800">No challenges found</p>
              <p className="text-xs text-slate-500">Be the first to post a new problem or adjust your search filters.</p>
              <Link
                href="/challenges/create"
                className="inline-block px-4 py-2 bg-emerald-600 text-white text-xs font-medium rounded-lg"
              >
                Post a Challenge
              </Link>
            </div>
          ) : (
            challenges.map((c) => (
              <div
                key={c.id}
                className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="space-y-2 flex-1">
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">{c.category}</span>
                    <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
                      {c.status}
                    </span>
                    <span className="text-slate-400">•</span>
                    <span className="text-slate-500">
                      {c.submission_count || 0} {c.submission_count === 1 ? 'submission' : 'submissions'}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-slate-900 leading-snug hover:text-emerald-600 transition-colors">
                    <Link href={`/challenges/${c.id}`}>{c.title}</Link>
                  </h3>

                  <p className="text-xs text-slate-600 line-clamp-2">{c.description}</p>

                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {c.skills?.map((sk: any) => (
                      <span key={sk.id} className="text-[11px] bg-slate-50 text-slate-600 px-2 py-0.5 rounded border border-slate-200">
                        {sk.name}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex md:flex-col items-center md:items-end justify-between md:justify-center border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0 md:pl-6 min-w-[140px]">
                  <div className="text-left md:text-right">
                    <div className="text-[11px] text-slate-500 uppercase font-semibold">Prize</div>
                    <div className="text-lg font-black text-slate-900">{c.currency} {Number(c.budget).toLocaleString()}</div>
                  </div>
                  <Link
                    href={`/challenges/${c.id}`}
                    className="mt-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg transition-colors flex items-center space-x-1"
                  >
                    <span>View Bounty</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
