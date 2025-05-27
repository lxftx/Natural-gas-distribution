function Footer() {
    return (
        <footer className="bg-black text-white py-12 px-4">
            <div className="container mx-auto max-w-6xl">
                {/* Основное предупреждение */}
                <div className="text-center mb-8">
                    <h3 className="text-lg font-medium mb-4">
                        Сайт является инструментом для расчета распределения газа в группе доменных печей
                        и не является коммерческим продуктом
                    </h3>
                    <p className="text-gray-400 text-sm">
                        Результаты расчетов носят рекомендательный характер
                    </p>
                </div>

                {/* Контактная информация и ссылки */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 border-t border-gray-800 pt-8">
                    {/* Контакты разработчиков */}
                    <div>
                        <h4 className="text-lg font-semibold mb-4">Разработчики</h4>
                        <ul className="space-y-2">
                            <li className="flex items-center gap-2">
                                <span className="text-gray-400">Научный руководитель:</span>
                                <span>Гурин И.А.</span>
                            </li>
                            <li className="flex items-center gap-2">
                                <span className="text-gray-400">Магистр:</span>
                                <span>Зеленский О.Д.</span>
                            </li>
                            <li className="flex items-center gap-2 mt-4">
                                <a href="mailto:lxftx04@gmail.com" className="text-blue-400 hover:underline">
                                    lxftx04@gmail.com
                                </a>
                            </li>
                        </ul>
                    </div>

                    {/* Ссылки на организации */}
                    <div>
                        <h4 className="text-lg font-semibold mb-4">Организации</h4>
                        <ul className="space-y-3">
                            <li>
                                <a href="https://urfu.ru"
                                   className="text-gray-300 hover:text-white transition flex items-center gap-2">
                                    <img src="/images/university.png" alt="УрФУ" className="h-5" />
                                    Уральский федеральный университет
                                </a>
                            </li>
                            <li>
                                <a href="https://inmt.urfu.ru"
                                   className="text-gray-300 hover:text-white transition flex items-center gap-2">
                                    <img src="/images/institut.png" alt="ИНМТ" className="h-5" />
                                    Институт новых материалов и технологий
                                </a>
                            </li>
                        </ul>
                    </div>

                    {/* Социальные сети и репозиторий */}
                    <div>
                        <h4 className="text-lg font-semibold mb-4">Связь и код</h4>
                        <div className="flex gap-4 mb-4">
                            <a href="https://t.me/bratella065" className="hover:opacity-80 transition">
                                <img src="/images/tg-blue.png" alt="Telegram" className="h-8" />
                            </a>
                            <a href="https://github.com/lxftx/Natural-gas-distribution" className="hover:opacity-80 transition">
                                <img src="/images/gh-blue.webp" alt="GitHub" className="h-8" />
                            </a>
                        </div>
                        <p className="text-gray-400 text-sm">
                            Исходный код доступен в открытом репозитории
                        </p>
                    </div>
                </div>

                {/* Копирайт и дополнительная информация */}
                <div className="border-t border-gray-800 mt-8 pt-6 text-center text-gray-500 text-sm">
                    <p>© {new Date().getFullYear()} УрФУ. Все права защищены</p>
                    <p className="mt-2">Версия 1.0.0</p>
                </div>
            </div>
        </footer>
    )
}

export default Footer