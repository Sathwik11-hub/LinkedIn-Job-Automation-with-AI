"use client"

import { useState, useEffect } from 'react'
import { Upload, Rocket, CheckCircle, AlertCircle, Settings, TrendingUp } from 'lucide-react'

export default function AutoAgentHire() {
  const [file, setFile] = useState(null)
  const [isRunning, setIsRunning] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState(null)
  const [jobTitle, setJobTitle] = useState("AI Engineer")
  const [location, setLocation] = useState("Remote")
  
  // Animation states
  const [isVisible, setIsVisible] = useState(false)
  
  useEffect(() => {
    setIsVisible(true) // Trigger entrance animations
  }, [])
  
  // API Configuration
  const BACKEND_URL = "http://127.0.0.1:8000"
  
  const checkApiHealth = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/health`)
      return response.ok
    } catch {
      return false
    }
  }
  
  const runAutomation = async () => {
    setIsRunning(true)
    setProgress(0)
    
    try {
      const preferences = {
        job_title: jobTitle,
        location: location,
        experience_level: "mid",
        resume_path: "data/resumes/default_resume.txt"
      }
      
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 500)
      
      const response = await fetch(`${BACKEND_URL}/api/run-agent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ preferences })
      })
      
      clearInterval(progressInterval)
      setProgress(100)
      
      const result = await response.json()
      setResults(result)
      
      setTimeout(() => {
        setIsRunning(false)
        setProgress(0)
      }, 2000)
      
    } catch (error) {
      console.error('Error running automation:', error)
      setIsRunning(false)
      setProgress(0)
    }
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-purple-800 relative overflow-hidden">
      {/* Animated background particles */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Add floating particles or animated SVG background */}
        <div className="absolute top-10 left-10 w-4 h-4 bg-white/20 rounded-full animate-pulse"></div>
        <div className="absolute top-32 right-20 w-6 h-6 bg-white/10 rounded-full animate-bounce"></div>
        <div className="absolute bottom-20 left-1/4 w-8 h-8 bg-white/15 rounded-full animate-ping"></div>
      </div>
      
      {/* Hero Section */}
      <section className={`min-h-screen flex flex-col items-center justify-center px-4 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
        {/* Logo and Title */}
        <div className="text-center mb-12">
          <h1 className="text-6xl md:text-7xl font-bold text-white mb-4 bg-clip-text text-transparent bg-gradient-to-r from-white to-purple-200">
            🤖 AutoAgentHire
          </h1>
          <p className="text-xl md:text-2xl text-purple-100">
            AI-Powered LinkedIn Job Automation
          </p>
        </div>
        
        {/* Status Badges */}
        <div className="flex gap-4 mb-8">
          <StatusBadge status="success" text="API Connected" />
          <StatusBadge status="error" text="AI Not Configured" />
          <StatusBadge status="error" text="LinkedIn Not Configured" />
        </div>
        
        {/* Scroll indicator */}
        <div className="animate-bounce mt-8">
          <div className="text-white text-sm">Scroll to start ↓</div>
        </div>
      </section>
      
      {/* Quick Start Section */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <GlassCard>
          <h2 className="text-3xl font-bold text-gray-800 mb-4">
            🚀 Quick Start AutoAgent
          </h2>
          <p className="text-gray-600 mb-8">
            Start LinkedIn job automation with default settings or customize your preferences below.
          </p>
          
          <div className="grid md:grid-cols-3 gap-4 mb-6">
            <input
              type="text"
              placeholder="Job Title"
              className="px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-200 transition-all"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
            />
            <select 
              className="px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 transition-all"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            >
              <option value="Remote">Remote</option>
              <option value="United States">United States</option>
              <option value="India">India</option>
              <option value="Canada">Canada</option>
            </select>
            <button 
              onClick={runAutomation}
              disabled={isRunning}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:scale-105 hover:shadow-2xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isRunning ? '🔄 Running...' : '🚀 Start AutoAgent'}
            </button>
          </div>
        </GlassCard>
      </section>
      
      {/* Main Configuration Section */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Resume Upload */}
          <GlassCard>
            <h3 className="text-2xl font-bold text-gray-800 mb-6">
              📄 Upload Your Resume
            </h3>
            <FileUploadZone onFileSelect={setFile} />
            {file && (
              <div className="mt-4 p-4 bg-green-50 rounded-xl border border-green-200">
                <p className="text-green-800 font-semibold">✅ Resume uploaded: {file.name}</p>
              </div>
            )}
          </GlassCard>
          
          {/* Job Preferences */}
          <GlassCard>
            <h3 className="text-2xl font-bold text-gray-800 mb-6">
              ⚙️ Job Search Preferences
            </h3>
            <PreferencesTabs />
          </GlassCard>
        </div>
      </section>
      
      {/* Run Automation Button */}
      <section className="max-w-3xl mx-auto px-4 py-16">
        <button 
          onClick={runAutomation}
          disabled={isRunning}
          className="w-full px-8 py-6 bg-gradient-to-r from-purple-600 to-blue-600 text-white text-2xl font-bold rounded-2xl hover:scale-105 hover:shadow-2xl transition-all duration-300 relative overflow-hidden group disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span className="relative z-10">
            {isRunning ? '🔄 Running AutoAgent...' : '🚀 Run AutoAgent Automation'}
          </span>
          <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 transition-opacity" />
        </button>
      </section>
      
      {/* Results Section (conditional) */}
      {results && (
        <section className="max-w-7xl mx-auto px-4 py-16">
          <ResultsDisplay results={results} />
        </section>
      )}
      
      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-4xl font-bold text-white text-center mb-12">
          🎯 How AutoAgentHire Works
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon="📄"
            title="1. Upload Resume"
            description="Upload your PDF resume for AI-powered analysis and skill extraction"
          />
          <FeatureCard
            icon="🤖"
            title="2. AI Analysis"
            description="Gemini AI analyzes job compatibility and makes intelligent decisions"
          />
          <FeatureCard
            icon="🚀"
            title="3. Auto Apply"
            description="Automated applications to matching positions on LinkedIn"
          />
        </div>
      </section>
      
      {/* Progress Modal (conditional) */}
      {isRunning && (
        <ProgressModal progress={progress} onClose={() => setIsRunning(false)} />
      )}
    </div>
  )
}

// Reusable Components
function GlassCard({ children }) {
  return (
    <div className="bg-white/95 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20 hover:shadow-purple-500/20 transition-all duration-500">
      {children}
    </div>
  )
}

function StatusBadge({ status, text }) {
  const colors = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500'
  }
  
  return (
    <div className={`${colors[status]} text-white px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-2 animate-pulse`}>
      {status === 'success' ? '✅' : '⚠️'} {text}
    </div>
  )
}

function FileUploadZone({ onFileSelect }) {
  const [isDragging, setIsDragging] = useState(false)
  
  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file && file.type === 'application/pdf') {
      onFileSelect(file)
    }
  }
  
  const handleDrop = (event) => {
    event.preventDefault()
    setIsDragging(false)
    const file = event.dataTransfer.files[0]
    if (file && file.type === 'application/pdf') {
      onFileSelect(file)
    }
  }
  
  return (
    <div 
      className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 cursor-pointer ${
        isDragging 
          ? 'border-purple-500 bg-purple-50 scale-105' 
          : 'border-gray-300 hover:border-purple-400'
      }`}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      onClick={() => document.getElementById('file-input').click()}
    >
      <Upload className="w-16 h-16 mx-auto mb-4 text-purple-500 animate-bounce" />
      <p className="text-lg font-medium text-gray-700">
        Drop your resume here or click to browse
      </p>
      <p className="text-sm text-gray-500 mt-2">PDF format only</p>
      <input
        id="file-input"
        type="file"
        accept=".pdf"
        onChange={handleFileSelect}
        className="hidden"
      />
    </div>
  )
}

