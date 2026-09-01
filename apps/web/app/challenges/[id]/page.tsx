'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { fetchApi } from '@/lib/api';
import {
  Trophy,
  Clock,
  CheckCircle2,
  Calendar,
  DollarSign,
  ShieldCheck,
  Send,
  ExternalLink,
  Github,
  AlertCircle,
  Award,
  CreditCard,
  CheckCircle
} from 'lucide-react';

export default function ChallengeDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const [challenge, setChallenge] = useState<any>(null);
  const [submissions, setSubmissions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [funding, setFunding] = useState(false);
  const [verifyingPayment, setVerifyingPayment] = useState(false);

  // Submit form state
  const [subTitle, setSubTitle] = useState('');
  const [subContent, setSubContent] = useState('');
  const [subGithub, setSubGithub] = useState('');
  const [subDemo, setSubDemo] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const loadData = async () => {
    try {
      const cData = await fetchApi(`/challenges/${id}/`);
      setChallenge(cData);

      if (user) {
        try {
          const sData = await fetchApi(`/challenges/${id}/submissions/`);
          setSubmissions(sData || []);
        } catch (e) {}
      }
    } catch (e: any) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (id) loadData();
  }, [id, user]);

  // Handle Paystack redirect callback verification
  useEffect(() => {
    if (typeof window === 'undefined' || !id) return;
    const params = new URLSearchParams(window.location.search);
    const ref = params.get('reference') || params.get('trxref');

    if (ref) {
      const verifyPayment = async () => {
        setVerifyingPayment(true);
        try {
          await fetchApi(`/payments/verify/${ref}/`);
          setSuccessMsg('🎉 Escrow Payment Verified! Your bounty has been funded and is now OPEN for submissions.');
          // Remove query params cleanly from browser URL
          window.history.replaceState({}, '', window.location.pathname);
          await loadData();
        } catch (err: any) {
          setErrorMsg(err.message || 'Payment verification failed with Paystack. Please check with support.');
        } finally {
          setVerifyingPayment(false);
        }
      };
      verifyPayment();
    }
  }, [id]);

  const handleSubmitSolution = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!subContent.trim()) {
      setErrorMsg('Please describe your proposed solution.');
      return;
    }
    setSubmitting(true);
    setErrorMsg('');
    try {
      await fetchApi(`/challenges/${id}/submissions/`, {
        method: 'POST',
        body: JSON.stringify({
          title: subTitle || 'Solution Proposal',
          content: subContent,
          github_repo_url: subGithub,
          live_demo_url: subDemo,
        }),
      });
      setSuccessMsg('Solution submitted successfully!');
      loadData();
    } catch (err: any) {
      setErrorMsg(err.message || 'Submission failed.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleSelectWinner = async (subId: string) => {
    if (!confirm('Are you sure you want to select this submission as the winning solution?')) return;
    try {
      await fetchApi(`/challenges/${id}/select-winner/`, {
        method: 'POST',
        body: JSON.stringify({ submission_id: subId, reason: 'Selected by poster' }),
      });
      alert('Winner selected successfully! Payout processing initiated.');
      loadData();
    } catch (err: any) {
      alert(err.message || 'Failed to select winner.');
    }
  };

  const handleFundChallenge = async () => {
    setFunding(true);
    setErrorMsg('');
    try {
      const res = await fetchApi('/payments/initialize/', {
        method: 'POST',
        body: JSON.stringify({
          challenge_id: id,
          callback_url: `${window.location.origin}/challenges/${id}?payment_verify=1`
        }),
      });
      if (res.authorization_url) {
        window.location.href = res.authorization_url;
      } else {
        setErrorMsg('Unable to obtain Paystack checkout link.');
        setFunding(false);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Payment initialization failed.');
      setFunding(false);
    }
  };

  if (loading) {
    return <div className="max-w-5xl mx-auto px-4 py-16 text-center text-sm text-slate-500">Loading challenge details...</div>;
  }

  if (!challenge) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16 text-center">
        <p className="text-lg font-bold text-slate-800">Challenge not found.</p>
        <Link href="/challenges" className="mt-4 inline-block text-emerald-600 text-sm font-medium">← Back to challenges</Link>
      </div>
    );
  }

  const isPoster = user && challenge.poster?.id === user.id;
  const isFundedOrOpen = challenge.status === 'OPEN' || challenge.status === 'FUNDED' || challenge.status === 'COMPLETED' || challenge.status === 'WINNER_SELECTED';

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Breadcrumb */}
      <div className="text-xs text-slate-500">
        <Link href="/challenges" className="hover:text-emerald-600">Challenges</Link>
        <span className="mx-2">/</span>
        <span className="text-slate-900 font-medium">{challenge.title}</span>
      </div>

      {/* Verification Notification Banner */}
      {verifyingPayment && (
        <div className="p-4 bg-emerald-50 border border-emerald-300 text-emerald-900 text-xs rounded-xl flex items-center space-x-2">
          <Clock className="w-4 h-4 animate-spin text-emerald-600" />
          <span>Verifying Paystack transaction and funding escrow...</span>
        </div>
      )}

      {successMsg && (
        <div className="p-4 bg-emerald-50 border border-emerald-300 text-emerald-900 text-sm rounded-xl flex items-center space-x-2">
          <CheckCircle className="w-5 h-5 text-emerald-600 flex-shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {errorMsg && (
        <div className="p-4 bg-rose-50 border border-rose-300 text-rose-900 text-sm rounded-xl flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Specification Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Header Card */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-semibold">
                {challenge.category}
              </span>
              <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                challenge.status === 'OPEN' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                challenge.status === 'PENDING_PAYMENT' || challenge.status === 'DRAFT' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                'bg-slate-100 text-slate-700'
              }`}>
                {challenge.status}
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">{challenge.title}</h1>

            <div className="flex items-center text-xs text-slate-500 space-x-4 border-t border-slate-100 pt-3">
              <span>Posted by: <strong className="text-slate-800">{challenge.poster?.full_name || challenge.poster?.email}</strong></span>
              <span>•</span>
              <span className="flex items-center"><Calendar className="w-3.5 h-3.5 mr-1" /> Deadline: {new Date(challenge.deadline).toLocaleDateString()}</span>
            </div>
          </div>

          {/* Unfunded Warning for Poster */}
          {isPoster && !isFundedOrOpen && (
            <div className="bg-amber-50 border border-amber-300 rounded-xl p-5 space-y-3">
              <div className="flex items-center space-x-2 text-amber-900 font-bold text-sm">
                <AlertCircle className="w-5 h-5 text-amber-600" />
                <span>Action Required: Escrow Funding Pending</span>
              </div>
              <p className="text-xs text-amber-800 leading-relaxed">
                This bounty is currently hidden from solvers until the prize is deposited into Paystack escrow. 
                Once paid, solvers can begin submitting solutions.
              </p>
              <button
                onClick={handleFundChallenge}
                disabled={funding}
                className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg shadow-sm flex items-center space-x-2 transition-all"
              >
                <CreditCard className="w-4 h-4" />
                <span>{funding ? 'Connecting to Paystack...' : `Pay ₦${(Number(challenge.budget) + Number(challenge.platform_fee || 0)).toLocaleString()} via Paystack`}</span>
              </button>
            </div>
          )}

          {/* Description & Problem */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <h2 className="text-base font-bold text-slate-900">The Problem & Objectives</h2>
            <p className="text-sm text-slate-700 whitespace-pre-wrap leading-relaxed">{challenge.description}</p>

            {challenge.skills?.length > 0 && (
              <div className="pt-2">
                <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-2">Required Skills</h3>
                <div className="flex flex-wrap gap-1.5">
                  {challenge.skills.map((s: any) => (
                    <span key={s.id} className="text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-1 rounded-md font-medium">
                      {s.name}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Requirements Checklist */}
          {challenge.requirements?.length > 0 && (
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <h2 className="text-base font-bold text-slate-900">Evaluation Criteria & Requirements</h2>
              <div className="space-y-2.5">
                {challenge.requirements.map((req: any, idx: number) => (
                  <div key={req.id || idx} className="flex items-start space-x-2.5 text-sm text-slate-700">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 flex-shrink-0" />
                    <span>{req.description}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Terms & IP */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <h2 className="text-base font-bold text-slate-900">Terms, Rules & IP Ownership</h2>
            <div className="space-y-3 text-xs text-slate-600">
              {challenge.ip_terms && (
                <div>
                  <strong className="text-slate-800">Intellectual Property:</strong> {challenge.ip_terms}
                </div>
              )}
              {challenge.rules && (
                <div>
                  <strong className="text-slate-800">Rules & Integrity:</strong> {challenge.rules}
                </div>
              )}
            </div>
          </div>

          {/* Submissions Section (for Poster or Solvers) */}
          {(isPoster || challenge.selected_winner) && (
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <h2 className="text-base font-bold text-slate-900">
                Submissions ({submissions.length})
              </h2>

              {submissions.length === 0 ? (
                <div className="p-8 text-center text-xs text-slate-500 bg-slate-50 rounded-lg">
                  No submissions yet. Solvers are working on solutions.
                </div>
              ) : (
                <div className="space-y-4">
                  {submissions.map((sub: any) => (
                    <div
                      key={sub.id}
                      className={`p-4 rounded-xl border ${
                        sub.status === 'WINNER' ? 'border-amber-400 bg-amber-50/40' : 'border-slate-200 bg-white'
                      } space-y-3`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="text-sm font-bold text-slate-900">{sub.title}</h4>
                          <span className="text-xs text-slate-500">By {sub.solver?.full_name || sub.solver?.email}</span>
                        </div>
                        {sub.status === 'WINNER' ? (
                          <span className="px-2.5 py-1 bg-amber-500 text-white font-bold text-xs rounded-full flex items-center space-x-1">
                            <Award className="w-3.5 h-3.5 mr-1" /> Selected Winner
                          </span>
                        ) : (
                          <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">
                            {sub.status}
                          </span>
                        )}
                      </div>

                      <p className="text-xs text-slate-700 whitespace-pre-wrap">{sub.content}</p>

                      <div className="flex items-center space-x-4 text-xs pt-1">
                        {sub.github_repo_url && (
                          <a href={sub.github_repo_url} target="_blank" rel="noreferrer" className="text-slate-700 hover:text-emerald-600 flex items-center">
                            <Github className="w-3.5 h-3.5 mr-1" /> Source Code
                          </a>
                        )}
                        {sub.live_demo_url && (
                          <a href={sub.live_demo_url} target="_blank" rel="noreferrer" className="text-emerald-700 hover:underline flex items-center font-medium">
                            <ExternalLink className="w-3.5 h-3.5 mr-1" /> Live Demo
                          </a>
                        )}
                      </div>

                      {isPoster && challenge.status === 'OPEN' && sub.status !== 'WINNER' && (
                        <div className="pt-2">
                          <button
                            onClick={() => handleSelectWinner(sub.id)}
                            className="px-3.5 py-1.5 bg-amber-500 hover:bg-amber-600 text-white text-xs font-semibold rounded-lg shadow-sm flex items-center space-x-1"
                          >
                            <Award className="w-3.5 h-3.5" />
                            <span>Select as Winner & Release Escrow</span>
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Sidebar: Prize Box & Actions */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
            <div>
              <div className="text-xs font-bold uppercase tracking-wider text-slate-500">Guaranteed Prize</div>
              <div className="text-3xl font-black text-slate-900 mt-1">
                {challenge.currency} {Number(challenge.budget).toLocaleString()}
              </div>
              <div className="text-xs text-emerald-700 font-medium flex items-center mt-1">
                <ShieldCheck className="w-4 h-4 mr-1 text-emerald-600" />
                {isFundedOrOpen ? 'Pre-funded in Paystack Escrow' : 'Awaiting Poster Escrow Deposit'}
              </div>
            </div>

            {/* Poster Funding Action if DRAFT/PENDING */}
            {isPoster && !isFundedOrOpen && (
              <div className="border-t border-slate-100 pt-5 space-y-4">
                <div className="text-xs font-bold text-slate-800">Deposit Summary</div>
                <div className="space-y-1.5 text-xs text-slate-600">
                  <div className="flex justify-between">
                    <span>Bounty Prize:</span>
                    <span>{challenge.currency} {Number(challenge.budget).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Platform Fee:</span>
                    <span>{challenge.currency} {Number(challenge.platform_fee || 0).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between font-bold text-slate-900 border-t border-slate-200 pt-1.5">
                    <span>Total Deposit:</span>
                    <span className="text-emerald-600">{challenge.currency} {(Number(challenge.budget) + Number(challenge.platform_fee || 0)).toLocaleString()}</span>
                  </div>
                </div>
                <button
                  onClick={handleFundChallenge}
                  disabled={funding}
                  className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold rounded-xl shadow-sm transition-colors flex items-center justify-center space-x-2"
                >
                  <CreditCard className="w-4 h-4" />
                  <span>{funding ? 'Redirecting to Paystack...' : 'Fund & Open Bounty'}</span>
                </button>
              </div>
            )}

            {/* Solver Submission Box */}
            {!isPoster && challenge.status === 'OPEN' && (
              <div className="border-t border-slate-100 pt-6 space-y-4">
                <h3 className="text-sm font-bold text-slate-900">Submit Your Solution</h3>

                {user ? (
                  <form onSubmit={handleSubmitSolution} className="space-y-3">
                    <div>
                      <label className="block text-xs font-medium text-slate-700 mb-1">Proposal Title</label>
                      <input
                        type="text"
                        placeholder="e.g. Clean PowerBI Dashboard & SQL Model"
                        value={subTitle}
                        onChange={(e) => setSubTitle(e.target.value)}
                        className="w-full px-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-slate-700 mb-1">Detailed Explanation / Proof of Work</label>
                      <textarea
                        rows={4}
                        placeholder="Describe your implementation, architecture, and results..."
                        value={subContent}
                        onChange={(e) => setSubContent(e.target.value)}
                        className="w-full px-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-slate-700 mb-1">GitHub / Code Repo URL (Optional)</label>
                      <input
                        type="url"
                        placeholder="https://github.com/..."
                        value={subGithub}
                        onChange={(e) => setSubGithub(e.target.value)}
                        className="w-full px-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-slate-700 mb-1">Live Demo / Dashboard URL (Optional)</label>
                      <input
                        type="url"
                        placeholder="https://my-demo-link.com"
                        value={subDemo}
                        onChange={(e) => setSubDemo(e.target.value)}
                        className="w-full px-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                      />
                    </div>

                    <button
                      type="submit"
                      disabled={submitting}
                      className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-sm flex items-center justify-center space-x-1.5 transition-colors"
                    >
                      <Send className="w-3.5 h-3.5" />
                      <span>{submitting ? 'Submitting...' : 'Submit Solution Proposal'}</span>
                    </button>
                  </form>
                ) : (
                  <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg text-center space-y-2">
                    <p className="text-xs text-slate-600">Please sign in as a Solver to submit your solution.</p>
                    <Link
                      href="/auth/login"
                      className="inline-block px-4 py-2 bg-emerald-600 text-white text-xs font-semibold rounded-lg"
                    >
                      Sign In to Compete
                    </Link>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
