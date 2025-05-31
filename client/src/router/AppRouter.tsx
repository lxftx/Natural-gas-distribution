import {createBrowserRouter} from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";
import HomePage from "../pages/Home";
import SolverPage from "../pages/Solver"
import DescriptionPage from "../pages/Description"

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
    }
]);