function PreferencesTabs() {
  const [activeTab, setActiveTab] = useState('basic')
  
  const tabs = [
    { id: 'basic', name: '🔍 Basic Search' },
    { id: 'details', name: '💼 Job Details' },
    { id: 'advanced', name: '🎯 Advanced' }
  ]
  
  return (
    <div>
      {/* Tab Navigation */}
      <div className="flex gap-2 mb-6 bg-gray-100 p-2 rounded-xl">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-purple-600 text-white shadow-lg'
                : 'text-gray-600 hover:bg-white'
            }`}
          >
            {tab.name}
          </button>
        ))}
      </div>
      
      {/* Tab Content */}
      <div className="space-y-4">
        {activeTab === 'basic' && (
          <>
            <input
              type="text"
              placeholder="Job Role/Keyword"
              className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 transition-all"
              defaultValue="AI Engineer"
            />
            <select className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 transition-all">
              <option>Remote</option>
              <option>India</option>
              <option>United States</option>
            </select>
            <textarea
              placeholder="Key Skills"
              className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 transition-all"
              defaultValue="Python, Machine Learning, AI, Data Science"
              rows="3"
            />
          </>
        )}
        
        {activeTab === 'details' && (
          <>
            <select className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 transition-all">
              <option>Any Experience Level</option>
              <option>Entry Level</option>
              <option>Mid-Senior Level</option>
              <option>Director</option>
            </select>
            <select className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 transition-all">
              <option>Full-time</option>
              <option>Part-time</option>
              <option>Contract</option>
            </select>
            <select className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 transition-all">
              <option>Any Salary</option>
              <option>$60,000+</option>
              <option>$80,000+</option>
              <option>$100,000+</option>
            </select>
          </>
        )}
        
        {activeTab === 'advanced' && (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Maximum Jobs: 15
              </label>
              <input
                type="range"
                min="1"
                max="50"
                defaultValue="15"
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Similarity Threshold: 60%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                defaultValue="60"
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
            <div className="flex items-center gap-3">
              <input type="checkbox" id="auto-apply" defaultChecked />
              <label htmlFor="auto-apply" className="text-gray-700 font-medium">
                🚀 Enable Automatic Applications
              </label>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="bg-white/95 backdrop-blur-xl rounded-2xl p-8 shadow-xl hover:scale-105 hover:shadow-2xl transition-all duration-300 group">
      <div className="text-5xl mb-4 group-hover:animate-bounce">{icon}</div>
      <h4 className="text-xl font-bold text-gray-800 mb-3">{title}</h4>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function ResultsDisplay({ results }) {
  if (!results || results.status !== 'success') {
    return (
      <GlassCard>
        <div className="text-center py-8">
          <AlertCircle className="w-16 h-16 mx-auto text-red-500 mb-4" />
          <h3 className="text-2xl font-bold text-gray-800 mb-2">Automation Failed</h3>
          <p className="text-gray-600">{results?.message || 'Unknown error occurred'}</p>
        </div>
      </GlassCard>
    )
  }
  
  const data = results.data || {}
  const executionSummary = results.execution_summary || {}
  
  return (
    <GlassCard>
      <div className="text-center mb-8">
        <CheckCircle className="w-16 h-16 mx-auto text-green-500 mb-4" />
        <h3 className="text-3xl font-bold text-gray-800 mb-2">✅ Automation Completed!</h3>
        <p className="text-gray-600">Your job automation has finished successfully</p>
      </div>
      
      {/* Metrics Grid */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <MetricCard
          label="Jobs Found"
          value={executionSummary.total_jobs_found || data.jobs_found || 0}
          icon="🔍"
        />
        <MetricCard
          label="Jobs Analyzed"
          value={data.jobs_analyzed || 0}
          icon="🤖"
        />
        <MetricCard
          label="Applications Submitted"
          value={executionSummary.applications_submitted || data.applications_attempted || 0}
          icon="📝"
        />
        <MetricCard
          label="Success Rate"
          value={`${executionSummary.success_rate || 0}%`}
          icon="📈"
        />
      </div>
      
      {/* Job Details */}
      {data.jobs && data.jobs.length > 0 && (
        <div>
          <h4 className="text-xl font-bold text-gray-800 mb-4">📋 Job Analysis Details</h4>
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {data.jobs.map((job, index) => (
              <JobCard key={index} job={job} index={index + 1} />
            ))}
          </div>
        </div>
      )}
    </GlassCard>
  )
}

function MetricCard({ label, value, icon }) {
  return (
    <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl p-6 text-center">
      <div className="text-3xl mb-2">{icon}</div>
      <div className="text-3xl font-bold text-purple-600 mb-1">{value}</div>
      <div className="text-sm text-gray-600">{label}</div>
    </div>
  )
}

function JobCard({ job, index }) {
  return (
    <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h5 className="text-lg font-bold text-gray-800">
            Job {index}: {job.title || 'Unknown Title'}
          </h5>
          <p className="text-gray-600">{job.company || 'Unknown Company'}</p>
          <p className="text-sm text-gray-500">📍 {job.location || 'N/A'}</p>
        </div>
        <div className="text-right">
          {job.applied ? (
            <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
              ✅ Applied
            </span>
          ) : (
            <span className="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm">
              ℹ️ Not Applied
            </span>
          )}
        </div>
      </div>
      
      {job.analysis && (
        <div className="mt-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-sm font-medium text-gray-700">Similarity Score:</span>
            <div className="flex-1 bg-gray-200 rounded-full h-2">
              <div 
                className="bg-purple-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${job.analysis.similarity_score || 0}%` }}
              />
            </div>
            <span className="text-sm font-bold text-purple-600">
              {job.analysis.similarity_score || 0}%
            </span>
          </div>
          {job.analysis.analysis && (
            <p className="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg">
              💡 {job.analysis.analysis}
            </p>
          )}
        </div>
      )}
      
      {job.url && (
        <a 
          href={job.url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 mt-4 text-purple-600 hover:text-purple-800 font-medium"
        >
          🔗 View Job Posting
        </a>
      )}
    </div>
  )
}

function ProgressModal({ progress, onClose }) {
  const getStatusText = () => {
    if (progress < 20) return "🔐 Logging into LinkedIn..."
    if (progress < 40) return "🔍 Searching for jobs..."
    if (progress < 70) return "🤖 Analyzing job compatibility..."
    if (progress < 90) return "📝 Processing applications..."
    return "✅ Completing automation..."
  }
  
  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50">
      <div className="bg-white rounded-3xl p-12 max-w-2xl w-full mx-4 shadow-2xl">
        <h3 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          🤖 Running Automation...
        </h3>
        
        {/* Animated progress bar */}
        <div className="w-full bg-gray-200 rounded-full h-4 mb-4 overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-purple-600 to-blue-600 transition-all duration-500 rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>
        
        <p className="text-center text-gray-600 text-lg mb-4">
          {progress}% Complete
        </p>
        
        <p className="text-center text-gray-500">
          {getStatusText()}
        </p>
        
        {/* Cancel button */}
        <div className="flex justify-center mt-8">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-200 text-gray-700 rounded-xl hover:bg-gray-300 transition-all"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}