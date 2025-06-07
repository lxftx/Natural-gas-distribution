import { AuthProvider } from "@/context/auth-context"
import { createRoot } from 'react-dom/client'
import { RouterProvider } from "react-router-dom";
import { router } from "./router/AppRouter";
import './index.css'

createRoot(document.getElementById('root')!).render(
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
)
