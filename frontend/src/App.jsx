import { useState } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ApiProvider } from './context/ApiContext'
import Header from './components/layout/Header'
import Footer from './components/layout/Footer'
import ClassifyTab from './components/classification/ClassifyTab'
import DetectTab from './components/detection/DetectTab'

const queryClient = new QueryClient({
  defaultOptions: { mutations: { retry: 0 } },
})

const TABS = [
  { id: 'cls', label: 'Clasificación', icon: '🔬', component: ClassifyTab },
  { id: 'det', label: 'Detección',     icon: '📍', component: DetectTab   },
]

export default function App() {
  const [activeTab, setActiveTab] = useState('cls')

  const ActivePanel = TABS.find((t) => t.id === activeTab)?.component

  return (
    <QueryClientProvider client={queryClient}>
      <ApiProvider>
        <div className="relative z-10 max-w-3xl mx-auto px-5 pb-16">
          <Header />

          {/* Tab nav */}
          <nav className="flex border-b border-border mb-8" role="tablist">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                role="tab"
                aria-selected={activeTab === tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  relative px-7 py-3.5 text-sm font-semibold tracking-wide transition-colors duration-200
                  after:absolute after:bottom-[-1px] after:left-0 after:right-0 after:h-0.5
                  after:rounded-t after:transition-transform after:duration-300
                  ${activeTab === tab.id
                    ? 'text-teal after:bg-teal after:scale-x-100'
                    : 'text-text-dim hover:text-white after:bg-teal after:scale-x-0'}
                `}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>

          {/* Active panel */}
          {ActivePanel && <ActivePanel />}

          <Footer />
        </div>
      </ApiProvider>
    </QueryClientProvider>
  )
}
