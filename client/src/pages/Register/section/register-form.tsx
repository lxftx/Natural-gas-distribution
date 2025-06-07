"use client"

import { useState, type FormEvent, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, Eye, EyeOff } from "lucide-react"
import { useAuth } from "@/context/auth-context"
import { useNavigate } from "react-router-dom";

function RegisterForm() {
  const [email, setEmail] = useState("")
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate();

  const { 
    register, 
    authMessage,
    errorMessage,
    clearMessages,
    isAuthenticated,
  } = useAuth()

  useEffect(() => {
      if (isAuthenticated) {
      navigate("/solver")
      }
  }, [isAuthenticated, navigate])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()

    if (password !== confirmPassword) {
      return
    }

    if (password.length < 6) {
      return
    }

    setIsLoading(true)
    clearMessages()

    try {
      await register(firstName, lastName, email, password)
    } catch (error) {
      // Ошибка уже обработана в контексте
    } finally {
      setIsLoading(false)
    }
  }

  const passwordsMatch = password === confirmPassword
  const passwordValid = password.length >= 6

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 px-4">
        <Card className="w-full max-w-md">
            <CardHeader className="text-center">
                <CardTitle className="text-2xl">Регистрация</CardTitle>
                <CardDescription>Создайте новый аккаунт для доступа к системе</CardDescription>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="first_name">Имя</Label>
                    <Input
                    id="first_name"
                    type="text"
                    placeholder="Ваше имя"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                    disabled={isLoading}
                    />
                </div>

                <div className="space-y-2">
                    <Label htmlFor="last_name">Фамилия</Label>
                    <Input
                    id="last_name"
                    type="text"
                    placeholder="Ваша фамилия"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                    disabled={isLoading}
                    />
                </div>

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
                        placeholder="Минимум 6 символов"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={isLoading}
                        className={!passwordValid && password.length > 0 ? "border-red-500" : ""}
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
                    {!passwordValid && password.length > 0 && (
                    <p className="text-sm text-red-500">Пароль должен содержать минимум 6 символов</p>
                    )}
                </div>

                <div className="space-y-2">
                    <Label htmlFor="confirmPassword">Подтвердите пароль</Label>
                    <div className="relative">
                    <Input
                        id="confirmPassword"
                        type={showConfirmPassword ? "text" : "password"}
                        placeholder="Повторите пароль"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                        disabled={isLoading}
                        className={!passwordsMatch && confirmPassword.length > 0 ? "border-red-500" : ""}
                    />
                    <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        disabled={isLoading}
                    >
                        {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </Button>
                    </div>
                    {!passwordsMatch && confirmPassword.length > 0 && (
                    <p className="text-sm text-red-500">Пароли не совпадают</p>
                    )}
                </div>

                {authMessage && (
                    <p className="text-green-600 text-sm">{authMessage}</p>
                )}
                {errorMessage && (
                    <p className="text-red-600 text-sm">{errorMessage}</p>
                )}

                <Button type="submit" className="w-full bg-black text-white hover:bg-gray-800" disabled={isLoading || !passwordsMatch || !passwordValid}>
                    {isLoading ? (
                    <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Регистрация...
                    </>
                    ) : (
                    "Зарегистрироваться"
                    )}
                </Button>

                <div className="text-center text-sm">
                    <span className="text-gray-600">Уже есть аккаунт? </span>
                    <Button
                    type="button"
                    variant="link"
                    className="p-0 h-auto font-normal"
                    onClick={() => navigate("/login")}
                    disabled={isLoading}
                    >
                    Войти
                    </Button>
                </div>
                </form>
            </CardContent>
        </Card>
    </div>
  )
}

export default RegisterForm