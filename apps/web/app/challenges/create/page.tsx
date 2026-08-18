'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { fetchApi } from '@/lib/api';
import { Sparkles, ArrowRight, ArrowLeft, Check, Trophy, ShieldCheck, Zap, Plus, Trash2 } from 'lucide-react';

export default function CreateChallengePage() {
  const router = useRouter();
  const { user } = useAuth();
  const [step, setStep] = useState(1);
  const [loadingAI, setLoadingAI] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  // AI Prompt Assistant Input
  const [aiPrompt, setAiPrompt] = useState('');

  // Form State
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('Software Engineering');
  const [description, setDescription] = useState('');
  const [budget, setBudget] = useState('100000');
  const [deadlineDays, setDeadlineDays] = useState('14');
  const [requirements, setRequirements] = useState<string[]>([
    'Complete working solution conforming to specifications',
    'Clean, maintainable source files',
    'Technical walkthrough documentation or demo'
  ]);
  const [newReq, setNewReq] = useState('');
  const [ipTerms, setIpTerms] = useState('Full intellectual property rights transfer to the challenge poster upon winner payout.');
  const [rules, setRules] = useState('No plagiarized submissions. Original code/designs only. Solvers must provide proof of work.');

  const handleRunAI = async () => {
    if (!aiPrompt.trim() || aiPrompt.trim().length < 10) {
      alert('Please enter a descriptive problem description (at least 10 characters).');
      return;
    }
    setLoadingAI(true);
    try {
      const res = await fetchApi('/ai/draft/', {
        method: 'POST',
        body: JSON.stringify({ raw_description: aiPrompt }),
      });
      if (res.title) setTitle(res.title);
      if (res.category) setCategory(res.category);
      if (res.requirements) setRequirements(res.requirements);
      if (res.suggested_prize?.recommended) setBudget(String(res.suggested_prize.recommended));
      setDescription(`${aiPrompt}\n\nDeliverables:\n` + (res.deliverables || []).join('\n'));
      alert('AI Challenge Architect generated your bounty specification!');
    } catch (e: any) {
      alert(e.message || 'AI assistant request failed. You can continue manually.');
    } finally {
      setLoadingAI(false);
    }
  };

  const handleAddRequirement = () => {
    if (newReq.trim()) {
      setRequirements([...requirements, newReq.trim()]);
      setNewReq('');
    }
  };

  const handleRemoveRequirement = (idx: number) => {
    setRequirements(requirements.filter((_, i) => i !== idx));
  };

  const handlePublish = async () => {
    if (!title.trim() || !description.trim()) {
      setErrorMsg('Title and description are required.');
      return;
    }
    setSubmitting(true);
    setErrorMsg('');
    try {
      const deadlineDate = new Date();
      deadlineDate.setDate(deadlineDate.getDate() + parseInt(deadlineDays || '14', 10));

      const payload = {
        title,
        description,
        category,
        budget: parseFloat(budget),
        currency: 'NGN',
        deadline: deadlineDate.toISOString(),
        requirements,
        ip_terms: ipTerms,
        rules,
      };

      const res = await fetchApi('/challenges/', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      // Automatically publish to OPEN
      await fetchApi(`/challenges/${res.id}/publish/`, { method: 'POST' });

      router.push(`/challenges/${res.id}`);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to create challenge.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Wizard Header */}
      <div className="border-b border-slate-200 pb-6 text-center">
        <h1 className="text-3xl font-extrabold text-slate-900">Post a Problem Bounty</h1>
        <p className="text-sm text-slate-600 mt-1">Structure your requirements, fund the prize pool, and attract Nigeria’s top solvers.</p>
        
        {/* Step Indicator */}
        <div className="flex items-center justify-center space-x-2 sm:space-x-4 mt-6 text-xs font-semibold">
          {['Problem & AI', 'Requirements', 'Prize & Rules', 'Preview & Publish'].map((label, idx) => {
            const stepNum = idx + 1;
            const isCurrent = step === stepNum;
            const isCompleted = step > stepNum;
            return (
              <div key={label} className="flex items-center space-x-2">
                <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                  isCurrent ? 'bg-emerald-600 text-white ring-4 ring-emerald-100' :
                  isCompleted ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-500'
                }`}>
                  {isCompleted ? <Check className="w-3.5 h-3.5" /> : stepNum}
                </div>
                <span className={`hidden sm:inline ${isCurrent ? 'text-slate-900 font-bold' : 'text-slate-500'}`}>{label}</span>
                {idx < 3 && <span className="text-slate-300">──</span>}
              </div>
            );
          })}
        </div>
      </div>

      {errorMsg && (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-800 text-xs rounded-xl">
          {errorMsg}
        </div>
      )}

      {/* Step 1: Problem & AI Assistant */}
      {step === 1 && (
        <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          {/* AI Challenge Architect Banner */}
          <div className="bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 rounded-xl p-5 space-y-3">
            <div className="flex items-center space-x-2 text-emerald-800 font-bold text-sm">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span>AI Challenge Architect (Optional Assistant)</span>
            </div>
            <p className="text-xs text-slate-600">
              Type your raw idea in plain English (e.g. <em>&quot;I need someone to create a dashboard showing our monthly sales and customer performance&quot;</em>) and let AI generate the title, deliverables, requirements, and prize benchmark.
            </p>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Describe what you need solved..."
                value={aiPrompt}
                onChange={(e) => setAiPrompt(e.target.value)}
                className="flex-1 px-3.5 py-2 text-xs bg-white border border-emerald-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
              <button
                onClick={handleRunAI}
                disabled={loadingAI}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors flex items-center space-x-1.5"
              >
                <Zap className="w-3.5 h-3.5" />
                <span>{loadingAI ? 'Generating...' : 'Auto-Draft'}</span>
              </button>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-900 mb-1">Challenge Title *</label>
              <input
                type="text"
                placeholder="e.g. Build a Monthly Sales & Customer Performance Dashboard"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-900 mb-1">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
              >
                <option>Software Engineering</option>
                <option>Data Analytics</option>
                <option>Mobile Development</option>
                <option>Design</option>
                <option>AI & ML</option>
                <option>Content & Marketing</option>
                <option>General</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-900 mb-1">Problem Description & Deliverables *</label>
              <textarea
                rows={6}
                placeholder="Detail the background, problem statement, key constraints, and expected output deliverables..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
                required
              />
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-100">
            <button
              onClick={() => {
                if (!title || !description) {
                  alert('Please enter a title and description.');
                  return;
                }
                setStep(2);
              }}
              className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-sm flex items-center space-x-1.5"
            >
              <span>Next: Requirements</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Requirements Checklist */}
      {step === 2 && (
        <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div>
            <h2 className="text-base font-bold text-slate-900">Define Verification Requirements</h2>
            <p className="text-xs text-slate-500 mt-1">Solvers will be evaluated against each requirement below before winner selection.</p>
          </div>

          <div className="space-y-3">
            {requirements.map((req, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-800 font-medium">{idx + 1}. {req}</span>
                <button
                  onClick={() => handleRemoveRequirement(idx)}
                  className="text-slate-400 hover:text-rose-600 p-1"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}

            <div className="flex gap-2 pt-2">
              <input
                type="text"
                placeholder="Add another requirement (e.g. Interactive drill-down filters)..."
                value={newReq}
                onChange={(e) => setNewReq(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddRequirement()}
                className="flex-1 px-3.5 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
              <button
                onClick={handleAddRequirement}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold rounded-lg flex items-center space-x-1"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add</span>
              </button>
            </div>
          </div>

          <div className="flex justify-between pt-4 border-t border-slate-100">
            <button
              onClick={() => setStep(1)}
              className="px-5 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 flex items-center space-x-1"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back</span>
            </button>
            <button
              onClick={() => setStep(3)}
              className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-sm flex items-center space-x-1.5"
            >
              <span>Next: Prize & Rules</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Prize, Deadline, Rules */}
      {step === 3 && (
        <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div>
            <h2 className="text-base font-bold text-slate-900">Prize, Timeline & Legal Terms</h2>
            <p className="text-xs text-slate-500 mt-1">Specify your reward amount and intellectual property transfer rules.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-900 mb-1">Prize Budget (NGN ₦) *</label>
              <input
                type="number"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                className="w-full px-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 font-bold"
                required
              />
              <span className="text-[11px] text-slate-500 mt-1 block">Platform fee (10%): ₦{(parseFloat(budget || '0') * 0.10).toLocaleString()}</span>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-900 mb-1">Duration (Days to Deadline)</label>
              <select
                value={deadlineDays}
                onChange={(e) => setDeadlineDays(e.target.value)}
                className="w-full px-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="3">3 Days (Sprint)</option>
                <option value="7">7 Days (1 Week)</option>
                <option value="14">14 Days (Standard)</option>
                <option value="30">30 Days (Deep Project)</option>
              </select>
            </div>
          </div>

          <div className="space-y-4 pt-2">
            <div>
              <label className="block text-xs font-bold text-slate-900 mb-1">Competition Rules</label>
              <textarea
                rows={2}
                value={rules}
                onChange={(e) => setRules(e.target.value)}
                className="w-full px-3.5 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-900 mb-1">IP Terms</label>
              <textarea
                rows={2}
                value={ipTerms}
                onChange={(e) => setIpTerms(e.target.value)}
                className="w-full px-3.5 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="flex justify-between pt-4 border-t border-slate-100">
            <button
              onClick={() => setStep(2)}
              className="px-5 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 flex items-center space-x-1"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back</span>
            </button>
            <button
              onClick={() => setStep(4)}
              className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-sm flex items-center space-x-1.5"
            >
              <span>Next: Preview Bounty</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Step 4: Preview & Publish */}
      {step === 4 && (
        <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-xs uppercase font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded border border-emerald-200">
              {category}
            </span>
            <h2 className="text-2xl font-extrabold text-slate-900 mt-2">{title}</h2>
            <div className="text-lg font-black text-emerald-600 mt-1">₦{Number(budget).toLocaleString()} Prize</div>
          </div>

          <div className="space-y-4 text-xs text-slate-700">
            <div>
              <h3 className="font-bold text-slate-900 uppercase tracking-wider mb-1">Description</h3>
              <p className="whitespace-pre-wrap">{description}</p>
            </div>

            <div>
              <h3 className="font-bold text-slate-900 uppercase tracking-wider mb-1">Requirements</h3>
              <ul className="list-disc pl-4 space-y-1">
                {requirements.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-200 flex items-center space-x-3 text-xs text-emerald-800">
            <ShieldCheck className="w-5 h-5 text-emerald-600 flex-shrink-0" />
            <div>
              <strong>Instant Escrow Publication:</strong> This challenge will immediately appear in the active bounties feed.
            </div>
          </div>

          <div className="flex justify-between pt-4 border-t border-slate-100">
            <button
              onClick={() => setStep(3)}
              className="px-5 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 flex items-center space-x-1"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back</span>
            </button>
            <button
              onClick={handlePublish}
              disabled={submitting}
              className="px-8 py-3 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold rounded-xl shadow-md transition-all flex items-center space-x-2"
            >
              <Trophy className="w-4 h-4" />
              <span>{submitting ? 'Publishing...' : 'Publish Challenge'}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
