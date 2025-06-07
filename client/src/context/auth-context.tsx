"use client"

import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from "react"
import API from "@/api"

interface User {
  email: string
  first_name: string
  last_name: string
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (
    first_name: string,
    last_name: string,
    email: string,
    password: string
  ) => Promise<void>
  logout: () => void
  authMessage: string | null
  errorMessage: string | null
  clearMessages: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [authMessage, setAuthMessage] = useState<string | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const isAuthenticated = !!user

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem("auth_token")
      if (token) {
        try {
          await API.refreshAccessToken()
          const response = await API.infoUser()
          setUser(response.data)
        } catch {
          localStorage.removeItem("auth_token")
          setUser(null)
        }
      }
      setIsLoading(false)
    }

    initAuth()
  }, [])

  const clearMessages = () => {
    setAuthMessage(null)
    setErrorMessage(null)
  }

  const login = async (email: string, password: string) => {
    clearMessages()
    try {
      const token = await API.loginUser(email, password)
      localStorage.setItem("auth_token", token)

      const response = await API.infoUser()
      setUser(response.data)

      setAuthMessage(`Добро пожаловать, ${response.data.first_name}!`)
    } catch (error: any) {
      setErrorMessage(error.message || "Неверные учетные данные")
      throw error
    }
  }

  const register = async (
    first_name: string,
    last_name: string,
    email: string,
    password: string
  ) => {
    clearMessages()
    try {
      const token = await API.registerUser(first_name, last_name, email, password)
      localStorage.setItem("auth_token", token)

      const response = await API.infoUser()
      setUser(response.data)

      setAuthMessage(`Добро пожаловать, ${first_name}!`)
    } catch (error: any) {
      setErrorMessage(error.message || "Не удалось создать аккаунт")
      throw error
    }
  }

  const logout = async () => {
    try {
      await API.logout()
    } catch {
      // Даже если logout неудачный — всё равно очищаем
    }
    localStorage.removeItem("auth_token")
    setUser(null)
    clearMessages()
    setAuthMessage("Вы успешно вышли из системы")
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated,
        login,
        register,
        logout,
        authMessage,
        errorMessage,
        clearMessages,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
