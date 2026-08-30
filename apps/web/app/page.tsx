import React from 'react';
import Link from 'next/link';
import { ArrowRight, Trophy, Sparkles, CheckCircle2, ShieldCheck, Zap, Users, Search } from 'lucide-react';

export default function HomePage() {
  const steps = [
    { num: '01', title: 'POST', desc: 'Define your challenge or use our AI Challenge Architect to draft clear specs.' },
    { num: '02', title: 'FUND', desc: 'Fund the bounty securely via our payment gateway into protected escrow account.' },
    { num: '03', title: 'COMPETE', desc: 'Top solvers across Nigeria submit verified working solutions.' },
    { num: '04', title: 'CHOOSE', desc: 'Review submissions, inspect code/demos, and pick the best solution.' },
    { num: '05', title: 'PAY', desc: 'Bounty funds are automatically disbursed to the winner’s bank account.' },
  ];

  const featuredChallenges = [
    {
      id: 'demo-1',
      title: 'Build a Monthly Sales & Customer Performance Dashboard',
      category: 'Data Analytics',
      budget: '₦125,000',
      daysLeft: '5 days left',
      skills: ['Power BI', 'SQL', 'Data Analytics'],
      status: 'OPEN',
      submissions: 4,
    },
    {
      id: 'demo-2',
      title: 'React Native Cross-Platform Logistics Delivery Tracker',
      category: 'Mobile Development',
      budget: '₦250,000',
      daysLeft: '3 days left',
      skills: ['React Native', 'TypeScript', 'Maps API'],
      status: 'OPEN',
      submissions: 7,
    },
    {
      id: 'demo-3',
      title: 'Fintech Mobile App UI/UX Design System in Figma',
      category: 'Design',
      budget: '₦80,000',
      daysLeft: '7 days left',
      skills: ['UI/UX Design', 'Figma', 'Design System'],
      status: 'OPEN',
      submissions: 9,
    },
  ];

  return (
    <div className="space-y-20 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-16 bg-gradient-to-b from-emerald-50/60 via-slate-50 to-slate-50 border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-100/80 text-emerald-800 text-xs font-semibold mb-6 border border-emerald-200">
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>AI-Powered Bounty Marketplace for Nigerian Talent</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 max-w-4xl mx-auto leading-tight sm:leading-none">
            Have a problem? <br className="hidden sm:block" />
            <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              Put a prize on it.
            </span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto">
            Get multiple high-quality solutions from verified Nigerian engineers, designers, and analysts. Guaranteed payouts in Naira.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/challenges/create"
              className="w-full sm:w-auto px-8 py-3.5 text-base font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-md hover:shadow-lg transition-all flex items-center justify-center space-x-2"
            >
              <span>Post a Problem</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              href="/challenges"
              className="w-full sm:w-auto px-8 py-3.5 text-base font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 rounded-xl shadow-sm hover:shadow transition-all flex items-center justify-center"
            >
              Solve & Win Bounties
            </Link>
          </div>

          {/* Quick Metrics */}
          <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto border-t border-slate-200/80 pt-8">
            <div className="p-3">
              <div className="text-2xl font-bold text-slate-900">₦15M+</div>
              <div className="text-xs text-slate-500 font-medium">Bounties Funded</div>
            </div>
            <div className="p-3">
              <div className="text-2xl font-bold text-slate-900">1,200+</div>
              <div className="text-xs text-slate-500 font-medium">Skilled Solvers</div>
            </div>
            <div className="p-3">
              <div className="text-2xl font-bold text-slate-900">98%</div>
              <div className="text-xs text-slate-500 font-medium">Success Rate</div>
            </div>
            <div className="p-3">
              <div className="text-2xl font-bold text-emerald-600">100%</div>
              <div className="text-xs text-slate-500 font-medium">Escrow Protected</div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <h2 className="text-xs font-bold text-emerald-600 uppercase tracking-widest">TRANSPARENT WORKFLOW</h2>
          <p className="mt-2 text-3xl font-bold text-slate-900">How SolveBounty Works</p>
          <p className="mt-2 text-sm text-slate-600">A clean, 5-step transaction loop from problem definition to escrow bank payout.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {steps.map((s, idx) => (
            <div key={idx} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
              <div className="text-2xl font-black text-emerald-600/30 mb-2 font-mono">{s.num}</div>
              <h3 className="text-base font-bold text-slate-900 mb-1.5">{s.title}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Challenges Feed */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Featured Active Bounties</h2>
            <p className="text-sm text-slate-600">Open challenges waiting for solutions right now</p>
          </div>
          <Link href="/challenges" className="text-sm font-semibold text-emerald-600 hover:text-emerald-700 flex items-center space-x-1">
            <span>View all bounties</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {featuredChallenges.map((c) => (
            <div key={c.id} className="bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-all p-6 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between text-xs mb-3">
                  <span className="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium">
                    {c.category}
                  </span>
                  <span className="text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 text-xs">
                    {c.daysLeft}
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900 leading-snug hover:text-emerald-600 transition-colors">
                  <Link href={`/challenges`}>{c.title}</Link>
                </h3>
                <div className="flex flex-wrap gap-1.5 mt-4">
                  {c.skills.map((skill, sIdx) => (
                    <span key={sIdx} className="text-[11px] bg-slate-50 text-slate-600 px-2 py-0.5 rounded border border-slate-200">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div className="border-t border-slate-100 pt-4 mt-6 flex items-center justify-between">
                <div>
                  <div className="text-xs text-slate-500 font-medium">Prize Pool</div>
                  <div className="text-lg font-extrabold text-slate-900">{c.budget}</div>
                </div>
                <Link
                  href="/challenges"
                  className="px-3.5 py-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 rounded-lg transition-colors"
                >
                  View Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Trust & Escrow Guarantee */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-r from-emerald-600 to-teal-700 rounded-2xl text-white p-8 sm:p-12 shadow-md">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <span className="px-3 py-1 rounded-full bg-emerald-500/40 text-xs font-semibold uppercase tracking-wider text-emerald-100">
                Guaranteed Payouts
              </span>
              <h2 className="text-3xl font-extrabold mt-3">Double-Entry Ledger & Escrow Security</h2>
              <p className="mt-3 text-emerald-100 text-sm leading-relaxed">
                Posters fund challenges up front before solvers invest their time. Every Naira is tracked through immutable accounting ledger entries and disbursed seamlessly to Nigerian bank accounts.
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 space-y-4">
              <div className="flex items-start space-x-3">
                <ShieldCheck className="w-5 h-5 text-emerald-300 mt-0.5 flex-shrink-0" />
                <div className="text-xs">
                  <div className="font-semibold text-white">100% Pre-funded Bounties</div>
                  <div className="text-emerald-100">No unpaid work. Challenges are locked in escrow prior to submission.</div>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-300 mt-0.5 flex-shrink-0" />
                <div className="text-xs">
                  <div className="font-semibold text-white">Instant NUBAN Bank Settlement</div>
                  <div className="text-emerald-100">Winners receive prize transfers directly into any Nigerian commercial bank.</div>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Zap className="w-5 h-5 text-emerald-300 mt-0.5 flex-shrink-0" />
                <div className="text-xs">
                  <div className="font-semibold text-white">AI Assistant & Dispute Arbitration</div>
                  <div className="text-emerald-100">Automated technical quality audits and formal 48h dispute protection.</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
