"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, Search, Eye, Trash2, RefreshCw } from "lucide-react"
import API from "@/api"
import type { HistoryDataGet } from "../types"
import { ResultModal } from "../ResultModal"

function History() {
  const [calculations, setCalculations] = useState<HistoryDataGet[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedResult, setSelectedResult] = useState<HistoryDataGet>()
  const [isModalOpen, setIsModalOpen] = useState(false)

  const loadCalculations = async () => {
    setIsLoading(true)
    try {
      const response = await API.getHistory()
      const data: HistoryDataGet[] = response.data;

      setCalculations(data)
    } catch (error: any) {
      setIsLoading(false)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await API.deleteHistory(id)
      setCalculations((History) => History.filter((calc) => calc.id !== id))

    } catch (error: any) {

    }
  }

  const handleViewResult = (calculation: HistoryDataGet) => {
    setSelectedResult(calculation)
    setIsModalOpen(true)
  }

  useEffect(() => {
    loadCalculations()
  }, [])

  const filteredCalculations = calculations.filter(
    (calc) =>
      String(calc.id).toLowerCase().includes(searchTerm.toLowerCase()) ||
      new Date(calc.created_at).toLocaleDateString().includes(searchTerm),
  )

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Загрузка истории расчетов...</span>
      </div>
    )
  }

  return (
    <>
      <div className="space-y-6">
        {/* Поиск и обновление */}
        <div className="flex items-center gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Поиск по ID или дате..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <Button onClick={loadCalculations} variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" />
            Обновить
          </Button>
        </div>
        
        {/* Таблица расчетов */}
        <Card>
          <CardHeader>
            <CardTitle>История расчетов</CardTitle>
          </CardHeader>
          <CardContent>
            {filteredCalculations.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                {searchTerm ? "Расчеты не найдены" : "История расчетов пуста"}
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>ID</TableHead>
                    <TableHead>Дата создания</TableHead>
                    <TableHead>Количество печей</TableHead>
                    <TableHead>Общая стоимость</TableHead>
                    <TableHead>Действия</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredCalculations.map((calculation) => (
                    <TableRow key={calculation.id}>
                      <TableCell className="font-mono text-sm">{calculation.id}</TableCell>
                      <TableCell>{new Date(calculation.created_at).toLocaleString("ru-RU")}</TableCell>
                      <TableCell>{calculation.calculate.N}</TableCell>
                      <TableCell>
                        {`${calculation.objective.toLocaleString("ru-RU")} руб`}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Button size="sm" variant="outline" onClick={() => handleViewResult(calculation)}>
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button size="sm" variant="outline" onClick={() => handleDelete(calculation.id)}>
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>
      </div>

      {isModalOpen && selectedResult && <ResultModal data={selectedResult} onClose={() => setIsModalOpen(false)} />}
    </>
  )
}

export default History