import React, { useState } from 'react';
import { 
  Beaker,
  Search,
  Settings,
  Bell,
  User,
  Layout,
  PlayCircle,
  History,
  BarChart3,
  FileText,
  Settings2,
  LayoutList,
  Terminal
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

function Analytics() {
  const navigate = useNavigate();
  const [viewMode, setViewMode] = useState<'log' | 'formatted'>('log');

  const logContent = `🚀 Starting automated test execution
📋 Loading test cases from: C:/Users/dange/OneDrive/Desktop/Work/6th sem/playwright_tests.json
✅ Successfully loaded 14 tests from C:/Users/dange/OneDrive/Desktop/Work/6th sem/playwright_tests.json
🌐 Base URL: https://krishi-mitra-front.vercel.app/
⏱ Running: Landing Page - Verify 'Fresh From Farm to Table' text
  Step 1: navigate with value 'https://krishi-mitra-front.vercel.app/'
  Step 2: expect with 2 selectors with value 'to be visible'
✅ Landing Page - Verify 'Fresh From Farm to Table' text passed!
⏱ Running: Landing Page - Verify 'Let's Get Started' button redirects to /auth
  Step 1: navigate with value 'https://krishi-mitra-front.vercel.app/'
  Step 2: wait with 2 selectors with value 'visible'
    🔍 Trying with selector: 'text=Let's Get Started'
    ✅ Selector worked: 'text=Let's Get Started'
  Step 3: click with 2 selectors
    🔍 Trying with selector: 'text=Let's Get Started'
    ✅ Selector worked: 'text=Let's Get Started'
    🔄 Waiting for navigation after form submission...
    ⚠ No navigation occurred after form submission. URL: https://krishi-mitra-front.vercel.app/autth
    🔍 Debugging authentication failure:
    📸 Auth debug screenshot: auth_debug_Landing_Page_-Verify'Let's_Get_Started'button_redirects_to/auth.png
  Step 4: expect with 5 selectors with value 'to be visible'
  Step 5: expect with value 'url to be /auth'
✅ Landing Page - Verify 'Let's Get Started' button redirects to /auth passed!`;

  const formattedContent = {
    summary: {
      totalTests: 4,
      sourceFile: "playwright_tests.json",
      baseUrl: "https://krishi-mitra-front.vercel.app/",
      status: "All tests passed, but there are navigation issues during authentication."
    },
    tests: [
      {
        name: "Landing Page - Verify 'Fresh From Farm to Table' text",
        status: "Passed",
        steps: [
          "Navigated to the base URL",
          "Verified that the 'Fresh From Farm to Table' text is visible"
        ]
      },
      {
        name: "Landing Page - Verify 'Let's Get Started' button redirects to /auth",
        status: "Passed",
        steps: [
          "Navigated to the base URL",
          "Clicked the 'Let's Get Started' button"
        ],
        issues: [
          "The navigation after clicking the button resulted in the URL 'https://krishi-mitra-front.vercel.app/autth' instead of 'https://krishi-mitra-front.vercel.app/auth'"
        ]
      }
    ],
    observations: [
      "There's a consistent issue with the navigation after the 'Let's Get Started' button click and login attempts",
      "The URL in the logs shows 'autth' instead of 'auth' or 'shop'",
      "This suggests a potential bug in the website's routing or a typo in the test setup"
    ]
  };

  return (
    <div className="min-h-screen bg-[#111] flex">
      {/* Sidebar */}
      <div className="w-64 bg-[#1a1a1a] border-r border-gray-800">
        <div className="p-4">
          <div className="flex items-center space-x-2">
            <Beaker className="h-8 w-8 text-[#a855f7]" />
            <span className="text-xl font-bold text-white">Testify</span>
          </div>
        </div>
        <nav className="mt-8">
          <div className="px-4 space-y-1">
            {[
              { icon: <Layout className="h-5 w-5" />, label: 'Dashboard', path: '/dashboard' },
              { icon: <PlayCircle className="h-5 w-5" />, label: 'Tests', path: '/tests' },
              { icon: <History className="h-5 w-5" />, label: 'History', path: '/history' },
              { icon: <BarChart3 className="h-5 w-5" />, label: 'Analytics', path: '/analytics', active: true },
              { icon: <FileText className="h-5 w-5" />, label: 'Reports', path: '/reports' },
              { icon: <Settings2 className="h-5 w-5" />, label: 'Settings', path: '/settings' }
            ].map((item) => (
              <button
                key={item.label}
                onClick={() => item.path && navigate(item.path)}
                className={`flex items-center space-x-3 w-full px-4 py-2 text-sm font-medium rounded-lg ${
                  item.active 
                    ? 'bg-[#a855f7] text-white' 
                    : 'text-gray-400 hover:bg-[#222] hover:text-white'
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            ))}
          </div>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        {/* Header */}
        <header className="bg-[#1a1a1a] border-b border-gray-800">
          <div className="flex items-center justify-between px-8 py-4">
            <div className="flex items-center flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search analytics..."
                  className="pl-10 pr-4 py-2 w-64 bg-[#222] border border-gray-800 rounded-lg text-gray-300 focus:outline-none focus:border-[#a855f7]"
                />
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-white">
                <Bell className="h-5 w-5" />
              </button>
              <button className="p-2 text-gray-400 hover:text-white">
                <Settings className="h-5 w-5" />
              </button>
              <button className="flex items-center space-x-2 p-2 text-gray-400 hover:text-white">
                <User className="h-5 w-5" />
                <span>Profile</span>
              </button>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="p-8">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold text-white mb-2">Test Results</h1>
              <p className="text-gray-400">View detailed test execution logs and analysis</p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setViewMode('log')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                  viewMode === 'log'
                    ? 'bg-[#a855f7] text-white'
                    : 'bg-[#222] text-gray-400 hover:text-white'
                }`}
              >
                <Terminal className="h-4 w-4" />
                <span>Log View</span>
              </button>
              <button
                onClick={() => setViewMode('formatted')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                  viewMode === 'formatted'
                    ? 'bg-[#a855f7] text-white'
                    : 'bg-[#222] text-gray-400 hover:text-white'
                }`}
              >
                <LayoutList className="h-4 w-4" />
                <span>Formatted View</span>
              </button>
            </div>
          </div>

          {viewMode === 'log' ? (
            <div className="bg-[#1a1a1a] rounded-xl border border-gray-800 overflow-hidden">
              <pre className="p-6 text-gray-300 font-mono text-sm whitespace-pre-wrap">
                {logContent}
              </pre>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Summary */}
              <div className="bg-[#1a1a1a] rounded-xl border border-gray-800 p-6">
                <h2 className="text-xl font-semibold text-white mb-4">Test Execution Summary</h2>
                <div className="space-y-2">
                  <p className="text-gray-300">Total Tests Run: {formattedContent.summary.totalTests}</p>
                  <p className="text-gray-300">Source File: {formattedContent.summary.sourceFile}</p>
                  <p className="text-gray-300">Base URL: {formattedContent.summary.baseUrl}</p>
                  <p className="text-gray-300">Status: {formattedContent.summary.status}</p>
                </div>
              </div>

              {/* Test Details */}
              <div className="bg-[#1a1a1a] rounded-xl border border-gray-800 p-6">
                <h2 className="text-xl font-semibold text-white mb-4">Test Details</h2>
                <div className="space-y-6">
                  {formattedContent.tests.map((test, index) => (
                    <div key={index} className="border-t border-gray-800 pt-4 first:border-0 first:pt-0">
                      <h3 className="text-lg font-medium text-white mb-2">{test.name}</h3>
                      <p className="text-green-400 mb-2">Status: {test.status}</p>
                      <div className="space-y-1">
                        <p className="text-gray-400">Steps:</p>
                        <ul className="list-disc list-inside text-gray-300 ml-4">
                          {test.steps.map((step, stepIndex) => (
                            <li key={stepIndex}>{step}</li>
                          ))}
                        </ul>
                        {test.issues && (
                          <div className="mt-2">
                            <p className="text-yellow-400">Issues:</p>
                            <ul className="list-disc list-inside text-gray-300 ml-4">
                              {test.issues.map((issue, issueIndex) => (
                                <li key={issueIndex}>{issue}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Observations */}
              <div className="bg-[#1a1a1a] rounded-xl border border-gray-800 p-6">
                <h2 className="text-xl font-semibold text-white mb-4">Important Observations</h2>
                <ul className="list-disc list-inside text-gray-300 ml-4">
                  {formattedContent.observations.map((observation, index) => (
                    <li key={index}>{observation}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default Analytics;