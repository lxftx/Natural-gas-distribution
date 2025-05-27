function Nav() {
    return (
        <nav className="h-[100px] bg-white shadow-sm">
            <div className="flex h-full">
                <a
                    className="flex-1 flex items-center justify-center text-2xl
                              transition-all duration-200 hover:shadow-md hover:bg-gray-50"
                    href="#"
                >
                    Описание
                </a>
                <a
                    className="flex-1 flex items-center justify-center text-2xl
                              transition-all duration-200 hover:shadow-md hover:bg-gray-50"
                    href="#"
                >
                    Решатель
                </a>
            </div>
        </nav>
    )
}

export default Nav