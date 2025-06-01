"use client"

import { useState } from "react"
import Solver from "./components/section/calculator-form"
import History from "./components/section/calculator-history"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function SolverPage() {
  const [activeTab, setActiveTab] = useState<"solver" | "history">("solver")

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        
        <Tabs defaultValue="calculator" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger 
              value="calculator"
              data-state={activeTab === "solver" ? "active": "inactive"}
              variant={activeTab === "solver" ? "default" : "outline"}
              onClick={() => setActiveTab("solver")}>
                Калькулятор
            </TabsTrigger>
            <TabsTrigger 
              value="history"
              data-state={activeTab === "history" ? "active": "inactive"}
              variant={activeTab === "history" ? "default" : "outline"} 
              onClick={() => setActiveTab("history")}>
                История расчетов
              </TabsTrigger>
          </TabsList>

          {
            activeTab === "solver" && 
            <TabsContent value="calculator">
              <Card>
                <CardHeader>
                  <CardTitle>Расчет параметров печей</CardTitle>
                  <CardDescription>Введите параметры для расчета оптимальных значений</CardDescription>
                </CardHeader>
                <CardContent>
                  <Solver />
                </CardContent>
              </Card>
            </TabsContent>
          }


          {
            activeTab === "history" &&
            <TabsContent value="history">
              <Card>
                <CardHeader>
                  <CardTitle>История расчетов</CardTitle>
                  <CardDescription>Просмотр сохраненных расчетов и их результатов</CardDescription>
                </CardHeader>
                <CardContent>
                  <History />
                </CardContent>
              </Card>
            </TabsContent>
          }
        </Tabs>
      </div>
    </div>
  )
}