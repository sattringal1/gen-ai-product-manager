import { NavLink } from 'react-router-dom'
import { Cpu, LayoutDashboard, Zap } from 'lucide-react'
import './Navigation.css'

export default function Navigation() {
  return (
    <nav className="nav">
      <div className="nav-inner">
        <NavLink to="/" className="nav-brand">
          <Cpu size={22} />
          <span>Gen-AI PM</span>
        </NavLink>
        <div className="nav-links">
          <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} end>
            Home
          </NavLink>
          <NavLink to="/portal" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            <Zap size={15} /> Portal
          </NavLink>
          <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            <LayoutDashboard size={15} /> Dashboard
          </NavLink>
        </div>
      </div>
    </nav>
  )
}
