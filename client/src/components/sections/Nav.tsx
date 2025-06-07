import {NavLink, useLocation} from "react-router-dom";

const PAGES = [
  { path: '/', label: 'Главная' },
  { path: '/task', label: 'Задача' },
  { path: '/solver', label: 'Решатель' },
];

function Nav() {
    const { pathname } = useLocation()

    return (
        <nav className="h-[100px] bg-white shadow-sm">
            <div className="flex h-full">
                {
                    PAGES.map((page) => (
                        page.path !== pathname && (
                            <NavLink
                                key={page.path}
                                to={page.path}
                                className="flex-1 flex items-center justify-center text-2xl
                              transition-all duration-200 hover:shadow-md hover:bg-gray-50"
                            >
                                {page.label}
                            </NavLink>
                        )
                    ))
                }
            </div>
        </nav>
    )
}

export default Nav