import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { RootLayout } from "@/layouts/RootLayout"
import { SettingsPage } from "@/pages/SettingsPage"
import { HistoryPage } from "@/pages/HistoryPage"
import { Toaster } from "sonner"
import { ThemeProvider } from "@/lib/themes"

// 添加future flags配置
const router = {
  future: {
    v7_startTransition: true,
    v7_relativeSplatPath: true
  }
}

export default function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="app-theme">
      <Router {...router}>
        <RootLayout>
          <Routes>
            <Route path="/" element={<SettingsPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </RootLayout>
        <Toaster richColors closeButton />
      </Router>
    </ThemeProvider>
  )
}
