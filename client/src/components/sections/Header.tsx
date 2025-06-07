import { useState, useRef, useEffect } from "react"
import { useAuth } from "@/context/auth-context"
import { useNavigate } from "react-router-dom"
import API from "@/api"

interface UserInfo {
  email: string
  first_name: string
  last_name: string
}

function Header() {
  const { logout, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Закрытие dropdown при клике вне
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  // Получение информации о пользователе при открытии меню
  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const response = await API.infoUser()
        setUserInfo(response.data)
      } catch (error) {
        console.error("Ошибка получения информации о пользователе", error)
      }
    }

    if (dropdownOpen && isAuthenticated) {
      fetchUserInfo()
    }
  }, [dropdownOpen, isAuthenticated])

  const handleLogout = () => {
    logout()
    setDropdownOpen(false)
  }

  return (
    <header className="flex items-center justify-between bg-black h-[100px] p-4 px-10">
      <div className="text-4xl font-thin text-white">
        Распределение природного газа в группе доменных печей
      </div>

      <div className="relative" ref={dropdownRef}>
        {!isAuthenticated ? (
          <button
            onClick={() => navigate("/login")}
            className="text-2xl text-white hover:underline"
          >
            Войти
          </button>
        ) : (
          <>
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="text-2xl text-white hover:underline"
            >
              Пользователь ▼
            </button>

            {dropdownOpen && (
              <div className="absolute right-0 mt-2 w-64 bg-white rounded shadow-lg z-10 p-4 space-y-2">
                {userInfo ? (
                  <div className="text-gray-800 text-sm">
                    <div><strong>Имя:</strong> {userInfo.first_name}</div>
                    <div><strong>Фамилия:</strong> {userInfo.last_name}</div>
                    <div><strong>Email:</strong> {userInfo.email}</div>
                  </div>
                ) : (
                  <div className="text-sm text-gray-500">Загрузка...</div>
                )}

                <hr />

                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-2 py-1 text-sm text-red-600 hover:bg-gray-100 rounded"
                >
                  Выйти
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </header>
  )
}

export default Header
