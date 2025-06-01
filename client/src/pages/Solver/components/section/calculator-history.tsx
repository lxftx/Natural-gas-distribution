"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, Search, Eye, Trash2, RefreshCw } from "lucide-react"
// import { useToast } from "@/hooks/use-toast"
import API from "@/api"
import type { CalculationHistory } from "@/lib/types"
import { ResultModal } from "../ResultModal"

function History() {
  const [calculations, setCalculations] = useState<CalculationHistory[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedResult, setSelectedResult] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  // const { toast } = useToast()

  const loadCalculations = async () => {
    setIsLoading(true)
    try {
      const data = await API.getCalculationsHistory()
      setCalculations(data)
    } catch (error: any) {
      setIsLoading(false)
      // toast({
      //   title: "Ошибка загрузки",
      //   description: error.message || "Не удалось загрузить историю расчетов",
      //   variant: "destructive",
      // })
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    try {
      await API.deleteCalculation(id)
      setCalculations((prev) => prev.filter((calc) => calc.id !== id))
      // toast({
      //   title: "Расчет удален",
      //   description: "Расчет успешно удален из истории",
      // })
    } catch (error: any) {
      // toast({
      //   title: "Ошибка удаления",
      //   description: error.message || "Не удалось удалить расчет",
      //   variant: "destructive",
      // })
    }
  }

  const handleViewResult = (calculation: CalculationHistory) => {
    setSelectedResult(calculation.result)
    setIsModalOpen(true)
  }

  useEffect(() => {
    loadCalculations()
  }, [])

  const filteredCalculations = calculations.filter(
    (calc) =>
      calc.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
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
                      <TableCell className="font-mono text-sm">{calculation.id.slice(0, 8)}...</TableCell>
                      <TableCell>{new Date(calculation.created_at).toLocaleString("ru-RU")}</TableCell>
                      <TableCell>{calculation.input_data.N}</TableCell>
                      <TableCell>
                        {calculation.result?.total_cost ? `${calculation.result.total_cost.toFixed(2)} руб` : "N/A"}
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