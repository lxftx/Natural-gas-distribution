"use client"

import { useState, type FormEvent, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, Eye, EyeOff } from "lucide-react"
import { useAuth } from "@/context/auth-context"
import { useNavigate } from "react-router-dom";

function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate();

  const {
    login,
    authMessage,
    errorMessage,
    clearMessages,
    isAuthenticated,  // добавим, чтобы отследить успешный вход
  } = useAuth()

  // После успешного входа - редирект
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/solver")
    }
  }, [isAuthenticated, navigate])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    clearMessages()

    try {
      await login(email, password)
    } catch {
      // Ошибка уже отображается через errorMessage
    } finally {
      setIsLoading(false)
    }
  }

  return (
    // Центрируем контейнер по середине экрана
    <div className="flex items-center justify-center min-h-screen bg-gray-50 px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Вход в систему</CardTitle>
          <CardDescription>Введите ваши учетные данные для входа</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Пароль</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Введите пароль"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={isLoading}
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </Button>
              </div>
            </div>

            {authMessage && (
              <p className="text-green-600 text-sm">{authMessage}</p>
            )}
            {errorMessage && (
              <p className="text-red-600 text-sm">{errorMessage}</p>
            )}

            {/* Черная кнопка */}
            <Button
              type="submit"
              className="w-full bg-black text-white hover:bg-gray-800"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Вход...
                </>
              ) : (
                "Войти"
              )}
            </Button>

            <div className="text-center text-sm">
              <span className="text-gray-600">Нет аккаунта? </span>
              <Button
                type="button"
                variant="link"
                className="p-0 h-auto font-normal"
                onClick={() => navigate("/register")}
                disabled={isLoading}
              >
                Зарегистрироваться
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default LoginForm
