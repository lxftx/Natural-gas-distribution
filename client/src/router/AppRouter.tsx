import {createBrowserRouter} from "react-router-dom";
import MainLayout from "@/components/layout/MainLayout";
import HomePage from "@/pages/Home";
import SolverPage from "@/pages/Solver"
import DescriptionPage from "@/pages/Description"
import LoginPage from "@/pages/Auth";
import RegisterPage from "@/pages/Register";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <MainLayout/>,
        children: [
            {
                index: true,
                element: <HomePage/>
            },
            {
                path: "solver",
                element: <SolverPage/>
            },
            {
                path: "desc",
                element: <DescriptionPage/>
            }
        ]
    },
    {
        path: "/login",
        element: <LoginPage />,
    },
        {
        path: "/register",
        element: <RegisterPage />,
    }
]);