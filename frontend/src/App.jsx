import { Routes, Route } from "react-router-dom"
import Home from "./pages/Home/Home"
import Teams from "./pages/Teams/Teams"
import Players from "./pages/Players/Players"

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/teams" element={<Teams />} />
      <Route path="/players" element={<Players />} />
    </Routes>
  )
}