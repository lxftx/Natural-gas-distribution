function Section() {
    return (
        <section className="min-h-[100px] py-10 bg-gray-50">
            <h2 className="text-2xl text-center uppercase mb-10">Разработан при поддержке</h2>

            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Левый блок */}
                    <div className="space-y-8">
                        <a href="https://urfu.ru/ru/" className="flex items-center gap-6 hover:bg-gray-100 p-4 rounded-lg transition">
                            <img src="/images/university.png" alt="УрФУ" className="h-16 object-contain" />
                            <span className="text-xl">Уральский Федеральный Университет</span>
                        </a>

                        <a href="https://inmt.urfu.ru/ru/" className="flex items-center gap-6 hover:bg-gray-100 p-4 rounded-lg transition">
                            <img src="/images/institut.png" alt="ИНМТ" className="h-16 object-contain" />
                            <span className="text-xl">Институт новых материалов и технологий</span>
                        </a>

                        <div className="flex items-center gap-6 p-4">
                            <span className="text-xl">Доцент, Учебный мастер 2 категории кандидат технических наук</span>
                            <span className="text-xl text-right font-semibold">Гурин Иван Александрович</span>
                        </div>
                    </div>

                    {/* Правый блок */}
                    <div className="space-y-8">
                        <div className="flex items-center justify-between p-4">
                            <span className="text-xl">Магистр</span>
                            <span className="text-xl text-right font-semibold">Зеленский Олег Денисович</span>
                        </div>

                        <div className="flex justify-center gap-6 p-4">
                            <a href="https://t.me/bratella065/" className="hover:opacity-80 transition">
                                <img src="/images/tg.png" alt="Telegram" className="h-12" />
                            </a>
                            <a href="https://github.com/lxftx" className="hover:opacity-80 transition">
                                <img src="/images/gh.png" alt="GitHub" className="h-12" />
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default Section