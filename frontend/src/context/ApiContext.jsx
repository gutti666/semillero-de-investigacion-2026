import { createContext, useContext } from 'react'
import { setApiBase } from '../api/algae'

const API_BASE = (import.meta.env.VITE_API_BASE ?? 'http://localhost:8000').replace(/\/$/, '')

// Apply the fixed base URL to the axios client at startup
setApiBase(API_BASE)

const ApiContext = createContext({ apiBase: API_BASE })

export function ApiProvider({ children }) {
  return (
    <ApiContext.Provider value={{ apiBase: API_BASE }}>
      {children}
    </ApiContext.Provider>
  )
}

export function useApi() {
  const ctx = useContext(ApiContext)
  if (!ctx) throw new Error('useApi must be inside ApiProvider')
  return ctx
}
